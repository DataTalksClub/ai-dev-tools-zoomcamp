"""Persistence operations for Agent Relay.

Routes and the worker call these functions instead of issuing SQL directly.
Claim, heartbeat, terminal submission, and recovery each use the same atomic
SQLite transaction seam, which is the one area students will later replace by
PostgreSQL row-locking operations.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import (
    Agent,
    Attempt,
    LEASE_SECONDS,
    MAX_ATTEMPTS,
    Task,
    as_db_time,
    db_session,
    db_time,
    immediate_transaction,
    iso_time,
    recover_expired,
    recover_expired_in_session,
    utcnow,
)
from errors import RelayError


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def new_secret(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(32)}"


def secret_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def payload_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def register_agent(name: str, description: str | None) -> dict[str, str]:
    agent_id = new_id("agent")
    token = new_secret("agt")
    now = as_db_time(utcnow())
    with db_session() as db:
        db.add(
            Agent(
                id=agent_id,
                name=name,
                description=description,
                token_hash=secret_hash(token),
                created_at=now,
                last_seen_at=None,
            )
        )
    return {"agent_id": agent_id, "token": token}


def authenticate(token: str) -> Agent:
    token_digest = secret_hash(token)
    # last_seen_at is an authenticated observation and therefore a write.  Use
    # the same writer boundary as task operations so concurrent workers do not
    # hold stale WAL snapshots while trying to update it.
    with immediate_transaction() as db:
        agent = db.scalar(select(Agent).where(Agent.token_hash == token_digest))
        if agent is None or not hmac.compare_digest(agent.token_hash, token_digest):
            raise RelayError("invalid_credentials", "The agent token is invalid.", 401)
        agent.last_seen_at = as_db_time(utcnow())
        db.flush()
        db.expunge(agent)
        return agent


def list_agents(limit: int, cursor: tuple[datetime, str] | None) -> tuple[list[Agent], str | None]:
    with db_session() as db:
        query = select(Agent).order_by(Agent.created_at, Agent.id).limit(limit + 1)
        if cursor:
            created_at, item_id = cursor
            created_at_db = as_db_time(created_at)
            query = query.where(
                (Agent.created_at > created_at_db)
                | ((Agent.created_at == created_at_db) & (Agent.id > item_id))
            )
        rows = list(db.scalars(query))
    has_more = len(rows) > limit
    rows = rows[:limit]
    return rows, encode_cursor(rows[-1].created_at, rows[-1].id) if has_more and rows else None


def create_task(sender_id: str, recipient_id: str, input_text: str, idempotency_key: str | None) -> dict[str, str]:
    # Serializing task creation makes the sender-scoped idempotency check and
    # unique constraint one operation even when two API processes race.
    with immediate_transaction() as db:
        recipient = db.get(Agent, recipient_id)
        if recipient is None:
            raise RelayError("not_found", "Recipient agent not found.", 404)
        if idempotency_key is not None:
            existing = db.scalar(
                select(Task).where(Task.sender_id == sender_id, Task.idempotency_key == idempotency_key)
            )
            if existing is not None:
                if existing.recipient_id != recipient_id or existing.input != input_text:
                    raise RelayError(
                        "idempotency_conflict",
                        "This Idempotency-Key was already used with a different task.",
                        409,
                    )
                return {"task_id": existing.id, "status": existing.status}
        task = Task(
            id=new_id("task"),
            sender_id=sender_id,
            recipient_id=recipient_id,
            input=input_text,
            status="queued",
            output=None,
            error=None,
            attempt_count=0,
            idempotency_key=idempotency_key,
            created_at=as_db_time(utcnow()),
            finished_at=None,
        )
        db.add(task)
        db.flush()
        return {"task_id": task.id, "status": task.status}


def claim_one(agent_id: str, worker_id: str | None) -> dict[str, Any] | None:
    with immediate_transaction() as db:
        now = utcnow()
        recover_expired_in_session(db, now)
        task = db.scalar(
            select(Task)
            .where(Task.recipient_id == agent_id, Task.status == "queued")
            .order_by(Task.created_at, Task.id)
            .limit(1)
        )
        if task is None:
            return None
        if task.attempt_count >= MAX_ATTEMPTS:
            task.status = "failed"
            task.error = "attempts_exhausted"
            task.finished_at = as_db_time(now)
            return None

        claim_token = new_secret("clm")
        task.status = "processing"
        task.attempt_count += 1
        lease_expires = as_db_time(now + timedelta(seconds=LEASE_SECONDS))
        db.add(
            Attempt(
                task_id=task.id,
                attempt_number=task.attempt_count,
                worker_id=worker_id,
                claim_token_hash=secret_hash(claim_token),
                claimed_at=as_db_time(now),
                lease_expires_at=lease_expires,
                finished_at=None,
                outcome="processing",
                terminal_action=None,
                terminal_payload_hash=None,
            )
        )
        db.flush()
        return {
            "task_id": task.id,
            "from": task.sender_id,
            "input": task.input,
            "attempt": task.attempt_count,
            "claim_token": claim_token,
            "lease_expires_at": iso_time(lease_expires),
        }


def _find_attempt_for_token(db: Session, task_id: str, token: str) -> Attempt | None:
    return db.scalar(
        select(Attempt).where(Attempt.task_id == task_id, Attempt.claim_token_hash == secret_hash(token))
    )


def heartbeat(task_id: str, agent_id: str, claim_token: str) -> str:
    with immediate_transaction() as db:
        task = db.get(Task, task_id)
        if task is None or task.recipient_id != agent_id:
            raise RelayError("not_found", "Task not found.", 404)
        attempt = _find_attempt_for_token(db, task_id, claim_token)
        now = utcnow()
        if (
            attempt is None
            or attempt.outcome != "processing"
            or task.status != "processing"
            or db_time(attempt.lease_expires_at) is None
            or db_time(attempt.lease_expires_at) <= now
        ):
            raise RelayError("stale_claim", "This claim is no longer active.", 409)
        attempt.lease_expires_at = as_db_time(now + timedelta(seconds=LEASE_SECONDS))
        db.flush()
        return iso_time(attempt.lease_expires_at) or ""


def commit_terminal(
    task_id: str,
    agent_id: str,
    claim_token: str,
    *,
    action: Literal["complete", "fail"],
    value: str,
) -> dict[str, str]:
    with immediate_transaction() as db:
        task = db.get(Task, task_id)
        if task is None or task.recipient_id != agent_id:
            raise RelayError("not_found", "Task not found.", 404)
        attempt = _find_attempt_for_token(db, task_id, claim_token)
        if attempt is None:
            raise RelayError("stale_claim", "This claim is no longer active.", 409)
        value_digest = payload_hash(value)
        if attempt.outcome in {"completed", "failed"}:
            if attempt.terminal_action == action and attempt.terminal_payload_hash == value_digest:
                return {"task_id": task.id, "status": task.status}
            raise RelayError("conflicting_terminal", "A different terminal result was already accepted.", 409)
        if attempt.outcome != "processing" or task.status != "processing":
            raise RelayError("stale_claim", "This claim is no longer active.", 409)
        now = utcnow()
        if db_time(attempt.lease_expires_at) is None or db_time(attempt.lease_expires_at) <= now:
            raise RelayError("stale_claim", "This claim is no longer active.", 409)
        now_db = as_db_time(now)
        if action == "complete":
            task.output = value
            task.error = None
            task.status = "completed"
            attempt.outcome = "completed"
        else:
            task.output = None
            task.error = value
            task.status = "failed"
            attempt.outcome = "failed"
        task.finished_at = now_db
        attempt.finished_at = now_db
        attempt.terminal_action = action
        attempt.terminal_payload_hash = value_digest
        return {"task_id": task.id, "status": task.status}


def task_for_participant(task_id: str, agent_id: str) -> Task:
    with db_session() as db:
        task = db.get(Task, task_id)
        if task is None or (task.sender_id != agent_id and task.recipient_id != agent_id):
            raise RelayError("not_found", "Task not found.", 404)
        db.expunge(task)
        return task


def list_tasks(
    agent_id: str,
    direction: Literal["sent", "received"],
    status: str | None,
    limit: int,
    cursor: tuple[datetime, str] | None,
) -> tuple[list[Task], str | None]:
    with db_session() as db:
        owner_column = Task.sender_id if direction == "sent" else Task.recipient_id
        query = select(Task).where(owner_column == agent_id).order_by(Task.created_at, Task.id).limit(limit + 1)
        if status:
            query = query.where(Task.status == status)
        if cursor:
            created_at, item_id = cursor
            created_at_db = as_db_time(created_at)
            query = query.where(
                (Task.created_at > created_at_db)
                | ((Task.created_at == created_at_db) & (Task.id > item_id))
            )
        rows = list(db.scalars(query))
        for row in rows:
            db.expunge(row)
    has_more = len(rows) > limit
    rows = rows[:limit]
    return rows, encode_cursor(rows[-1].created_at, rows[-1].id) if has_more and rows else None


def attempts_for_participant(task_id: str, agent_id: str) -> list[Attempt]:
    with db_session() as db:
        task = db.get(Task, task_id)
        if task is None or (task.sender_id != agent_id and task.recipient_id != agent_id):
            raise RelayError("not_found", "Task not found.", 404)
        rows = list(db.scalars(select(Attempt).where(Attempt.task_id == task_id).order_by(Attempt.attempt_number)))
        for row in rows:
            db.expunge(row)
        return rows


def encode_cursor(created_at: datetime, item_id: str) -> str:
    # Response timestamps intentionally use second precision, but a cursor
    # must retain microseconds or several rows created in one second can repeat
    # on the next page.
    precise_time = db_time(created_at)
    raw = json.dumps(
        {"created_at": precise_time.isoformat(timespec="microseconds") if precise_time else None, "id": item_id},
        separators=(",", ":"),
    ).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def decode_cursor(cursor: str | None) -> tuple[datetime, str] | None:
    if not cursor:
        return None
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
        timestamp = datetime.fromisoformat(str(decoded["created_at"]).replace("Z", "+00:00"))
        item_id = str(decoded["id"])
        if not item_id:
            raise ValueError
        return timestamp.astimezone(timezone.utc), item_id
    except (ValueError, TypeError, KeyError, json.JSONDecodeError, UnicodeError):
        raise RelayError("invalid_cursor", "The cursor is invalid.", 400)


__all__ = [
    "authenticate",
    "attempts_for_participant",
    "claim_one",
    "commit_terminal",
    "create_task",
    "decode_cursor",
    "encode_cursor",
    "heartbeat",
    "list_agents",
    "list_tasks",
    "new_secret",
    "payload_hash",
    "recover_expired",
    "register_agent",
    "secret_hash",
    "task_for_participant",
]

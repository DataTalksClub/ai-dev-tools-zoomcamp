"""FastAPI routes for Agent Relay.

Persistence and SQLite transaction details live in :mod:`database` and
:mod:`storage`; the deterministic local worker is in :mod:`worker`.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import hmac
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any, Literal

from fastapi import Depends, FastAPI, Header, Path as FastAPIPath, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, Response
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from database import (
    DEFAULT_PAGE_SIZE,
    MAX_BODY_BYTES,
    MAX_PAGE_SIZE,
    RECOVERY_INTERVAL_SECONDS,
    db_session,
    init_db,
    recover_expired,
)
from dashboard import dashboard_html
from errors import RelayError
from schemas import (
    ClaimRequest,
    ClaimTokenRequest,
    CompleteRequest,
    FailRequest,
    RegisterRequest,
    TaskCreateRequest,
    agent_summary,
    attempt_summary,
    task_summary,
)
from storage import (
    authenticate,
    attempts_for_participant,
    claim_one,
    commit_terminal,
    create_task,
    decode_cursor,
    heartbeat,
    list_agents,
    list_tasks,
    register_agent,
    task_for_participant,
)


LOGGER = logging.getLogger("agent_relay")


def error_response(code: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": {"code": code, "message": message}})


def bearer_value(authorization: str | None) -> str:
    if not authorization:
        raise RelayError("missing_credentials", "Authorization: Bearer <agent-token> is required.", 401)
    scheme, separator, value = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not value.strip():
        raise RelayError("invalid_credentials", "Use Authorization: Bearer <agent-token>.", 401)
    return value.strip()


def current_agent(authorization: str | None = Header(default=None)):
    return authenticate(bearer_value(authorization))


def page_params(limit: int, cursor: str | None) -> tuple[int, tuple[Any, str] | None]:
    if limit < 1 or limit > MAX_PAGE_SIZE:
        raise RelayError("invalid_input", f"limit must be between 1 and {MAX_PAGE_SIZE}.", 400)
    return limit, decode_cursor(cursor)


async def recovery_loop(stop: asyncio.Event) -> None:
    while not stop.is_set():
        try:
            recovered = await asyncio.to_thread(recover_expired)
            if recovered:
                LOGGER.info("recovered %d expired attempt(s)", recovered)
        except asyncio.CancelledError:
            raise
        except Exception:
            LOGGER.exception("lease recovery pass failed")
        try:
            await asyncio.wait_for(stop.wait(), timeout=RECOVERY_INTERVAL_SECONDS)
        except asyncio.TimeoutError:
            pass


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    stop = asyncio.Event()
    recovery_task = asyncio.create_task(recovery_loop(stop))
    try:
        yield
    finally:
        stop.set()
        recovery_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await recovery_task


app = FastAPI(title="Agent Relay", version="0.1.0", lifespan=lifespan)
# ASGI transports used by small scripts do not always run lifespan handlers;
# initialize the schema at import as well as during normal application startup.
init_db()


@app.exception_handler(RelayError)
async def relay_error_handler(_request: Request, exc: RelayError) -> JSONResponse:
    return error_response(exc.code, exc.message, exc.status_code)


@app.exception_handler(RequestValidationError)
async def request_validation_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    # Avoid logging ``exc.errors()``: Pydantic includes submitted values and a
    # malformed claim body could otherwise put a credential in debug logs.
    LOGGER.debug("request validation failed (%d error(s))", len(exc.errors()))
    return error_response("invalid_input", "The request is invalid.", 400)


@app.middleware("http")
async def body_size_limit(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            too_large = int(content_length) > MAX_BODY_BYTES
        except ValueError:
            too_large = True
        if too_large:
            return error_response("body_too_large", "The request body is too large.", 413)
    return await call_next(request)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> JSONResponse:
    try:
        with db_session() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"status": "not_ready"})
    return JSONResponse(status_code=200, content={"status": "ready"})


@app.post("/api/v1/agents", status_code=201)
async def register(
    body: RegisterRequest,
    x_enrollment_secret: str | None = Header(default=None),
) -> dict[str, str]:
    enrollment_secret = os.getenv("RELAY_ENROLLMENT_SECRET") or os.getenv("ENROLLMENT_SECRET")
    if enrollment_secret is not None and not hmac.compare_digest(x_enrollment_secret or "", enrollment_secret):
        raise RelayError("invalid_enrollment", "A valid enrollment secret is required.", 401)
    return register_agent(body.name, body.description)


@app.get("/api/v1/agents")
async def agents(
    current=Depends(current_agent),
    cursor: str | None = Query(default=None),
    limit: int = Query(default=DEFAULT_PAGE_SIZE),
) -> dict[str, Any]:
    del current
    limit, decoded = page_params(limit, cursor)
    rows, next_cursor = list_agents(limit, decoded)
    return {"items": [agent_summary(row) for row in rows], "next_cursor": next_cursor}


@app.get("/api/v1/agents/me")
async def me(current=Depends(current_agent)) -> dict[str, Any]:
    return agent_summary(current)


@app.post("/api/v1/tasks", status_code=201)
async def tasks_create(
    body: TaskCreateRequest,
    current=Depends(current_agent),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> JSONResponse:
    if idempotency_key is not None and (
        not idempotency_key.strip() or len(idempotency_key) > 255 or "\x00" in idempotency_key
    ):
        raise RelayError("invalid_input", "Idempotency-Key must be nonempty and at most 255 characters.", 400)
    for retry in range(3):
        try:
            result = create_task(current.id, body.to, body.input, idempotency_key)
            return JSONResponse(status_code=201, content=result)
        except OperationalError as exc:
            if retry == 2 or "locked" not in str(exc).lower():
                raise
            await asyncio.sleep(0.05 * (retry + 1))
    raise RelayError("storage_error", "The task could not be persisted.", 503)


@app.post("/api/v1/tasks/claim")
async def claim(
    body: ClaimRequest,
    current=Depends(current_agent),
) -> Response:
    deadline = time.monotonic() + body.wait_seconds
    while True:
        try:
            result = await asyncio.to_thread(claim_one, current.id, body.worker_id)
        except OperationalError as exc:
            if "locked" not in str(exc).lower():
                raise
            result = None
        if result is not None:
            return JSONResponse(status_code=200, content=result)
        remaining = deadline - time.monotonic()
        if body.wait_seconds == 0 or remaining <= 0:
            return Response(status_code=204)
        # Polling is deliberate: a task may be submitted by another API
        # process, where an in-process event cannot be signalled.  It also
        # keeps TestClient instances on separate event loops independent.
        await asyncio.sleep(min(remaining, 0.5))


@app.post("/api/v1/tasks/{task_id}/heartbeat")
async def task_heartbeat(
    body: ClaimTokenRequest,
    task_id: str = FastAPIPath(..., min_length=1, max_length=100),
    current=Depends(current_agent),
) -> dict[str, str]:
    return {"lease_expires_at": heartbeat(task_id, current.id, body.claim_token)}


@app.post("/api/v1/tasks/{task_id}/complete")
async def task_complete(
    body: CompleteRequest,
    task_id: str = FastAPIPath(..., min_length=1, max_length=100),
    current=Depends(current_agent),
) -> dict[str, str]:
    return commit_terminal(task_id, current.id, body.claim_token, action="complete", value=body.output)


@app.post("/api/v1/tasks/{task_id}/fail")
async def task_fail(
    body: FailRequest,
    task_id: str = FastAPIPath(..., min_length=1, max_length=100),
    current=Depends(current_agent),
) -> dict[str, str]:
    return commit_terminal(task_id, current.id, body.claim_token, action="fail", value=body.error)


@app.get("/api/v1/tasks/{task_id}")
async def task_get(
    task_id: str = FastAPIPath(..., min_length=1, max_length=100),
    current=Depends(current_agent),
) -> dict[str, Any]:
    return task_summary(task_for_participant(task_id, current.id))


@app.get("/api/v1/tasks")
async def task_list(
    direction: Literal["sent", "received"] = Query(...),
    status: str | None = Query(default=None),
    cursor: str | None = Query(default=None),
    limit: int = Query(default=DEFAULT_PAGE_SIZE),
    current=Depends(current_agent),
) -> dict[str, Any]:
    if status is not None and status not in {"queued", "processing", "completed", "failed"}:
        raise RelayError("invalid_input", "status is invalid.", 400)
    limit, decoded = page_params(limit, cursor)
    rows, next_cursor = list_tasks(current.id, direction, status, limit, decoded)
    return {"items": [task_summary(row) for row in rows], "next_cursor": next_cursor}


@app.get("/api/v1/tasks/{task_id}/attempts")
async def task_attempts(
    task_id: str = FastAPIPath(..., min_length=1, max_length=100),
    current=Depends(current_agent),
) -> dict[str, Any]:
    return {"items": [attempt_summary(row) for row in attempts_for_participant(task_id, current.id)]}


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    return HTMLResponse(dashboard_html())


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_alias() -> HTMLResponse:
    return HTMLResponse(dashboard_html())


def build_cli() -> argparse.ArgumentParser:
    # Kept here so ``python main.py worker ...`` remains the documented command.
    from worker import build_parser

    return build_parser()


def main() -> None:
    from worker import worker_command

    args = build_cli().parse_args()
    if args.slow_seconds < 0 or args.wait_seconds < 0 or args.wait_seconds > 30:
        raise SystemExit("slow-seconds must be >= 0 and wait-seconds must be between 0 and 30")
    asyncio.run(worker_command(args))


if __name__ == "__main__":
    main()


__all__ = ["app", "build_cli", "main"]

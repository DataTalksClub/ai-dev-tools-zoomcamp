"""Deterministic local worker for Agent Relay.

The worker deliberately performs only ``input.upper()``.  Submitted text is
never evaluated as Python or executed by the relay process.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import logging
import os
import stat
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx


LOGGER = logging.getLogger("agent_relay.worker")


def parse_lease(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


async def submit_terminal(client: httpx.AsyncClient, path: str, payload: dict[str, str]) -> httpx.Response:
    """Retry the exact terminal payload on transient transport/server errors."""

    for attempt in range(5):
        try:
            response = await client.post(path, json=payload)
        except httpx.HTTPError:
            if attempt == 4:
                raise
            await asyncio.sleep(min(2**attempt, 8))
            continue
        if response.status_code not in {429, 500, 502, 503, 504} or attempt == 4:
            return response
        retry_after = float(response.headers.get("Retry-After", "0"))
        await asyncio.sleep(min(max(retry_after, 2**attempt, 0.1), 30))
    raise RuntimeError("terminal submission retry loop exhausted")


async def run_worker(
    base_url: str,
    agent_id: str,
    token: str,
    worker_id: str,
    *,
    slow_seconds: float = 0,
    wait_seconds: int = 30,
    stop_after: int | None = None,
) -> None:
    """Poll, uppercase, and acknowledge tasks for one agent identity."""

    base_url = base_url.rstrip("/")
    headers = {"Authorization": f"Bearer {token}"}
    completed = 0
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=40) as client:
        while stop_after is None or completed < stop_after:
            response = await client.post(
                "/api/v1/tasks/claim", json={"worker_id": worker_id, "wait_seconds": wait_seconds}
            )
            if response.status_code == 204:
                continue
            if response.status_code in {429, 500, 502, 503, 504}:
                retry_after = float(response.headers.get("Retry-After", "1"))
                await asyncio.sleep(min(max(retry_after, 0.1), 30))
                continue
            response.raise_for_status()
            claim = response.json()
            task_id = claim["task_id"]
            claim_token = claim["claim_token"]
            active_lease: list[datetime | None] = [parse_lease(claim.get("lease_expires_at"))]
            stop_heartbeating = asyncio.Event()

            async def heartbeat_loop() -> None:
                while not stop_heartbeating.is_set():
                    current_lease = active_lease[0]
                    delay = 20 if current_lease is None else max(
                        0.1, min(20, (current_lease - datetime.now(timezone.utc)).total_seconds() / 3)
                    )
                    try:
                        await asyncio.wait_for(stop_heartbeating.wait(), timeout=delay)
                        return
                    except asyncio.TimeoutError:
                        pass
                    try:
                        heartbeat = await client.post(
                            f"/api/v1/tasks/{task_id}/heartbeat", json={"claim_token": claim_token}
                        )
                        if heartbeat.status_code == 200:
                            active_lease[0] = parse_lease(heartbeat.json().get("lease_expires_at"))
                        else:
                            LOGGER.warning("heartbeat for %s rejected: %s", task_id, heartbeat.text)
                            return
                    except httpx.HTTPError as exc:
                        LOGGER.warning("heartbeat for %s failed: %s", task_id, exc)

            heartbeat_task = asyncio.create_task(heartbeat_loop())
            try:
                if slow_seconds > 0:
                    await asyncio.sleep(slow_seconds)
                # This is the complete execution engine for the starter.  Keep
                # it explicit so task input remains untrusted data.
                output = claim["input"].upper()
                result = await submit_terminal(
                    client,
                    f"/api/v1/tasks/{task_id}/complete",
                    {"claim_token": claim_token, "output": output},
                )
                if result.status_code == 200:
                    completed += 1
                    LOGGER.info("worker=%s task=%s attempt=%s status=completed", worker_id, task_id, claim["attempt"])
                elif result.status_code == 409:
                    LOGGER.warning("worker=%s task=%s claim became stale", worker_id, task_id)
                else:
                    result.raise_for_status()
            finally:
                stop_heartbeating.set()
                heartbeat_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await heartbeat_task


def load_credentials(path: Path) -> dict[str, str] | None:
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict) or not data.get("agent_id") or not data.get("token"):
            return None
        return {"agent_id": str(data["agent_id"]), "token": str(data["token"])}
    except (OSError, ValueError, TypeError):
        return None


def save_credentials(path: Path, credentials: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(credentials, indent=2) + "\n")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)


async def worker_command(args: argparse.Namespace) -> None:
    credentials = load_credentials(args.credentials) if args.credentials else None
    if args.token:
        if not args.agent_id:
            raise SystemExit("--agent-id is required when --token is supplied")
        credentials = {"agent_id": args.agent_id, "token": args.token}
    async with httpx.AsyncClient(base_url=args.base_url.rstrip("/"), timeout=20) as client:
        if credentials is None:
            if not args.name:
                raise SystemExit("--name is required when --credentials does not contain an agent")
            headers = {"X-Enrollment-Secret": args.enrollment_secret} if args.enrollment_secret else {}
            response = await client.post(
                "/api/v1/agents", json={"name": args.name, "description": args.description}, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            credentials = {"agent_id": data["agent_id"], "token": data["token"]}
            if args.credentials:
                save_credentials(args.credentials, credentials)
                LOGGER.info("saved credentials for %s to %s", credentials["agent_id"], args.credentials)
    await run_worker(
        args.base_url,
        credentials["agent_id"],
        credentials["token"],
        args.worker_id,
        slow_seconds=args.slow_seconds,
        wait_seconds=args.wait_seconds,
        stop_after=args.stop_after,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent Relay deterministic uppercase worker")
    subparsers = parser.add_subparsers(dest="command")
    worker = subparsers.add_parser("worker", help="run the deterministic uppercase worker")
    worker.add_argument("--base-url", default=os.getenv("RELAY_BASE_URL", "http://127.0.0.1:8000"))
    worker.add_argument("--worker-id", default=f"worker-{uuid.uuid4().hex[:8]}")
    worker.add_argument("--agent-id", default=None, help="existing agent identity used with --token")
    worker.add_argument("--token", default=None, help="existing agent token (prefer --credentials for persistence)")
    worker.add_argument("--credentials", type=Path, default=None, help="JSON file containing agent_id and token")
    worker.add_argument("--name", default=None, help="register this name when credentials are absent")
    worker.add_argument("--description", default="Deterministic uppercase worker")
    worker.add_argument("--enrollment-secret", default=os.getenv("RELAY_ENROLLMENT_SECRET"))
    worker.add_argument("--slow-seconds", type=float, default=float(os.getenv("RELAY_WORKER_SLOW_SECONDS", "0")))
    worker.add_argument("--wait-seconds", type=int, default=30)
    worker.add_argument("--stop-after", type=int, default=None, help="exit after completing this many tasks")
    return parser


def main() -> None:
    argv = sys.argv[1:]
    # ``main.py worker ...`` is the documented form, while accepting
    # ``worker.py ...`` is convenient when the worker module is copied into a
    # separate process image.
    if argv and argv[0] not in {"worker", "-h", "--help"}:
        argv.insert(0, "worker")
    args = build_parser().parse_args(argv)
    if args.command != "worker":
        build_parser().print_help()
        return
    if args.slow_seconds < 0 or args.wait_seconds < 0 or args.wait_seconds > 30:
        raise SystemExit("slow-seconds must be >= 0 and wait-seconds must be between 0 and 30")
    asyncio.run(worker_command(args))


if __name__ == "__main__":
    main()


__all__ = ["build_parser", "load_credentials", "run_worker", "save_credentials", "submit_terminal", "worker_command"]

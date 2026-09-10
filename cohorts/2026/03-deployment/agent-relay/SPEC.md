# Agent Relay specification

Status: v1 starter. This document defines the protocol and behavior implemented by the local SQLite starter.

The starter deliberately uses SQLite so it can run with no external service. Students may port the storage layer to PostgreSQL as a later deployment exercise; the HTTP protocol, credential rules, task lifecycle, and delivery guarantees should remain unchanged.

## Purpose

Agent Relay lets software agents register, send tasks to one another, claim work, and return results over HTTP and JSON. Agents execute tasks on their own machines. The relay stores identities, tasks, and delivery attempts and exposes a dashboard for observing them.

Registration creates an identity and an inbox. It does not start an agent process. An agent may remain registered while offline; tasks wait until a process serving that identity claims them.

V1 supports one recipient and one final result per task. Conversations, streaming results, attachments, automatic agent selection, and execution of agent code inside the relay are outside its scope. No LLM is required by the relay.

## Components and identity

- **Relay API:** authenticates callers and manages registration, task submission, claims, and results.
- **SQLite (starter):** persists agents, tasks, and delivery attempts. WAL mode and a `BEGIN IMMEDIATE` writer transaction coordinate concurrent claims across API/worker processes. A future student PostgreSQL port can replace this transaction with row locking (for example, `FOR UPDATE SKIP LOCKED`) without changing the protocol.
- **Agent process:** polls for tasks, executes them locally, and reports results. Several processes may serve the same agent identity.
- **Dashboard:** displays agents, last-seen times, task states, results, and delivery history through the API.

An agent ID identifies the logical recipient. A worker ID identifies a running process for diagnostics. Worker IDs do not grant permissions. Every claim has its own secret claim token, distinct from the agent's authentication token.

The API and agent processes can restart without losing queued work. Agent processes persist their registration credentials locally and reuse them after restart.

## HTTP conventions

All endpoints below are relative to `/api/v1`. Request and response bodies use JSON, except responses with no body. IDs are opaque strings. Timestamps use UTC RFC 3339 format. Hosted installations require HTTPS.

Except for registration, all endpoints require `Authorization: Bearer <agent_token>`. The token determines the caller's identity; clients cannot choose a sender or inbox by supplying another agent's ID.

Errors have the form:

```json
{"error": {"code": "stale_claim", "message": "This claim is no longer active."}}
```

Use `400` for invalid input, `401` for missing or invalid credentials, `404` for missing or inaccessible resources, `409` for conflicting state, `413` for an oversized body, and `429` for rate limits. Rate-limit responses include `Retry-After`.

## 1. Register an agent

`POST /agents`

```json
{"name": "alice-reviewer", "description": "Reviews Python code"}
```

Returns `201 Created`:

```json
{"agent_id": "agent_123", "token": "<secret-agent-token>"}
```

Names are display labels, not addresses, and need not be unique. IDs are server-generated and unique. The description is optional and describes intended behavior; it is not a verified capability.

The secret token is returned only at creation. Store only a hash of it on the server. Do not include credentials in dashboard responses, URLs, or logs. V1 has no account recovery; losing a token requires registering a new identity.

Registration is open on a local instance. A shared installation must require an operator-issued enrollment secret for this endpoint and rate-limit registration. The enrollment secret is separate from the per-agent token.

`GET /agents` returns a paginated directory of agent IDs, names, descriptions, registration times, and last-seen times to authenticated callers. `GET /agents/me` returns the caller's own record. Directory entries never contain tokens.

Last-seen time records the most recent authenticated request by that agent. It is an observation, not proof that a worker is still running.

## 2. Send a task

`POST /tasks`

```json
{
  "to": "agent_123",
  "input": "Review this Python function: ..."
}
```

Returns `201 Created`:

```json
{"task_id": "task_456", "status": "queued"}
```

The server records the authenticated caller as the sender. The recipient must exist but may be offline. Sending a task to yourself is allowed. Input is a nonempty UTF-8 string; v1 does not interpret it or prescribe an execution engine.

Clients should send an `Idempotency-Key` header when creating tasks. The server scopes the key to the sender and retains it for the task's lifetime. Repeating the same key and payload returns the original task without creating another. Reusing the key with a different payload returns `409`.

## 3. Claim work

`POST /tasks/claim`

```json
{"worker_id": "alice-laptop-1", "wait_seconds": 30}
```

The server claims at most one queued task addressed to the authenticated agent, preferring the oldest available task. `worker_id` is an optional diagnostic label. `wait_seconds` is an integer from 0 to 30, defaulting to 30. The server holds the request until a task is available or the wait expires.

No available work returns `204 No Content`. A successful claim returns `200 OK`:

```json
{
  "task_id": "task_456",
  "from": "agent_789",
  "input": "Review this Python function: ...",
  "attempt": 1,
  "claim_token": "<secret-claim-token>",
  "lease_expires_at": "2026-09-09T12:05:00Z"
}
```

Claiming atomically changes the task to `processing` and creates a delivery attempt with a new claim token. Concurrent workers cannot successfully claim the same task while that lease is active. The SQLite starter uses a `BEGIN IMMEDIATE` transaction (SQLite has no `FOR UPDATE SKIP LOCKED`) rather than process-local locks. When porting storage to PostgreSQL, use a transaction and row locking such as `FOR UPDATE SKIP LOCKED`.

The default lease lasts 60 seconds from the successful claim. All lease decisions use server/database time. If a claim response is lost, its lease eventually expires; retrying a claim request is not guaranteed to return the same task.

## 4. Execute and maintain the lease

The agent executes the input locally. The relay never executes submitted text. Agents treat incoming task content as untrusted input and run it within their own configured tool permissions.

For work that may outlast the lease, call `POST /tasks/{task_id}/heartbeat` approximately every 20 seconds:

```json
{"claim_token": "<secret-claim-token>"}
```

A valid heartbeat returns `200 OK` with `lease_expires_at`, extending the lease to 60 seconds after the current server time. Heartbeats require both the recipient's authentication token and the active, unexpired claim token.

Expired, superseded, or terminal claims return `409 stale_claim`. An expired lease cannot be revived, even if no replacement worker has claimed the task yet. A worker that loses its lease should stop execution where possible and must not assume its result will be accepted.

## 5. Complete or fail a task

`POST /tasks/{task_id}/complete`

```json
{
  "claim_token": "<secret-claim-token>",
  "output": "The function has an off-by-one error ..."
}
```

A successful request atomically stores the string output, closes the delivery attempt, and changes the task to `completed`. Returns `200 OK` with the task ID and status.

An agent unable to execute the task can call `POST /tasks/{task_id}/fail`:

```json
{
  "claim_token": "<secret-claim-token>",
  "error": "Unsupported task: this agent only reviews Python code."
}
```

This stores the error, closes the attempt, and changes the task to `failed`. Explicit failure is terminal in v1; it does not trigger automatic retries.

Both endpoints require the recipient's credentials and the active, unexpired claim token. Once a terminal submission has succeeded, an identical retry with the same claim token and payload returns the original successful response, even after its former lease deadline. A different result, conflicting terminal action, or superseded token returns `409`. This lets a worker safely retry when a response is lost.

## 6. Retrieve tasks and results

`GET /tasks/{task_id}` returns task details to the sender or recipient:

```json
{
  "task_id": "task_456",
  "from": "agent_789",
  "to": "agent_123",
  "input": "Review this Python function: ...",
  "status": "completed",
  "output": "The function has an off-by-one error ...",
  "error": null,
  "attempt_count": 1,
  "created_at": "2026-09-09T12:03:00Z",
  "finished_at": "2026-09-09T12:04:30Z"
}
```

Unfinished tasks have null output, error, and finish time. Failed tasks have an error and no output. Other agents cannot read the task or its result.

`GET /tasks?direction=sent|received&status=...&cursor=...&limit=...` lists the caller's tasks. Direction is required; status is optional. Lists default to 50 records and allow at most 100, returning `items` and `next_cursor`. The agent directory uses the same pagination envelope.

`GET /tasks/{task_id}/attempts` exposes delivery history to the same authorized callers: attempt number, worker ID, claim time, lease expiry, finish time, and outcome. It never exposes claim tokens. Outcomes are `processing`, `completed`, `failed`, or `expired`.

The sender may poll for the result, initially every two seconds and backing off for longer tasks. The dashboard uses these same authorized endpoints. A shared dashboard must not expose everyone's task contents through a public view.

## Lifecycle and delivery guarantees

```text
queued -> processing -> completed
                     -> failed       (explicit failure)
                     -> queued       (lease expired; attempts remain)
                     -> failed       (lease expired; attempt limit reached)
```

A background recovery loop checks for expired leases at least every five seconds. Recovery marks the attempt `expired` and either requeues the task or fails it with `attempts_exhausted`. The default maximum is five delivery attempts per task. This limit and lease duration are server configuration; clients use the returned deadline rather than assuming a duration.

Recovery, heartbeat, claim, and terminal submission must coordinate through database transactions so a race has one consistent outcome. A completion arriving after expiry is rejected even if recovery has not run yet.

Execution is at least once, subject to the attempt limit. If a worker performs an action and crashes before reporting completion, another worker may execute that task again. Agents performing external side effects should use the task ID as an idempotency key where the external system supports it. The relay cannot guarantee exactly-once execution or undo side effects.

Queue age alone does not expire a task. A recipient that remains offline leaves its tasks queued. Cancellation and manual retries are outside v1; a sender can submit a new task after failure.

## Client loop and operational limits

```text
load saved credentials (register if missing)
repeat:
    claim a task with long polling
    if no task: claim again
    execute locally while heartbeating
    complete or fail, retrying identical submissions on transient errors
```

Clients use bounded exponential backoff with jitter for connection failures, `429`, and `5xx` responses, respecting `Retry-After`. They do not blindly retry validation errors or stale claims. An orderly shutdown stops new claims and tries to finish existing work; abrupt shutdown relies on lease recovery.

V1 limits names to 100 characters, descriptions to 1,000 characters, worker IDs to 100 characters, and request bodies to 256 KiB. Shared installations also enforce configurable per-agent request and queued-task limits. Task content and results are rendered as text in the dashboard.

## Acceptance scenarios

1. Register two agents. One sends a task; the other claims and completes it; the sender reads the result.
2. Register an agent without starting a worker. Its task remains queued until the worker starts with the saved credentials.
3. Start three workers serving one agent and submit multiple tasks. Tasks are distributed with no overlapping active claims for the same task.
4. Kill a worker after claiming. After lease expiry, another worker receives the task with a different claim token and incremented attempt number.
5. Submit a result using the expired token. It is rejected, including before recovery has requeued the task.
6. Heartbeat during a long task. Other workers cannot claim it while the renewed lease remains active.
7. Repeat a task submission with the same idempotency key, and repeat a completion after simulating a lost response. Neither creates duplicate records or changes the accepted result.
8. Exhaust the delivery attempt limit. The task becomes failed and no longer appears in claims.
9. Try to read another pair of agents' task or claim another agent's inbox. Access is denied and no task content or credentials leak.
10. Restart the relay with queued and processing tasks. Queued tasks remain available, and expired processing tasks recover from persisted leases.

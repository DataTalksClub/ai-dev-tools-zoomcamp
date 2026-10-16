"""Pydantic request models and response shaping for Agent Relay."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from database import Agent, Attempt, Task, iso_time


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator("name", "description")
    @classmethod
    def reject_invalid_text(cls, value: str | None) -> str | None:
        if value is not None and "\x00" in value:
            raise ValueError("must not contain NUL bytes")
        return value


class TaskCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    to: str = Field(min_length=1, max_length=100)
    input: str = Field(min_length=1)

    @field_validator("to", "input")
    @classmethod
    def reject_invalid_text(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("must not contain NUL bytes")
        return value


class ClaimRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    worker_id: str | None = Field(default=None, max_length=100)
    wait_seconds: int = Field(default=30, ge=0, le=30)

    @field_validator("worker_id")
    @classmethod
    def validate_worker(cls, value: str | None) -> str | None:
        if value is not None and "\x00" in value:
            raise ValueError("must not contain NUL bytes")
        return value


class ClaimTokenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_token: str = Field(min_length=1, max_length=200)


class CompleteRequest(ClaimTokenRequest):
    output: str = Field(default="")

    @field_validator("output")
    @classmethod
    def validate_output(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("must not contain NUL bytes")
        return value


class FailRequest(ClaimTokenRequest):
    error: str = Field(min_length=1)

    @field_validator("error")
    @classmethod
    def validate_error(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("must not contain NUL bytes")
        return value


def task_summary(task: Task) -> dict[str, Any]:
    return {
        "task_id": task.id,
        "from": task.sender_id,
        "to": task.recipient_id,
        "input": task.input,
        "status": task.status,
        "output": task.output,
        "error": task.error,
        "attempt_count": task.attempt_count,
        "created_at": iso_time(task.created_at),
        "finished_at": iso_time(task.finished_at),
    }


def agent_summary(agent: Agent) -> dict[str, Any]:
    return {
        "agent_id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "created_at": iso_time(agent.created_at),
        "last_seen_at": iso_time(agent.last_seen_at),
    }


def attempt_summary(attempt: Attempt) -> dict[str, Any]:
    return {
        "attempt": attempt.attempt_number,
        "worker_id": attempt.worker_id,
        "claimed_at": iso_time(attempt.claimed_at),
        "lease_expires_at": iso_time(attempt.lease_expires_at),
        "finished_at": iso_time(attempt.finished_at),
        "outcome": attempt.outcome,
    }


__all__ = [
    "ClaimRequest",
    "ClaimTokenRequest",
    "CompleteRequest",
    "FailRequest",
    "RegisterRequest",
    "TaskCreateRequest",
    "agent_summary",
    "attempt_summary",
    "task_summary",
]

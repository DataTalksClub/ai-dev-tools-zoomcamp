"""Data model: projects and their weekly feedback entries."""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone

STATUSES = ("green", "yellow", "red")

STATUS_ALIASES = {
    "g": "green", "green": "green", "ok": "green", "good": "green", "on-track": "green",
    "y": "yellow", "yellow": "yellow", "warn": "yellow", "amber": "yellow", "at-risk": "yellow",
    "r": "red", "red": "red", "blocked": "red", "off-track": "red",
}

STATUS_ICON = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
STATUS_WORD = {"green": "on track", "yellow": "at risk", "red": "off track"}

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


class ValidationError(ValueError):
    """Raised when user input does not fit the model."""


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9._-]+", "-", value.strip().lower()).strip("-.")
    if not slug or not SLUG_RE.match(slug):
        raise ValidationError(f"cannot build a project key from {value!r}")
    return slug


def parse_status(value: str) -> str:
    key = (value or "").strip().lower()
    if key not in STATUS_ALIASES:
        raise ValidationError(
            f"unknown status {value!r}; use one of: {', '.join(STATUSES)}"
        )
    return STATUS_ALIASES[key]


def parse_score(value: object) -> int | None:
    if value in (None, "", "-"):
        return None
    try:
        score = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"score must be a whole number 1-5, got {value!r}") from exc
    if not 1 <= score <= 5:
        raise ValidationError(f"score must be between 1 and 5, got {score}")
    return score


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _clean(items: object) -> list[str]:
    if not items:
        return []
    if isinstance(items, str):
        items = [items]
    return [line.strip() for line in items if str(line).strip()]  # type: ignore[union-attr]


@dataclass
class Project:
    key: str
    name: str = ""
    path: str = ""
    owner: str = ""
    tags: list[str] = field(default_factory=list)
    archived: bool = False
    created_at: str = field(default_factory=now)

    def __post_init__(self) -> None:
        if not SLUG_RE.match(self.key):
            raise ValidationError(
                f"invalid project key {self.key!r}: use lowercase letters, digits, '-', '_', '.'"
            )
        self.name = self.name.strip() or self.key
        self.tags = _clean(self.tags)

    @property
    def label(self) -> str:
        return self.name if self.name != self.key else self.key

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "name": self.name,
            "path": self.path,
            "owner": self.owner,
            "tags": list(self.tags),
            "archived": self.archived,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        return cls(
            key=data["key"],
            name=data.get("name", ""),
            path=data.get("path", ""),
            owner=data.get("owner", ""),
            tags=data.get("tags") or [],
            archived=bool(data.get("archived", False)),
            created_at=data.get("created_at") or now(),
        )


@dataclass
class Entry:
    """One project's feedback for one ISO week."""

    project: str
    week: str
    status: str = "green"
    score: int | None = None
    highlights: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    notes: str = ""
    author: str = ""
    created_at: str = field(default_factory=now)
    updated_at: str = field(default_factory=now)

    LIST_FIELDS = ("highlights", "issues", "blockers", "next_steps")

    def __post_init__(self) -> None:
        self.status = parse_status(self.status)
        self.score = parse_score(self.score)
        for name in self.LIST_FIELDS:
            setattr(self, name, _clean(getattr(self, name)))
        self.notes = self.notes.strip()

    @property
    def is_empty(self) -> bool:
        return not any(getattr(self, name) for name in self.LIST_FIELDS) and not self.notes

    def merged_with(self, other: "Entry") -> "Entry":
        """Fold ``other`` into this entry, appending list fields."""
        merged = {
            name: getattr(self, name) + [
                item for item in getattr(other, name) if item not in getattr(self, name)
            ]
            for name in self.LIST_FIELDS
        }
        notes = "\n".join(part for part in (self.notes, other.notes) if part)
        return replace(
            self,
            status=other.status,
            score=other.score if other.score is not None else self.score,
            notes=notes,
            author=other.author or self.author,
            updated_at=now(),
            **merged,
        )

    def to_dict(self) -> dict:
        return {
            "project": self.project,
            "week": self.week,
            "status": self.status,
            "score": self.score,
            "highlights": list(self.highlights),
            "issues": list(self.issues),
            "blockers": list(self.blockers),
            "next_steps": list(self.next_steps),
            "notes": self.notes,
            "author": self.author,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        return cls(
            project=data["project"],
            week=data["week"],
            status=data.get("status", "green"),
            score=data.get("score"),
            highlights=data.get("highlights") or [],
            issues=data.get("issues") or [],
            blockers=data.get("blockers") or [],
            next_steps=data.get("next_steps") or [],
            notes=data.get("notes", ""),
            author=data.get("author", ""),
            created_at=data.get("created_at") or now(),
            updated_at=data.get("updated_at") or now(),
        )

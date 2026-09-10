"""JSON-backed store for projects and weekly entries.

A single human-readable JSON file keeps the data easy to inspect, diff and
commit alongside a repo. Writes are atomic so an interrupted run cannot
truncate the store.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Entry, Project, ValidationError

VERSION = 1
LOCAL_FILE = "weekly-feedback.json"
ENV_VAR = "WEEKLY_FEEDBACK_FILE"


class StoreError(Exception):
    """Raised for missing projects, duplicate keys and unreadable stores."""


def default_path(cwd: Path | None = None, env: dict | None = None) -> Path:
    """Where the store lives, unless overridden on the command line.

    Order: ``$WEEKLY_FEEDBACK_FILE`` > ``./weekly-feedback.json`` (if present,
    so a repo can carry its own) > ``~/.weekly-feedback/feedback.json``.
    """
    env = os.environ if env is None else env
    override = env.get(ENV_VAR)
    if override:
        return Path(override).expanduser()

    local = (cwd or Path.cwd()) / LOCAL_FILE
    if local.exists():
        return local

    home = env.get("HOME") or str(Path.home())
    return Path(home).expanduser() / ".weekly-feedback" / "feedback.json"


class Store:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._projects: dict[str, Project] = {}
        self._entries: dict[tuple[str, str], Entry] = {}

    # ------------------------------------------------------------------ io

    @classmethod
    def load(cls, path: Path) -> "Store":
        store = cls(path)
        if not store.path.exists():
            return store

        try:
            raw = json.loads(store.path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError as exc:
            raise StoreError(f"{store.path} is not valid JSON: {exc}") from exc
        if not isinstance(raw, dict):
            raise StoreError(f"{store.path} does not contain a feedback store")

        for data in raw.get("projects", []):
            project = Project.from_dict(data)
            store._projects[project.key] = project
        for data in raw.get("entries", []):
            entry = Entry.from_dict(data)
            store._entries[(entry.project, entry.week)] = entry
        return store

    def save(self) -> None:
        payload = {
            "version": VERSION,
            "projects": [p.to_dict() for p in self.projects(include_archived=True)],
            "entries": [e.to_dict() for e in self.entries()],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        tmp.replace(self.path)

    # ------------------------------------------------------------ projects

    def projects(self, include_archived: bool = False) -> list[Project]:
        found = sorted(self._projects.values(), key=lambda p: p.key)
        return found if include_archived else [p for p in found if not p.archived]

    def project(self, key: str) -> Project:
        try:
            return self._projects[key]
        except KeyError:
            raise StoreError(
                f"unknown project {key!r}"
                + (f"; known: {', '.join(sorted(self._projects))}" if self._projects else "")
            ) from None

    def has_project(self, key: str) -> bool:
        return key in self._projects

    def add_project(self, project: Project) -> Project:
        if project.key in self._projects:
            raise StoreError(f"project {project.key!r} already exists")
        self._projects[project.key] = project
        return project

    def update_project(self, project: Project) -> Project:
        self.project(project.key)
        self._projects[project.key] = project
        return project

    def remove_project(self, key: str, drop_entries: bool = False) -> int:
        self.project(key)
        del self._projects[key]
        removed = 0
        if drop_entries:
            for entry_key in [k for k in self._entries if k[0] == key]:
                del self._entries[entry_key]
                removed += 1
        return removed

    # ------------------------------------------------------------- entries

    def entries(
        self,
        project: str | None = None,
        week: str | None = None,
        weeks: list[str] | None = None,
    ) -> list[Entry]:
        wanted = set(weeks) if weeks else None
        found = [
            entry
            for entry in self._entries.values()
            if (project is None or entry.project == project)
            and (week is None or entry.week == week)
            and (wanted is None or entry.week in wanted)
        ]
        return sorted(found, key=lambda e: (e.week, e.project))

    def entry(self, project: str, week: str) -> Entry | None:
        return self._entries.get((project, week))

    def put_entry(self, entry: Entry, mode: str = "merge") -> tuple[Entry, bool]:
        """Store ``entry``; returns the stored entry and whether it replaced one.

        ``mode`` is ``merge`` (append to list fields), ``replace`` (overwrite)
        or ``strict`` (fail if the week already has an entry).
        """
        if not self.has_project(entry.project):
            raise StoreError(f"unknown project {entry.project!r}; add it first")

        existing = self._entries.get((entry.project, entry.week))
        if existing is None:
            self._entries[(entry.project, entry.week)] = entry
            return entry, False

        if mode == "strict":
            raise StoreError(
                f"{entry.project} already has feedback for {entry.week}; "
                "pass --replace to overwrite or --merge to add to it"
            )
        if mode == "replace":
            stored = Entry.from_dict({**entry.to_dict(), "created_at": existing.created_at})
        elif mode == "merge":
            stored = existing.merged_with(entry)
        else:  # pragma: no cover - guarded by the CLI
            raise ValidationError(f"unknown write mode {mode!r}")

        self._entries[(entry.project, entry.week)] = stored
        return stored, True

    def remove_entry(self, project: str, week: str) -> bool:
        return self._entries.pop((project, week), None) is not None

    def known_weeks(self) -> list[str]:
        return sorted({entry.week for entry in self._entries.values()})

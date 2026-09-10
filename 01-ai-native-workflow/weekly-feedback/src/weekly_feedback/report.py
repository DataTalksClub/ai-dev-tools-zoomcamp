"""Rendering: weekly digests, per-project history and trend sparklines."""

from __future__ import annotations

from dataclasses import dataclass

from . import weeks
from .models import STATUS_ICON, STATUS_WORD, STATUSES, Entry, Project
from .storage import Store

SECTIONS = (
    ("highlights", "Highlights"),
    ("issues", "Issues"),
    ("blockers", "Blockers"),
    ("next_steps", "Next"),
)


@dataclass
class Digest:
    week: str
    reported: list[tuple[Project, Entry]]
    missing: list[Project]

    @property
    def counts(self) -> dict[str, int]:
        counts = {status: 0 for status in STATUSES}
        for _, entry in self.reported:
            counts[entry.status] += 1
        return counts

    @property
    def blockers(self) -> list[tuple[Project, str]]:
        return [
            (project, blocker)
            for project, entry in self.reported
            for blocker in entry.blockers
        ]

    @property
    def average_score(self) -> float | None:
        scores = [entry.score for _, entry in self.reported if entry.score is not None]
        return round(sum(scores) / len(scores), 1) if scores else None

    def to_dict(self) -> dict:
        return {
            "week": self.week,
            "range": weeks.describe(self.week),
            "counts": self.counts,
            "average_score": self.average_score,
            "reported": [
                {"project": project.to_dict(), "entry": entry.to_dict()}
                for project, entry in self.reported
            ],
            "missing": [project.key for project in self.missing],
        }


def build_digest(store: Store, week: str, tag: str | None = None) -> Digest:
    projects = [
        project
        for project in store.projects()
        if tag is None or tag in project.tags
    ]
    reported, missing = [], []
    # Worst status first, so a red project is never buried under the greens.
    order = {status: index for index, status in enumerate(("red", "yellow", "green"))}
    for project in projects:
        entry = store.entry(project.key, week)
        if entry is None:
            missing.append(project)
        else:
            reported.append((project, entry))
    reported.sort(key=lambda pair: (order[pair[1].status], pair[0].key))
    return Digest(week=week, reported=reported, missing=missing)


def render_digest(digest: Digest, plain: bool = False) -> str:
    icon = _icons(plain)
    out: list[str] = [
        f"# Weekly feedback - {digest.week} ({weeks.describe(digest.week)})",
        "",
        _headline(digest, icon),
        "",
    ]

    if digest.blockers:
        out.append("## Blockers")
        out += [f"- **{project.label}**: {blocker}" for project, blocker in digest.blockers]
        out.append("")

    for project, entry in digest.reported:
        out += _project_block(project, entry, icon)

    if digest.missing:
        out.append("## No feedback this week")
        out += [f"- {project.label} (`{project.key}`)" for project in digest.missing]
        out.append("")

    if not digest.reported and not digest.missing:
        out.append("_No projects tracked yet - add one with `weekly-feedback project add`._")

    return "\n".join(out).rstrip() + "\n"


def render_history(
    store: Store, project: Project, labels: list[str], plain: bool = False
) -> str:
    icon = _icons(plain)
    out = [f"# {project.label} (`{project.key}`)"]
    if project.owner:
        out.append(f"Owner: {project.owner}")
    if project.tags:
        out.append(f"Tags: {', '.join(project.tags)}")
    out += ["", f"Trend: {sparkline(store, project.key, labels, plain)}", ""]

    for label in labels:
        entry = store.entry(project.key, label)
        if entry is None:
            continue
        out += _week_block(entry, icon)

    if not store.entries(project=project.key, weeks=labels):
        out.append("_No feedback recorded for this period._")
    return "\n".join(out).rstrip() + "\n"


def sparkline(store: Store, project: str, labels: list[str], plain: bool = False) -> str:
    icon = _icons(plain)
    marks = []
    for label in labels:
        entry = store.entry(project, label)
        marks.append(icon[entry.status] if entry else ("." if plain else "⬜"))
    return ("".join(marks) if not plain else " ".join(marks)) + f"  ({labels[0]} -> {labels[-1]})"


def render_pending(digest: Digest) -> str:
    if not digest.missing:
        return f"All tracked projects reported for {digest.week}.\n"
    lines = [f"Missing feedback for {digest.week} ({weeks.describe(digest.week)}):"]
    lines += [
        f"  {project.key:<24} {project.owner or '-'}"
        for project in digest.missing
    ]
    return "\n".join(lines) + "\n"


def render_project_table(projects: list[Project], store: Store) -> str:
    if not projects:
        return "No projects yet. Add one: weekly-feedback project add <key>\n"
    current = weeks.current_week()
    width = max(len(project.key) for project in projects)
    lines = [f"{'KEY'.ljust(width)}  {'LAST':<9} {'OWNER':<14} NAME"]
    for project in projects:
        entries = store.entries(project=project.key)
        last = entries[-1].week if entries else "-"
        flag = " (archived)" if project.archived else ""
        marker = "!" if last != current else " "
        lines.append(
            f"{project.key.ljust(width)} {marker}{last:<9} {(project.owner or '-'):<14} "
            f"{project.name}{flag}"
        )
    lines.append("")
    lines.append("'!' marks a project with no feedback for the current week.")
    return "\n".join(lines) + "\n"


def _headline(digest: Digest, icon: dict) -> str:
    counts = digest.counts
    total = len(digest.reported) + len(digest.missing)
    parts = [f"**{len(digest.reported)}/{total} projects reported**"]
    parts += [
        f"{icon[status]} {counts[status]} {STATUS_WORD[status]}"
        for status in STATUSES
        if counts[status]
    ]
    if digest.average_score is not None:
        parts.append(f"avg score {digest.average_score}/5")
    return " · ".join(parts)


def _project_block(project: Project, entry: Entry, icon: dict) -> list[str]:
    heading = f"## {icon[entry.status]} {project.label}"
    if entry.score is not None:
        heading += f" - {entry.score}/5"
    out = [heading]
    people: list[str] = []
    for person in (entry.author, project.owner):
        if person and person not in people:
            people.append(person)
    if people:
        out.append(f"_{', '.join(people)}_")
    out.append("")
    out += _body(entry)
    return out


def _week_block(entry: Entry, icon: dict) -> list[str]:
    heading = f"## {entry.week} {icon[entry.status]} {STATUS_WORD[entry.status]}"
    if entry.score is not None:
        heading += f" - {entry.score}/5"
    return [heading, ""] + _body(entry)


def _body(entry: Entry) -> list[str]:
    out: list[str] = []
    for attribute, title in SECTIONS:
        items = getattr(entry, attribute)
        if items:
            out.append(f"**{title}**")
            out += [f"- {item}" for item in items]
            out.append("")
    if entry.notes:
        out += [entry.notes, ""]
    if not out:
        out += ["_(no details)_", ""]
    return out


def _icons(plain: bool) -> dict:
    return {status: f"[{status[0].upper()}]" for status in STATUSES} if plain else STATUS_ICON

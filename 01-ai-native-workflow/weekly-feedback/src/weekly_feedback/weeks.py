"""ISO week parsing and formatting helpers."""

from __future__ import annotations

import re
from datetime import date, timedelta

WEEK_RE = re.compile(r"^(\d{4})-?[wW](\d{1,2})$")
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
OFFSET_RE = re.compile(r"^([+-]\d+)$")

_ALIASES = {
    "current": 0,
    "this": 0,
    "now": 0,
    "last": -1,
    "prev": -1,
    "previous": -1,
    "next": 1,
}


class WeekError(ValueError):
    """Raised when a week specification cannot be understood."""


def week_of(day: date) -> str:
    """Return the ISO week label (``2026-W30``) containing ``day``."""
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def current_week(today: date | None = None) -> str:
    return week_of(today or date.today())


def shift(week: str, weeks: int) -> str:
    """Return the label of the week ``weeks`` after (or before) ``week``."""
    return week_of(week_start(week) + timedelta(weeks=weeks))


def week_start(week: str) -> date:
    """Monday of the given ISO week."""
    year, number = _split(week)
    try:
        return date.fromisocalendar(year, number, 1)
    except ValueError as exc:  # week 53 in a 52-week year
        raise WeekError(f"no week {number} in {year}") from exc


def week_end(week: str) -> date:
    """Sunday of the given ISO week."""
    return week_start(week) + timedelta(days=6)


def week_range(week: str) -> tuple[date, date]:
    return week_start(week), week_end(week)


def parse(spec: str, today: date | None = None) -> str:
    """Turn a user-supplied week spec into a canonical ``YYYY-Www`` label.

    Accepts ``2026-W30``, ``2026W30``, a date inside the week (``2026-07-22``),
    the aliases ``current``/``last``/``next``, and relative offsets (``-2``).
    """
    spec = (spec or "").strip()
    if not spec:
        return current_week(today)

    lowered = spec.lower()
    if lowered in _ALIASES:
        return shift(current_week(today), _ALIASES[lowered])

    if OFFSET_RE.match(spec):
        return shift(current_week(today), int(spec))

    match = WEEK_RE.match(spec)
    if match:
        year, number = int(match.group(1)), int(match.group(2))
        label = f"{year}-W{number:02d}"
        week_start(label)  # validates that the week exists
        return label

    match = DATE_RE.match(spec)
    if match:
        try:
            day = date(*(int(part) for part in match.groups()))
        except ValueError as exc:
            raise WeekError(f"not a valid date: {spec}") from exc
        return week_of(day)

    raise WeekError(
        f"cannot read week {spec!r}; use 2026-W30, a date, 'current', 'last' or '-2'"
    )


def recent(count: int, until: str | None = None, today: date | None = None) -> list[str]:
    """The ``count`` week labels ending at ``until`` (default: this week)."""
    end = until or current_week(today)
    return [shift(end, -offset) for offset in range(count - 1, -1, -1)]


def describe(week: str) -> str:
    """Human-readable span, e.g. ``Jul 20 - Jul 26, 2026``."""
    start, end = week_range(week)
    if start.month == end.month:
        return f"{start:%b %-d}-{end:%-d}, {end.year}"
    return f"{start:%b %-d} - {end:%b %-d}, {end.year}"


def _split(week: str) -> tuple[int, int]:
    match = WEEK_RE.match(week.strip())
    if not match:
        raise WeekError(f"not an ISO week label: {week!r}")
    return int(match.group(1)), int(match.group(2))

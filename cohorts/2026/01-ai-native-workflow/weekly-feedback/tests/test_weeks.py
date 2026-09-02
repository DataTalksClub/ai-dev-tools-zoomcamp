from datetime import date

import pytest

from weekly_feedback import weeks

TODAY = date(2026, 7, 22)  # Wednesday of ISO week 2026-W30


def test_week_of_and_current():
    assert weeks.week_of(TODAY) == "2026-W30"
    assert weeks.current_week(TODAY) == "2026-W30"


@pytest.mark.parametrize(
    "spec, expected",
    [
        ("2026-W30", "2026-W30"),
        ("2026W30", "2026-W30"),
        ("2026-w7", "2026-W07"),
        ("2026-07-22", "2026-W30"),
        ("current", "2026-W30"),
        ("last", "2026-W29"),
        ("-3", "2026-W27"),
        ("+1", "2026-W31"),
        ("", "2026-W30"),
    ],
)
def test_parse(spec, expected):
    assert weeks.parse(spec, today=TODAY) == expected


@pytest.mark.parametrize("spec", ["nonsense", "2026-W99", "2026-13-40", "W30"])
def test_parse_rejects_junk(spec):
    with pytest.raises(weeks.WeekError):
        weeks.parse(spec, today=TODAY)


def test_week_range_is_monday_to_sunday():
    start, end = weeks.week_range("2026-W30")
    assert (start, end) == (date(2026, 7, 20), date(2026, 7, 26))
    assert start.weekday() == 0 and end.weekday() == 6


def test_shift_crosses_year_boundary():
    assert weeks.shift("2027-W01", -1) == "2026-W53"
    assert weeks.shift("2026-W52", 2) == "2027-W01"


def test_recent_returns_oldest_first():
    assert weeks.recent(3, until="2026-W30") == ["2026-W28", "2026-W29", "2026-W30"]


def test_describe():
    assert weeks.describe("2026-W30") == "Jul 20-26, 2026"
    assert weeks.describe("2026-W31") == "Jul 27 - Aug 2, 2026"

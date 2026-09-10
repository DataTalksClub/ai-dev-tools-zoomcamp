"""The prompt-driven `add` path, driven by scripted answers."""

import pytest

from weekly_feedback.cli import main
from weekly_feedback.storage import Store


@pytest.fixture
def tty(monkeypatch):
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)

    def script(answers):
        replies = iter(answers)

        def fake_input(prompt=""):
            try:
                return next(replies)
            except StopIteration:  # a real terminal would just keep waiting
                raise EOFError from None

        monkeypatch.setattr("builtins.input", fake_input)

    return script


ANSWERS = [
    "yellow", "3",
    "shipped invoices", "fixed a flaky test", "",
    "CI is slow", "",
    "vendor sandbox down", "",
    "finish the migration", "",
]


def test_interactive_add_collects_every_section(tmp_path, tty, capsys):
    db = tmp_path / "feedback.json"
    main(["--file", str(db), "project", "add", "api"])
    tty(ANSWERS)

    assert main(["--file", str(db), "add", "api", "-w", "2026-W30", "--author", "alexey"]) == 0

    entry = Store.load(db).entry("api", "2026-W30")
    assert entry.status == "yellow" and entry.score == 3
    assert entry.highlights == ["shipped invoices", "fixed a flaky test"]
    assert entry.issues == ["CI is slow"]
    assert entry.blockers == ["vendor sandbox down"]
    assert entry.next_steps == ["finish the migration"]
    assert entry.author == "alexey"
    assert "Recorded api / 2026-W30" in capsys.readouterr().out


def test_interactive_defaults_when_answers_are_blank(tmp_path, tty, capsys):
    db = tmp_path / "feedback.json"
    main(["--file", str(db), "project", "add", "api"])
    tty(["", "", "kept going", ""])  # status, score, one highlight, then end of input

    assert main(["--file", str(db), "add", "api", "-w", "2026-W30"]) == 0
    entry = Store.load(db).entry("api", "2026-W30")
    assert entry.status == "green" and entry.score is None
    assert entry.highlights == ["kept going"]


def test_interactive_add_records_nothing_when_all_sections_are_empty(tmp_path, tty, capsys):
    db = tmp_path / "feedback.json"
    main(["--file", str(db), "project", "add", "api"])
    tty(["green", ""])

    assert main(["--file", str(db), "add", "api", "-w", "2026-W30"]) == 1
    assert Store.load(db).entry("api", "2026-W30") is None
    assert "Nothing recorded" in capsys.readouterr().out


def test_interactive_prefills_from_the_existing_entry(tmp_path, tty, capsys):
    db = tmp_path / "feedback.json"
    main(["--file", str(db), "project", "add", "api"])
    main(["--file", str(db), "add", "api", "-w", "2026-W30", "-s", "red", "--score", "2",
          "-H", "earlier note"])
    tty(["", "", "later note", ""])  # blank status/score keep the stored values

    assert main(["--file", str(db), "add", "api", "-w", "2026-W30"]) == 0
    entry = Store.load(db).entry("api", "2026-W30")
    assert entry.status == "red" and entry.score == 2
    assert entry.highlights == ["earlier note", "later note"]
    assert "already exists" in capsys.readouterr().out


def test_interactive_survives_ctrl_d(tmp_path, tty):
    db = tmp_path / "feedback.json"
    main(["--file", str(db), "project", "add", "api"])
    tty(["green", "4", "one thing"])  # input ends mid-section

    assert main(["--file", str(db), "add", "api", "-w", "2026-W30"]) == 0
    assert Store.load(db).entry("api", "2026-W30").highlights == ["one thing"]

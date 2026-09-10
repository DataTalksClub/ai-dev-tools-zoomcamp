import json

import pytest

from weekly_feedback.cli import main
from weekly_feedback.storage import Store


@pytest.fixture
def db(tmp_path):
    return tmp_path / "feedback.json"


def run(db, *args):
    return main(["--file", str(db), *args])


@pytest.fixture
def seeded(db):
    run(db, "project", "add", "api", "--name", "Billing API", "--owner", "alexey", "--tag", "core")
    run(db, "project", "add", "web", "--name", "Web app", "--tag", "core")
    run(db, "add", "api", "-w", "2026-W30", "-s", "red", "--score", "2",
        "-H", "shipped invoices", "-b", "vendor sandbox down", "-n", "retry migration")
    run(db, "add", "web", "-w", "2026-W30", "-s", "green", "--score", "5", "-H", "new onboarding")
    return db


def test_add_project_and_entry(db, capsys):
    assert run(db, "project", "add", "api") == 0
    assert run(db, "add", "api", "-w", "2026-W30", "-H", "did a thing") == 0

    entry = Store.load(db).entry("api", "2026-W30")
    assert entry is not None and entry.highlights == ["did a thing"]
    assert "Recorded api / 2026-W30" in capsys.readouterr().out


def test_unknown_project_is_an_error(db, capsys):
    assert run(db, "add", "ghost", "-H", "x") == 2
    assert "unknown project 'ghost'" in capsys.readouterr().err


def test_bad_status_is_an_error(db, capsys):
    run(db, "project", "add", "api")
    assert run(db, "add", "api", "-s", "purple", "-H", "x") == 2
    assert "unknown status" in capsys.readouterr().err


def test_add_without_content_fails_when_not_a_tty(db, capsys):
    run(db, "project", "add", "api")
    assert run(db, "add", "api") == 2
    assert "nothing to record" in capsys.readouterr().err


def test_second_add_merges_by_default(db):
    run(db, "project", "add", "api")
    run(db, "add", "api", "-w", "2026-W30", "-H", "first")
    run(db, "add", "api", "-w", "2026-W30", "-H", "second", "-s", "yellow")

    entry = Store.load(db).entry("api", "2026-W30")
    assert entry.highlights == ["first", "second"] and entry.status == "yellow"


def test_replace_flag_overwrites(db):
    run(db, "project", "add", "api")
    run(db, "add", "api", "-w", "2026-W30", "-H", "first")
    run(db, "add", "api", "-w", "2026-W30", "-H", "second", "--replace")
    assert Store.load(db).entry("api", "2026-W30").highlights == ["second"]


def test_report_orders_red_first_and_lists_blockers(seeded, capsys):
    assert run(seeded, "report", "-w", "2026-W30") == 0
    out = capsys.readouterr().out

    assert "2/2 projects reported" in out
    assert "avg score 3.5/5" in out
    assert "**Billing API**: vendor sandbox down" in out
    assert out.index("Billing API - 2/5") < out.index("Web app - 5/5")


def test_report_json_format(seeded, capsys):
    run(seeded, "report", "-w", "2026-W30", "--format", "json")
    payload = json.loads(capsys.readouterr().out)
    assert payload["counts"] == {"green": 1, "yellow": 0, "red": 1}
    assert payload["missing"] == []
    assert payload["range"] == "Jul 20-26, 2026"


def test_report_to_file(seeded, tmp_path, capsys):
    target = tmp_path / "out" / "digest.md"
    run(seeded, "report", "-w", "2026-W30", "-o", str(target))
    assert "Weekly feedback - 2026-W30" in target.read_text()
    assert "Wrote" in capsys.readouterr().err


def test_report_filters_by_tag(seeded, capsys):
    run(seeded, "project", "add", "infra", "--tag", "ops")
    run(seeded, "report", "-w", "2026-W30", "--tag", "ops")
    out = capsys.readouterr().out
    assert "0/1 projects reported" in out and "Billing API" not in out


def test_pending_lists_silent_projects_and_exits_nonzero(seeded, capsys):
    assert run(seeded, "pending", "-w", "2026-W31") == 1
    out = capsys.readouterr().out
    assert "api" in out and "web" in out

    assert run(seeded, "pending", "-w", "2026-W30") == 0
    assert "All tracked projects reported" in capsys.readouterr().out


def test_archived_projects_drop_out_of_the_digest(seeded, capsys):
    run(seeded, "project", "archive", "web")
    run(seeded, "report", "-w", "2026-W30")
    out = capsys.readouterr().out
    assert "1/1 projects reported" in out and "Web app" not in out


def test_show_history_has_a_trend_line(seeded, capsys):
    run(seeded, "add", "api", "-w", "2026-W29", "-s", "green", "-H", "kickoff")
    assert run(seeded, "show", "api", "--weeks", "3", "-w", "2026-W30") == 0
    out = capsys.readouterr().out
    assert "Trend:" in out and "2026-W28 -> 2026-W30" in out
    assert out.index("2026-W29") < out.index("2026-W30")


def test_show_plain_output_avoids_emoji(seeded, capsys):
    run(seeded, "--plain", "show", "api", "-w", "2026-W30")
    out = capsys.readouterr().out
    assert "[R]" in out and "🔴" not in out


def test_project_list_marks_missing_current_week(seeded, capsys):
    run(seeded, "project", "list")
    out = capsys.readouterr().out
    assert "Billing API" in out and "2026-W30" in out and "!" in out


def test_delete_entry(seeded, capsys):
    assert run(seeded, "delete", "api", "-w", "2026-W30") == 0
    assert Store.load(seeded).entry("api", "2026-W30") is None
    assert run(seeded, "delete", "api", "-w", "2026-W30") == 1


def test_export_csv_flattens_lists(seeded, capsys):
    run(seeded, "export", "--format", "csv")
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines[0].startswith("project,week,status,score")
    assert any("vendor sandbox down" in line for line in lines[1:])


def test_export_json_can_be_scoped_to_one_project(seeded, capsys):
    run(seeded, "export", "--key", "api")
    payload = json.loads(capsys.readouterr().out)
    assert {row["project"] for row in payload} == {"api"}


def test_edit_project_fields(seeded, capsys):
    run(seeded, "project", "edit", "api", "--owner", "sam", "--tag", "billing")
    project = Store.load(seeded).project("api")
    assert project.owner == "sam" and project.tags == ["billing"]


def test_empty_store_report_is_friendly(db, capsys):
    assert run(db, "report") == 0
    assert "No projects tracked yet" in capsys.readouterr().out


def test_no_command_prints_help(capsys):
    assert main([]) == 1
    assert "usage:" in capsys.readouterr().out

import json

import pytest

from weekly_feedback.models import Entry, Project, ValidationError, parse_score, slugify
from weekly_feedback.storage import Store, StoreError, default_path


@pytest.fixture
def store(tmp_path):
    store = Store.load(tmp_path / "feedback.json")
    store.add_project(Project(key="api", name="Billing API", owner="alexey"))
    return store


def test_project_key_must_be_a_slug():
    with pytest.raises(ValidationError):
        Project(key="Billing API")
    assert slugify("Billing API!") == "billing-api"


def test_status_and_score_are_normalised():
    entry = Entry(project="api", week="2026-W30", status="AMBER", score="4")
    assert (entry.status, entry.score) == ("yellow", 4)
    with pytest.raises(ValidationError):
        Entry(project="api", week="2026-W30", status="purple")
    with pytest.raises(ValidationError):
        parse_score(9)


def test_list_fields_are_trimmed_and_emptied():
    entry = Entry(project="api", week="2026-W30", highlights=["  shipped  ", "", "   "])
    assert entry.highlights == ["shipped"]
    assert Entry(project="api", week="2026-W30").is_empty


def test_duplicate_project_rejected(store):
    with pytest.raises(StoreError):
        store.add_project(Project(key="api"))


def test_entry_requires_known_project(store):
    with pytest.raises(StoreError):
        store.put_entry(Entry(project="ghost", week="2026-W30", highlights=["x"]))


def test_round_trip_through_disk(store):
    store.put_entry(
        Entry(project="api", week="2026-W30", status="red", score=2, blockers=["vendor"])
    )
    store.save()

    reloaded = Store.load(store.path)
    entry = reloaded.entry("api", "2026-W30")
    assert entry is not None
    assert (entry.status, entry.score, entry.blockers) == ("red", 2, ["vendor"])
    assert reloaded.project("api").name == "Billing API"

    on_disk = json.loads(store.path.read_text())
    assert on_disk["version"] == 1 and len(on_disk["entries"]) == 1


def test_merge_appends_without_duplicating(store):
    store.put_entry(Entry(project="api", week="2026-W30", highlights=["a"], score=3))
    stored, existed = store.put_entry(
        Entry(project="api", week="2026-W30", highlights=["a", "b"], status="yellow"),
        mode="merge",
    )
    assert existed is True
    assert stored.highlights == ["a", "b"]
    assert stored.status == "yellow"
    assert stored.score == 3  # kept, because the new entry did not set one


def test_replace_overwrites_but_keeps_created_at(store):
    first, _ = store.put_entry(Entry(project="api", week="2026-W30", highlights=["a"]))
    stored, _ = store.put_entry(
        Entry(project="api", week="2026-W30", highlights=["b"]), mode="replace"
    )
    assert stored.highlights == ["b"]
    assert stored.created_at == first.created_at


def test_strict_mode_refuses_to_clobber(store):
    store.put_entry(Entry(project="api", week="2026-W30", highlights=["a"]))
    with pytest.raises(StoreError):
        store.put_entry(Entry(project="api", week="2026-W30"), mode="strict")


def test_removing_project_can_keep_history(store):
    store.put_entry(Entry(project="api", week="2026-W30", highlights=["a"]))
    store.remove_project("api")
    assert store.entries(project="api") != []
    assert not store.has_project("api")


def test_entries_filtered_by_week(store):
    store.put_entry(Entry(project="api", week="2026-W29", highlights=["a"]))
    store.put_entry(Entry(project="api", week="2026-W30", highlights=["b"]))
    assert [e.week for e in store.entries(weeks=["2026-W30"])] == ["2026-W30"]
    assert store.known_weeks() == ["2026-W29", "2026-W30"]


def test_corrupt_store_reports_the_path(tmp_path):
    bad = tmp_path / "feedback.json"
    bad.write_text("{not json")
    with pytest.raises(StoreError) as exc:
        Store.load(bad)
    assert str(bad) in str(exc.value)


def test_default_path_precedence(tmp_path):
    env = {"HOME": str(tmp_path), "WEEKLY_FEEDBACK_FILE": str(tmp_path / "custom.json")}
    assert default_path(tmp_path, env) == tmp_path / "custom.json"

    env.pop("WEEKLY_FEEDBACK_FILE")
    assert default_path(tmp_path, env) == tmp_path / ".weekly-feedback" / "feedback.json"

    (tmp_path / "weekly-feedback.json").write_text("{}")
    assert default_path(tmp_path, env) == tmp_path / "weekly-feedback.json"

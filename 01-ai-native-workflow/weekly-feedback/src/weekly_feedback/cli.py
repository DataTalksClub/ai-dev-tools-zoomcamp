"""Command line interface for weekly project feedback."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

from . import gitlog, report, weeks
from .models import STATUSES, Entry, Project, ValidationError, slugify
from .storage import Store, StoreError, default_path

PROG = "weekly-feedback"
__version__ = "0.1.0"


# --------------------------------------------------------------------- parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Track weekly feedback and health across your projects.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            f"  {PROG} project add api --name 'Billing API' --path ~/code/api --owner alexey\n"
            f"  {PROG} add api -s yellow --score 3 -H 'shipped invoices' -b 'waiting on vendor'\n"
            f"  {PROG} add api --from-git            # pull this week's commits in as highlights\n"
            f"  {PROG} report --week last --output digest.md\n"
            f"  {PROG} pending                       # who has not reported yet\n"
            f"  {PROG} show api --weeks 8            # one project's trend and history\n"
        ),
    )
    parser.add_argument("--version", action="version", version=f"{PROG} {__version__}")
    parser.add_argument(
        "-f", "--file", metavar="PATH", help="feedback store to use (default: auto-detect)"
    )
    parser.add_argument(
        "--plain", action="store_true", help="ASCII output instead of status emoji"
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    _add_project_commands(subparsers)
    _add_log_command(subparsers)
    _add_read_commands(subparsers)
    return parser


def _add_project_commands(subparsers) -> None:
    project = subparsers.add_parser("project", help="manage tracked projects")
    actions = project.add_subparsers(dest="action", metavar="<action>")

    add = actions.add_parser("add", help="start tracking a project")
    add.add_argument("key", help="short key, e.g. billing-api")
    add.add_argument("--name", default="", help="display name")
    add.add_argument("--path", default="", help="local repo path (enables --from-git)")
    add.add_argument("--owner", default="", help="person responsible")
    add.add_argument("--tag", action="append", default=[], dest="tags", help="repeatable")
    add.set_defaults(func=cmd_project_add)

    listing = actions.add_parser("list", help="list tracked projects")
    listing.add_argument("--all", action="store_true", help="include archived projects")
    listing.add_argument("--tag", help="only projects with this tag")
    listing.set_defaults(func=cmd_project_list)

    edit = actions.add_parser("edit", help="change a project's details")
    edit.add_argument("key")
    edit.add_argument("--name")
    edit.add_argument("--path")
    edit.add_argument("--owner")
    edit.add_argument("--tag", action="append", dest="tags", help="replaces existing tags")
    edit.set_defaults(func=cmd_project_edit)

    archive = actions.add_parser("archive", help="stop asking for weekly feedback")
    archive.add_argument("key")
    archive.set_defaults(func=cmd_project_archive)

    unarchive = actions.add_parser("unarchive", help="resume tracking a project")
    unarchive.add_argument("key")
    unarchive.set_defaults(func=cmd_project_unarchive)

    remove = actions.add_parser("remove", help="delete a project")
    remove.add_argument("key")
    remove.add_argument(
        "--with-entries", action="store_true", help="also delete its feedback history"
    )
    remove.set_defaults(func=cmd_project_remove)

    project.set_defaults(func=lambda args, store: _usage(project))


def _add_log_command(subparsers) -> None:
    add = subparsers.add_parser("add", help="record feedback for a project week")
    add.add_argument("key", help="project key")
    add.add_argument("-w", "--week", default="current", help="2026-W30, a date, 'last', '-2'")
    add.add_argument("-s", "--status", choices=None, help=f"one of: {', '.join(STATUSES)}")
    add.add_argument("--score", help="1 (bad) to 5 (great)")
    add.add_argument("-H", "--highlight", action="append", default=[], help="repeatable")
    add.add_argument("-i", "--issue", action="append", default=[], help="repeatable")
    add.add_argument("-b", "--blocker", action="append", default=[], help="repeatable")
    add.add_argument("-n", "--next", action="append", default=[], dest="next_steps")
    add.add_argument("--note", default="", help="free-form remark")
    add.add_argument("--author", default="", help="who is giving the feedback")
    add.add_argument(
        "--from-git", action="store_true", help="seed highlights from the repo's commits"
    )
    add.add_argument("--replace", action="store_true", help="overwrite an existing entry")
    add.set_defaults(func=cmd_add)

    remove = subparsers.add_parser("delete", help="remove one feedback entry")
    remove.add_argument("key")
    remove.add_argument("-w", "--week", default="current")
    remove.set_defaults(func=cmd_delete)

    draft = subparsers.add_parser("draft", help="preview a week's git activity for a project")
    draft.add_argument("key")
    draft.add_argument("-w", "--week", default="current")
    draft.set_defaults(func=cmd_draft)


def _add_read_commands(subparsers) -> None:
    digest = subparsers.add_parser("report", help="weekly digest across all projects")
    digest.add_argument("-w", "--week", default="current")
    digest.add_argument("--tag", help="only projects with this tag")
    digest.add_argument("--format", choices=("md", "json"), default="md")
    digest.add_argument("-o", "--output", help="write to a file instead of stdout")
    digest.set_defaults(func=cmd_report)

    show = subparsers.add_parser("show", help="one project's history")
    show.add_argument("key")
    show.add_argument("--weeks", type=int, default=6, metavar="N", help="how many weeks (6)")
    show.add_argument("-w", "--week", default="current", help="week to count back from")
    show.add_argument("--format", choices=("md", "json"), default="md")
    show.set_defaults(func=cmd_show)

    pending = subparsers.add_parser("pending", help="projects with no feedback yet")
    pending.add_argument("-w", "--week", default="current")
    pending.add_argument("--tag")
    pending.set_defaults(func=cmd_pending)

    export = subparsers.add_parser("export", help="dump entries as json or csv")
    export.add_argument("--format", choices=("json", "csv"), default="json")
    export.add_argument("--key", help="limit to one project")
    export.add_argument("-o", "--output")
    export.set_defaults(func=cmd_export)


# -------------------------------------------------------------------- project


def cmd_project_add(args, store: Store) -> int:
    key = args.key if args.key.islower() else slugify(args.key)
    project = Project(
        key=key,
        name=args.name,
        path=str(Path(args.path).expanduser()) if args.path else "",
        owner=args.owner,
        tags=args.tags,
    )
    store.add_project(project)
    store.save()
    print(f"Tracking {project.key} ({project.name}).")
    return 0


def cmd_project_list(args, store: Store) -> int:
    projects = store.projects(include_archived=args.all)
    if args.tag:
        projects = [project for project in projects if args.tag in project.tags]
    print(report.render_project_table(projects, store), end="")
    return 0


def cmd_project_edit(args, store: Store) -> int:
    project = store.project(args.key)
    if args.name is not None:
        project.name = args.name.strip() or project.key
    if args.path is not None:
        project.path = str(Path(args.path).expanduser()) if args.path else ""
    if args.owner is not None:
        project.owner = args.owner
    if args.tags is not None:
        project.tags = args.tags
    store.update_project(project)
    store.save()
    print(f"Updated {project.key}.")
    return 0


def cmd_project_archive(args, store: Store) -> int:
    return _set_archived(args.key, store, True)


def cmd_project_unarchive(args, store: Store) -> int:
    return _set_archived(args.key, store, False)


def _set_archived(key: str, store: Store, archived: bool) -> int:
    project = store.project(key)
    project.archived = archived
    store.update_project(project)
    store.save()
    print(f"{project.key} {'archived' if archived else 'active again'}.")
    return 0


def cmd_project_remove(args, store: Store) -> int:
    kept = len(store.entries(project=args.key))
    removed = store.remove_project(args.key, drop_entries=args.with_entries)
    store.save()
    if args.with_entries:
        print(f"Removed {args.key} and {removed} entries.")
    else:
        print(f"Removed {args.key}; kept {kept} entries (use --with-entries to delete them).")
    return 0


# ------------------------------------------------------------------ feedback


def cmd_add(args, store: Store) -> int:
    project = store.project(args.key)
    week = weeks.parse(args.week)

    highlights = list(args.highlight)
    notes = args.note

    if args.from_git:
        if not project.path:
            raise StoreError(
                f"{project.key} has no path; set one with "
                f"'{PROG} project edit {project.key} --path <repo>'"
            )
        activity = gitlog.collect(project.path, week)
        highlights += [item for item in activity.commits if item not in highlights]
        notes = "\n".join(part for part in (notes, activity.summary) if part)

    supplied = any(
        [highlights, args.issue, args.blocker, args.next_steps, notes, args.status, args.score]
    )
    if not supplied:
        if not sys.stdin.isatty():
            raise ValidationError(
                "nothing to record; pass -s/-H/-i/-b/-n or run interactively"
            )
        return _interactive_add(store, project, week, args)

    entry = Entry(
        project=project.key,
        week=week,
        status=args.status or "green",
        score=args.score,
        highlights=highlights,
        issues=args.issue,
        blockers=args.blocker,
        next_steps=args.next_steps,
        notes=notes,
        author=args.author,
    )
    stored, existed = store.put_entry(entry, mode="replace" if args.replace else "merge")
    store.save()
    verb = "Replaced" if (existed and args.replace) else "Updated" if existed else "Recorded"
    print(f"{verb} {stored.project} / {stored.week} ({stored.status}).")
    return 0


def _interactive_add(store: Store, project: Project, week: str, args) -> int:
    print(f"Feedback for {project.label} - {week} ({weeks.describe(week)})")
    print("Enter one item per line; a blank line ends each section.\n")

    existing = store.entry(project.key, week)
    if existing:
        print("(an entry already exists; new items will be added to it)\n")

    status = _ask_status(existing.status if existing else "green")
    score = _ask_score(existing.score if existing else None)
    entry = Entry(
        project=project.key,
        week=week,
        status=status,
        score=score,
        highlights=_ask_list("What went well?"),
        issues=_ask_list("What did not?"),
        blockers=_ask_list("Blockers?"),
        next_steps=_ask_list("Next week?"),
        author=args.author,
    )
    if entry.is_empty:
        print("Nothing recorded.")
        return 1
    stored, existed = store.put_entry(entry, mode="replace" if args.replace else "merge")
    store.save()
    print(f"\n{'Updated' if existed else 'Recorded'} {stored.project} / {stored.week}.")
    return 0


def _ask(prompt: str) -> str:
    """Read one answer; Ctrl-D counts as an empty one."""
    try:
        return input(prompt).strip()
    except EOFError:
        print()
        return ""


def _ask_status(default: str) -> str:
    return _ask(f"Status [{'/'.join(STATUSES)}] ({default}): ") or default


def _ask_score(default: int | None) -> int | None:
    shown = default if default is not None else "skip"
    return _ask(f"Score 1-5 ({shown}): ") or default


def _ask_list(question: str) -> list[str]:
    print(question)
    items = []
    while True:
        line = _ask("  - ")
        if not line:
            break
        items.append(line)
    return items


def cmd_delete(args, store: Store) -> int:
    week = weeks.parse(args.week)
    if not store.remove_entry(args.key, week):
        print(f"No entry for {args.key} / {week}.", file=sys.stderr)
        return 1
    store.save()
    print(f"Deleted {args.key} / {week}.")
    return 0


def cmd_draft(args, store: Store) -> int:
    project = store.project(args.key)
    week = weeks.parse(args.week)
    if not project.path:
        raise StoreError(f"{project.key} has no path set; add one with 'project edit --path'")

    activity = gitlog.collect(project.path, week)
    print(f"{project.label} - {week} ({weeks.describe(week)})")
    print(f"{activity.summary}\n")
    for commit in activity.commits:
        print(f"  - {commit}")
    if activity.commits:
        print(f"\nRecord it with:\n  {PROG} add {project.key} -w {week} --from-git")
    return 0


# --------------------------------------------------------------------- views


def cmd_report(args, store: Store) -> int:
    digest = report.build_digest(store, weeks.parse(args.week), tag=args.tag)
    if args.format == "json":
        text = json.dumps(digest.to_dict(), indent=2, ensure_ascii=False) + "\n"
    else:
        text = report.render_digest(digest, plain=args.plain)
    _emit(text, args.output)
    return 0


def cmd_show(args, store: Store) -> int:
    project = store.project(args.key)
    count = max(1, args.weeks)
    labels = weeks.recent(count, until=weeks.parse(args.week))
    if args.format == "json":
        entries = store.entries(project=project.key, weeks=labels)
        payload = {
            "project": project.to_dict(),
            "weeks": labels,
            "entries": [entry.to_dict() for entry in entries],
        }
        _emit(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", None)
    else:
        _emit(report.render_history(store, project, labels, plain=args.plain), None)
    return 0


def cmd_pending(args, store: Store) -> int:
    digest = report.build_digest(store, weeks.parse(args.week), tag=args.tag)
    print(report.render_pending(digest), end="")
    return 1 if digest.missing else 0


def cmd_export(args, store: Store) -> int:
    entries = store.entries(project=args.key) if args.key else store.entries()
    if args.key:
        store.project(args.key)  # fail loudly on a typo

    if args.format == "json":
        text = json.dumps([entry.to_dict() for entry in entries], indent=2, ensure_ascii=False)
        text += "\n"
    else:
        buffer = io.StringIO()
        columns = [
            "project", "week", "status", "score",
            "highlights", "issues", "blockers", "next_steps", "notes", "author", "updated_at",
        ]
        writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for entry in entries:
            row = entry.to_dict()
            for name in Entry.LIST_FIELDS:
                row[name] = " | ".join(row[name])
            writer.writerow({column: row[column] for column in columns})
        text = buffer.getvalue()
    _emit(text, args.output)
    return 0


# ----------------------------------------------------------------- plumbing


def _emit(text: str, output: str | None) -> None:
    if output:
        path = Path(output).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path}", file=sys.stderr)
    else:
        sys.stdout.write(text)


def _usage(parser: argparse.ArgumentParser) -> int:
    parser.print_help()
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 1

    path = Path(args.file).expanduser() if args.file else default_path()
    try:
        store = Store.load(path)
        return args.func(args, store)
    except (StoreError, ValidationError, weeks.WeekError, gitlog.GitError) as exc:
        print(f"{PROG}: error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        return 130


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

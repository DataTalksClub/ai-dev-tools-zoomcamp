# weekly-feedback

A small command-line tool for keeping a weekly pulse on a set of projects.
Register the projects you care about, log a short entry per project per week
(status, wins, issues, blockers, next steps), and get a digest you can paste
into a weekly update — plus a nag list of whoever hasn't reported yet.

No dependencies beyond the Python standard library. Data lives in one
human-readable JSON file you can diff and commit.

## Install

```bash
pip install -e .          # provides `weekly-feedback` and the short alias `wfb`
```

Or run it straight from the source tree without installing:

```bash
PYTHONPATH=src python3 -m weekly_feedback --help
```

## Quick start

```bash
# 1. register the projects you want to track
wfb project add api --name "Billing API" --owner alexey --path ~/code/api --tag core
wfb project add web --name "Web app" --owner sam --tag core

# 2. log the week
wfb add api -s red --score 2 \
    -H "refunds endpoint live" \
    -i "flaky integration tests" \
    -b "vendor sandbox is down" \
    -n "retry the migration"

# ...or just answer the prompts
wfb add web

# 3. read the week
wfb report
wfb pending          # exits 1 if anyone is missing — handy in a cron job
```

`wfb report` prints:

```markdown
# Weekly feedback - 2026-W30 (Jul 20-26, 2026)

**2/3 projects reported** · 🟢 1 on track · 🔴 1 off track · avg score 3.5/5

## Blockers
- **Billing API**: vendor sandbox is down

## 🔴 Billing API - 2/5
_alexey_

**Highlights**
- refunds endpoint live

**Issues**
- flaky integration tests
...

## No feedback this week
- Docs site (`docs`)
```

Blockers are lifted to the top and red projects sort first, so the thing that
needs attention is never buried under the projects that are fine.

## Filling an entry from git

If a project has a `--path`, the tool can read the week's commits for you:

```bash
wfb draft api                 # preview what happened, as commit subjects + diffstat
wfb add api --from-git        # record those commits as highlights
wfb add api --from-git -b "still waiting on the vendor"   # combine with your own notes
```

Merge commits, `wip`, `fixup!` and dependency bumps are filtered out.

## Commands

| Command | What it does |
| --- | --- |
| `project add/list/edit/archive/unarchive/remove` | manage the tracked projects |
| `add <key>` | record (or add to) one project's feedback for a week |
| `delete <key>` | drop a single entry |
| `draft <key>` | preview a week's git activity for a project |
| `report` | the weekly digest across all projects (`--format md\|json`) |
| `show <key>` | one project's trend and history (`--weeks N`) |
| `pending` | projects with no feedback yet; exits 1 if any are missing |
| `export` | all entries as `json` or `csv` |

Useful flags: `--week/-w` accepts `2026-W30`, any date inside the week
(`2026-07-22`), `current`, `last`, or an offset like `-2`. `--plain` swaps the
status emoji for `[G]`/`[Y]`/`[R]`. `--tag` narrows `report` and `pending` to
one slice of the portfolio. `-o/--output` writes to a file.

`wfb show api --weeks 8` includes a trend line, where `⬜` is a week with no
entry:

```
Trend: ⬜⬜🟢🟢🟡🟢🟢🔴  (2026-W23 -> 2026-W30)
```

## Where the data lives

Resolved in this order:

1. `--file PATH`
2. `$WEEKLY_FEEDBACK_FILE`
3. `./weekly-feedback.json`, if it exists — so a repo can carry its own
4. `~/.weekly-feedback/feedback.json`

Repeated `add` calls for the same project and week **merge** by default
(list items are appended, duplicates skipped, status and score updated).
Pass `--replace` to overwrite the entry instead. Writes are atomic.

## Development

```bash
uv run --with pytest python -m pytest      # 62 tests, no network, no fixtures on disk
```

Layout: `weeks.py` (ISO week parsing), `models.py` (`Project`, `Entry`,
validation), `storage.py` (the JSON store), `gitlog.py` (git → draft entry),
`report.py` (rendering), `cli.py` (argparse wiring).

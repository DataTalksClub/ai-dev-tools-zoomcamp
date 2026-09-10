"""Pre-fill a weekly entry from a project's git history."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

from . import weeks

# Commit subjects that describe plumbing rather than progress.
NOISE_PREFIXES = ("merge ", "revert ", "wip", "fixup!", "squash!", "bump ", "chore(deps")


class GitError(Exception):
    """Raised when a path is not a usable git repository."""


@dataclass
class Activity:
    commits: list[str]
    authors: list[str]
    files_changed: int
    insertions: int
    deletions: int

    @property
    def summary(self) -> str:
        if not self.commits:
            return "no commits this week"
        return (
            f"{len(self.commits)} commit{'s' if len(self.commits) != 1 else ''}, "
            f"{self.files_changed} file{'s' if self.files_changed != 1 else ''} changed "
            f"(+{self.insertions}/-{self.deletions})"
            + (f" by {', '.join(self.authors)}" if self.authors else "")
        )


def collect(path: str | Path, week: str, runner=None) -> Activity:
    """Summarise commits in ``path`` during ``week``."""
    repo = Path(path).expanduser()
    run = runner or _run
    if not repo.is_dir():
        raise GitError(f"{repo} is not a directory")
    if not (repo / ".git").exists() and run(repo, ["rev-parse", "--git-dir"]) is None:
        raise GitError(f"{repo} is not a git repository")

    start, end = weeks.week_range(week)
    window = [
        f"--since={start.isoformat()} 00:00",
        f"--until={(end + timedelta(days=1)).isoformat()} 00:00",
    ]

    log = run(repo, ["log", "--no-merges", "--pretty=format:%an\t%s", *window]) or ""
    commits: list[str] = []
    authors: list[str] = []
    for line in log.splitlines():
        author, _, subject = line.partition("\t")
        subject = subject.strip()
        if not subject or _is_noise(subject):
            continue
        commits.append(subject)
        if author and author not in authors:
            authors.append(author)

    stats = run(repo, ["log", "--no-merges", "--shortstat", "--pretty=format:", *window]) or ""
    return Activity(
        commits=commits,
        authors=authors,
        files_changed=_sum(stats, "file"),
        insertions=_sum(stats, "insertion"),
        deletions=_sum(stats, "deletion"),
    )


def _is_noise(subject: str) -> bool:
    lowered = subject.lower()
    return any(lowered.startswith(prefix) for prefix in NOISE_PREFIXES)


def _sum(shortstat: str, word: str) -> int:
    total = 0
    for line in shortstat.splitlines():
        for chunk in line.split(","):
            chunk = chunk.strip()
            if word in chunk:
                number = chunk.split()[0]
                if number.isdigit():
                    total += int(number)
    return total


def _run(repo: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitError(f"could not run git in {repo}: {exc}") from exc
    if result.returncode != 0:
        return None
    return result.stdout

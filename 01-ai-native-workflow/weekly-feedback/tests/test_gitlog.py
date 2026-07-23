import shutil
import subprocess

import pytest

from weekly_feedback import gitlog
from weekly_feedback.cli import main


def test_collect_parses_log_and_shortstat(tmp_path):
    calls = []

    def fake_run(repo, args):
        calls.append(args)
        if args[0] == "log" and "--shortstat" in args:
            return " 3 files changed, 40 insertions(+), 5 deletions(-)\n"
        if args[0] == "log":
            return (
                "alexey\tadd invoice export\n"
                "sam\tMerge branch 'main'\n"
                "sam\tfix rounding\n"
                "sam\twip\n"
            )
        return ""

    activity = gitlog.collect(tmp_path, "2026-W30", runner=fake_run)

    assert activity.commits == ["add invoice export", "fix rounding"]
    assert activity.authors == ["alexey", "sam"]
    assert (activity.files_changed, activity.insertions, activity.deletions) == (3, 40, 5)
    assert "2 commits, 3 files changed (+40/-5)" in activity.summary
    log_args = next(args for args in calls if args[0] == "log")
    assert "--since=2026-07-20 00:00" in log_args
    assert "--until=2026-07-27 00:00" in log_args  # end-exclusive, so Sunday is included


def test_collect_rejects_a_non_repo(tmp_path):
    with pytest.raises(gitlog.GitError):
        gitlog.collect(tmp_path, "2026-W30", runner=lambda repo, args: None)
    with pytest.raises(gitlog.GitError):
        gitlog.collect(tmp_path / "missing", "2026-W30", runner=lambda repo, args: "")


def test_empty_week_summary(tmp_path):
    activity = gitlog.collect(tmp_path, "2026-W30", runner=lambda repo, args: "")
    assert activity.summary == "no commits this week"


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_from_git_pulls_real_commits(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {
        "GIT_AUTHOR_NAME": "Tester", "GIT_AUTHOR_EMAIL": "t@example.com",
        "GIT_COMMITTER_NAME": "Tester", "GIT_COMMITTER_EMAIL": "t@example.com",
        "GIT_AUTHOR_DATE": "2026-07-22T10:00:00", "GIT_COMMITTER_DATE": "2026-07-22T10:00:00",
        "PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(tmp_path),
    }
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env)
    (repo / "file.txt").write_text("hello\n")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True, env=env)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "-m", "add greeting"], check=True, env=env
    )

    db = tmp_path / "feedback.json"
    main(["--file", str(db), "project", "add", "repo", "--path", str(repo)])
    assert main(["--file", str(db), "add", "repo", "-w", "2026-W30", "--from-git"]) == 0

    from weekly_feedback.storage import Store

    entry = Store.load(db).entry("repo", "2026-W30")
    assert entry.highlights == ["add greeting"]
    assert "1 commit" in entry.notes


def test_from_git_without_a_path_is_an_error(tmp_path, capsys):
    db = tmp_path / "feedback.json"
    main(["--file", str(db), "project", "add", "api"])
    assert main(["--file", str(db), "add", "api", "--from-git"]) == 2
    assert "has no path" in capsys.readouterr().err

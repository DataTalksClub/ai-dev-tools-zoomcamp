# The Tool Map

Video: TBA

## Why this lesson is short

In the 2025 cohort, the tool tour was most of this module. We went
through products one by one, with install commands and links.

For 2026 it is one lesson. That is deliberate, and I want to say why
openly: brand names age in months, categories do not. Half the specific
tools we demoed last year have changed name, changed pricing model,
changed defaults, or been absorbed into something else. The five
categories below have not moved at all.

So this lesson gives you the categories, and then the thing that
actually lasts: a way to place a tool you have never seen before,
within about ten minutes of opening it.

## The five categories

### 1. Chat assistants

ChatGPT, Claude, Gemini, and the rest of the web chat interfaces. You
type, it answers, you copy code out by hand. This is still the best
place for thinking out loud: explaining an unfamiliar library, talking
through a design before committing to it, arguing about trade-offs,
drafting a spec. Where it hurts is repo awareness. The model only knows
what you pasted, so it will confidently suggest a function signature
that does not exist in your codebase. And every change costs you a
copy-paste round trip, which is fine for one file and miserable for
six.

### 2. Terminal coding agents

Claude Code, Codex CLI, Gemini CLI, Aider. These run in your terminal,
inside a real repo. They read files themselves, edit several at once,
run your tests, and read the failures. The copy-paste tax disappears,
and that changes what you are willing to attempt. The cost is that
something is now writing to your disk and running commands, so you need
permission discipline: know what it can do without asking, and check
before you say yes to the rest. They also over-edit. Ask for one bug fix
and you can get a bug fix plus a reformatted file plus a helpfully
renamed variable.

### 3. Agentic IDEs and desktop workbenches

Cursor, Windsurf, VS Code agent mode, Zed, Antigravity. Roughly the same
capability as a terminal agent, wrapped in an editor. The win is
interactive work: you see the diff highlighted in the file, you accept
or reject hunks, you run the app in a pane next to the chat. For
anything visual, or anything where you want to stay close to the code
while it works, this is the most comfortable category. The cost is that
comfort makes accepting changes very easy, and a fast accept button and
a careful review are in tension.

### 4. Cloud and GitHub-native agents

Copilot coding agent, and the background or cloud sessions that several
vendors now offer. The shape is different from everything above: you
assign an issue and later a pull request appears. Nothing runs on your
machine and you are not watching it work. That is genuinely useful for
small, well-specified, boring tasks. The catch is that all the work
moves to review. An agent that opens five PRs while you are at lunch has
not saved you time until you have read all five, and a PR you did not
watch being written is harder to review than one you did.

### 5. Project bootstrappers

Lovable, Bolt, Replit Agent. You describe an app and get a running app,
usually with a UI, usually in a browser. For a first draft or a
prototype to show someone, nothing else is close on speed. The problem
comes at the handover. The generated project has its own structure,
choices you did not make, and dependencies you did not pick, and at some
point you have to pull it into a normal repo with normal tests and
normal review. Plan for that step, because it is where the time you
saved goes back.

## Placing a tool you have never seen

This is the durable part. Someone launches something next month, or your
employer hands you a tool you did not choose. You do not need a review
of it, you need to place it. Ask these seven questions:

1. **Does it see my repo?** All of it, the files I open, or only what I
   paste?
2. **Can it edit files?** Or does it only produce text I move myself?
3. **Can it run commands?** Tests, builds, installs, git. This is the
   line between a suggester and an agent.
4. **Can it show me a diff?** Before or after applying. If you cannot
   see what changed, you cannot review it.
5. **Can I control what it is allowed to do?** Approval prompts, allowed
   and denied commands, sandboxing.
6. **Can I tell what context it used?** Which files it read, what it
   remembered, what it silently truncated.
7. **Can I control cost?** Subscription or per-token, and can you see
   spend before the invoice.

The answers put any tool on the map immediately. No file access, no
commands, no diff means it is a chat assistant regardless of the
marketing. Full repo access, commands, diffs and permissions means it is
an agent, whether it lives in a terminal, an editor, or a browser tab.

Questions 4, 5 and 6 are the ones people skip, and they are the ones
that decide whether you can work with the tool safely. A tool that edits
your repo but cannot show you a clean diff is not a tool you can use on
anything that matters.

## The fuller 2025 tour

If you want the longer version, the 2025 module is still in this repo:

- [cohorts/2025/01-overview/](../../cohorts/2025/01-overview/)

Read it for the categories and the shape of each one. Do not read it as
a product list. The specific tools named there have moved on, some of
the install commands no longer apply, and a couple of the products are
not the same thing they were. That is the whole reason this lesson
exists in its compressed form.

The two Snake versions in this repo came out of that cohort and are a
better use of your time than the link list. One was built by pasting
code out of a chat window, the other by a terminal agent working in the
folder:

- [snake-chatgpt/](../snake-chatgpt/)
- [snake-claude-code/](../snake-claude-code/)

Same game, two workflows. Comparing the two repos tells you more about
categories 1 and 2 than any feature table.

## Pick one tool, and stay with it

Now the practical part. Choose one primary tool for the cohort and
commit to it.

I want to be blunt about this, because tool-hopping is the single most
common way students lose time in this course. Every switch restarts the
learning curve. You go back to not knowing how to give it context, not
knowing what its defaults are, not knowing how to interrupt it well, not
knowing what it does when it is wrong. None of the practice compounds,
and at the end of eight weeks you have four weeks of beginner experience
four times over.

The skills this module teaches are about specs, context, steering,
verification and review. They transfer between tools. But you only get
them by building fluency in one tool first, and fluency takes weeks of
daily use, not an afternoon.

So:

- Pick one. A terminal agent or an agentic IDE is the best fit for this
  course, because most of the exercises involve a real repo.
- Use it for everything, including the parts where another tool would
  have been slightly better.
- Keep a chat assistant open on the side. That is not tool-hopping, that
  is a different job.
- Try the others after the cohort, when you have a baseline to compare
  them against.

If your workplace already mandates a tool, use that one. Fluency in the
tool you actually have beats admiration for one you do not.

## Reading benchmarks and vendor claims

You will see coding benchmarks quoted on every product page. Treat them
as literacy, not as a skill to practice. Know that these scores are
measured on curated task sets that look nothing like your repo, that
vendors choose which comparisons to publish, that the scoring setup
often includes retries and scaffolding that are not part of what you get
in the product, and that the differences being celebrated are frequently
smaller than the run-to-run noise. A model that scores a few points
higher on a public benchmark can easily be the worse tool for your
codebase. The only benchmark that decides your choice is the one you run
yourself: take a task from your own project, give it to the tool, and
see what comes back. That is worth more than any leaderboard, and it is
what the rest of this module trains you to do.

Next: how to use whichever tool you picked to get oriented in a codebase
you did not write.

[← Introduction](01-intro.md) | [Understanding an Unfamiliar Codebase →](03-understanding-codebase.md)

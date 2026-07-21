# Loop Engineering

Video: TBA

So far you have typed every prompt yourself. Three sessions per task -
groom, implement, test - and you started each one.

That is the right way to learn the shape, and it stops being the right
way at about the fifth task. The steps are the same every time, and the
thing deciding what happens next is you, reading an issue and typing a
sentence.

Loop engineering is what you call it when something else does that.

## The definition

Loop engineering is designing the system that runs a coding agent
repeatedly, instead of driving the agent prompt by prompt.

The "system" is the harness from [lesson 2](02-tool-map.md) plus
whatever you wrap around it: the thing that decides what the agent
picks up next, checks the result, and decides whether to go again.

The unit of engineering effort moves from the instruction to the thing
that issues instructions.

## The ladder

```text
prompt engineering    what you say in one message
context engineering   what the agent knows before it starts
loop engineering      how often it runs, on what, and when it stops
graph engineering     who does what, when there is more than one agent
```

Each rung widens the unit of work: one message, then one session, then
many sessions, then many agents. Graph engineering is [lesson
10](10-graph-engineering.md).

Each rung also assumes the ones below it. A loop around a badly-briefed
agent produces bad results faster, and forty of them. Everything from
[lesson 5](05-context-engineering.md) applies inside every iteration.

## /goal in practice

The simplest useful loop is one command:

```text
/goal all tests pass
```

The agent works, runs the suite, reads the failures, works again, and
stops when the suite is green or it hits the turn limit. You are not in
that cycle.

Something more realistic for our project:

```text
/goal refactor src/cost so no file is over 200 lines, tests stay green
```

Both of those work for the same reason: the stop condition is
something a machine can evaluate. "All tests pass" is checkable. "No
file over 200 lines" is checkable. "Make the code better" is not, and a
loop with that as its goal either stops immediately or never.

This is why [lesson 8](08-testing-a-task.md) insisted that QA outputs
PASS or FAIL. A verdict is a stop condition. A paragraph of nuance is
not.

## The five parts

Any loop has five parts, and naming them is how you tell whether a
setup is sound:

| Part | What it means | What we already have |
|---|---|---|
| Discovery | how it picks the next piece of work | the backlog of issues |
| Isolation | where the work happens | a branch |
| Verification | how the result gets checked | the test suite, and the QA verdict |
| State | what carries between iterations | commits, and the issue status |
| Stop | what ends it | backlog empty, or a turn limit |

The right-hand column is the point of this lesson. You did not build
those five things in order to run loops - you built them because each
one was useful on its own. But they are exactly what a loop needs, and
a project that has them is a project you can automate.

That is also the honest test for someone else's repo. If you cannot
name the stop condition, do not run it unattended.

## How far you can let it run

You can let an agent run on its own exactly as far as something can
automatically tell it that it is wrong.

Not as far as the model is capable, and not as far as you are feeling
optimistic. As far as your checks reach.

A project with a fast test suite can support a loop running for an
hour, because a wrong turn gets caught within one iteration. A project
with no tests cannot, however good the agent is, because nothing in the
loop can produce the word FAIL. It will keep going, confidently, in
whatever direction it started.

That is the real answer to "can I let it run overnight?" It is not
about trust. It is about what happens at 3am when it is wrong and
nothing notices.

## Building the loop yourself

`/goal` and `/loop` are Claude Code commands. Codex has no equivalent -
it has `/goal` as a per-session objective and budget tracker, but
nothing that re-runs the agent. So it is worth knowing how to build
this, both because your tool may not have it and because building one
is how the idea stops being abstract.

Three ways, roughly in order of effort:

- Stop hooks. A hook that fires when the agent finishes a turn can
  check a condition and prompt it again. That is `/goal` by hand.
- Scheduled pings into a tmux session. If the agent is running in tmux,
  anything that can send keystrokes can re-prompt it on a timer. That
  is `/loop` by hand, and it is how I drive agents from a phone -
  described in [The System I Built to Ship Code From a
  Phone](https://alexeyondata.substack.com/p/the-system-i-built-to-ship-code-from).
- A shell loop around non-interactive mode:

```bash
for i in $(seq 1 10); do
  codex exec "run the tests, fix one failing test, then stop" || break
done
```

`codex exec` returns non-zero when a turn fails, which is what the
script branches on. Discovery is in the prompt, verification is the
test run, state is the commits, and the stop condition is the loop
bound. Same five parts.

Also give the agent a way to stop the loop itself. An agent that can
say "I am done" or "I am stuck" ends the run cleanly instead of
burning the remaining iterations.

## What goes wrong

**No stop condition.** The loop runs until you notice, or until your
usage limits notice for you. This is the failure mode behind the
"ralph loop" people write about - an agent left running against a goal
it cannot reach. I wrote about running Claude forever, and what it
costs, in [My Experiments with Claude
Code](https://alexeyondata.substack.com/p/my-experiments-with-claude-code).

**Weak verification.** The tests pass and the work is wrong, so the
loop marches confidently through six issues in the wrong direction. One
bad iteration is a mistake. A loop turns it into a pattern.

**No state.** Each iteration starts fresh with no record of the last
one, so it re-does work, or undoes it. The issue status and the commits
are what prevent this, which is why the engineer role is told to commit
as it goes.

**Silent failure.** It looks like it is working and it is stuck.
Telling those apart from the outside is the most common complaint about
unattended agents, and it is worse when several are running at once.

## Where this goes

The loop in this lesson has one agent in it. It picks up work, does it,
checks it, repeats.

The loop you actually want has three, because you already split the
work into three roles and each one is better at its job for not being
the other two. That is the next lesson, and the command at the end of
it is the one promised in [lesson 1](01-intro.md):

```text
/goal work through the backlog
```

[← Testing a Task](08-testing-a-task.md) | [Graph Engineering →](10-graph-engineering.md)

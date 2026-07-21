# Loop Engineering

Video: TBA

## Definition

**Loop engineering** is the practice of designing [the control system] - whats the control sustem? harness?  

 that
runs a coding agent repeatedly, instead of driving the agent prompt by
prompt.

Designing that system means deciding five things: what work the agent
picks up next, where it does that work, how the result is verified, what
carries over between iterations, and what makes it stop.

Instead of you typing a prompt,
reading the answer, and typing the next prompt, you build the thing that
does the prompting. The unit of engineering effort moves from the
individual instruction to the system that issues instructions.

## Where the term came from

It appeared in early June 2026. Addy Osmani wrote the post that gave it
shape, crediting a couple of practitioners who'd been describing the shift
on X - including people building coding agents at Anthropic. Within a few
weeks it had its own explainer sites, and by the end of June Anthropic had
published a first-party post about loops in Claude Code.

let's include some screenshots from twitter and posts

That last part is why this term is on firmer ground than graph
engineering. It isn't only discussion - the vendors shipped features for
it. Claude Code has `/goal`, `/loop` and `/schedule`, which are exactly
this idea productized: run until a goal is met, repeat a prompt, or run on
a schedule.

The name is still about seven weeks old and people don't agree on its
exact boundaries. But the practice underneath has tooling behind it.

You can also build these things yourself with

- stop hooks (for /goal)
- running agents in tmux sessions and doing regular pings (/loop)
- giving agents tools to stop the work and stop the loops (refer to my tmuxctl)



## The ladder

Loop engineering is usually presented as the next rung on a ladder, and
the ladder is a genuinely useful way to hold it:

```text
prompt engineering    what you say in one message
context engineering   what the agent knows before it starts
loop engineering      how often it runs, on what, and when it stops
graph egnineering     what is it ? add a few words and say that we'll cover it in more details
```

Each rung (what is it) widens the unit of work. And each one assumes the ones below it:
a loop that runs a badly-briefed agent forty times just produces forty
bad results faster. Everything from lesson 5 still applies inside every
iteration of the loop.

## What a loop is made of

Strip away the vocabulary and a loop has five parts. This is the useful
part of the term - it gives you a checklist:

1. **Discovery** - how it decides what to work on next. Failing tests, an
   issue queue, a CI signal, a schedule.
2. **Isolation** - where the work happens, so a half-finished attempt
   doesn't damage anything. Usually a separate branch or checkout.
3. **Verification** - how the result gets checked, by something the agent
   didn't write. Tests, a type checker, a linter, CI.
4. **State** - what it remembers between iterations. A progress file,
   commits, issue status.
5. **Stop condition** - what ends it. Goal met, tests green, iteration
   limit, budget cap, or a human gate.

If you can name all five for a given setup, you understand it. If you
can't name the stop condition, don't run it unattended.

how do we set it? how does it work with /goal? it's too theoretical here
let's make it more practical

## The idea worth remembering

One line does more work than the rest of the term put together:

> The autonomy ceiling is set by verification reach.

I don't undestand it

You can safely delegate exactly as far as you can automatically check. Not
as far as the model is capable, and not as far as you're feeling
optimistic - as far as you can *check*.

This connects directly to lesson 7. When you listed what your project can
verify automatically - types, tests, lint, build, CI - you were measuring
how much autonomy you can afford. A repo with a fast, trustworthy test
suite can support a loop running unattended. A repo with no tests cannot,
no matter how good the agent is, because nothing can tell it that it's
wrong.

That's also the honest answer to "should I let it run overnight?" It
depends on what happens when it's wrong at 3am and nothing catches it.

## The simplest real example

The clearest case is a repo with failing tests:

```text
1. Discovery      read the test output, pick one failure
2. Isolation      work on a branch
3. Verification   re-run the suite
4. State          commit when a test goes green
5. Stop           all green, or ten attempts, whichever comes first
```

That's a loop. You can write it as a short shell script around an agent's
non-interactive mode, or use the built-in commands. Either way, the
structure is the same, and the structure is what the term is naming.

The iteration limit matters more than it looks. Without it, a loop that
can't solve something doesn't fail - it keeps going, and keeps spending.

## The same idea in two tools

It's worth seeing this in two tools, because they draw the line in
different places and that tells you something about the concept.

**Claude Code ships loops as commands.** It groups them into four kinds:
turn-based (you prompt, it stops when it judges the work done),
goal-based, time-based, and proactive ones triggered by events.

```text
/goal    keep going until success criteria are met, or the turn limit is hit
/loop    run a prompt on an interval, locally
```

For example:

```text
/loop 5m check my PR, address review comments, and fix failing CI
```

The guidance on `/goal` is worth repeating, because it is the whole
lesson in one line: it works when you give it deterministic criteria,
like a number of tests passing. "Make it good" is not a stop condition.

**Codex has no loop command.** There is no `/loop` and no `/schedule`.
It has `/goal`, but that is a per-session objective and budget tracker
rather than something that re-runs the agent.

also mention that you can use tools like tmuxctl for schedulign anyhing to any tmux session 

So in Codex you build the loop yourself, around its non-interactive
mode:

```bash
codex exec "run the tests, fix one failing test, then stop"
```

`codex exec` returns a non-zero exit code when a turn fails, which is
what a script branches on. Wrapped in a shell loop with a counter, that
is the same five parts as before: discovery in the prompt, verification
in the test run, state in your commits, and a stop condition in the loop
bound.

Neither approach is more correct. One tool decided this was common enough
to ship as a command; the other left it to you. The structure underneath
is identical, which is the point - if you understand the five parts, you
can build this on any tool, including one that has no word for it.

## What goes wrong

- **No stop condition.** The loop runs until you notice, or until your
  usage limits do. (refer to my article about ralph loop)
- **Weak verification.** The check passes but the work is wrong, so the
  loop confidently marches through twelve tasks in the wrong direction.
- **No state.** Each iteration starts over, redoing work or undoing the
  last pass.
- **Silent failure.** It looks like it's working and it's stuck. Being
  unable to tell those apart is the most common complaint about running
  agents unattended.

Every one of these is a missing piece from the list of five.

it's very abstract I want concrete things 

## Where we go deeper

We are not building production loops in this module. 
yes we aren't but I want to show /goal in practice

simple loops: /goal "refactor this codebase" - here
more complex loops /goal work though the backlog - next lesson 
where we combine loops and multi-agent setup


The point here is
that you know what the term means, can identify the five parts, and can
judge whether a repo is ready for one.

[Module 3](../../03-mcp/) is where we build agent capabilities properly -
including the pieces that make unattended running safe.

Next: the same idea, but with several agents instead of one.

[← Testing a Task](08-testing-a-task.md) | [Graph Engineering →](10-graph-engineering.md)

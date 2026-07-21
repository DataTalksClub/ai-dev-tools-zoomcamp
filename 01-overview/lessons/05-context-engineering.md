# Context Engineering

Video: TBA

## Definition

Context engineering is the practice of making your project
understandable to an agent before the agent starts working.

It is not "writing better prompts". A prompt is one message in one
session. Context is everything that is relevant for the agent to know before they start their task.

## AGENTS.md

Every session starts from a clean slate. The agent doesn't remember what happend in the past.

The agent that refactored your test suite yesterday does not know today
that you use `pytest` and not `unittest`. So it has to discover it over and over again.

You can help it by spefying these things in `AGENTS.md`.
`AGENTS.md` is a plain Markdown file at the root of the repo
describing the project to any coding agent that opens it.

You can put anything you want to this file, and it will be read by the 
agents at the startup. 

Note: Claude Code reads `CLAUDE.md`, not `AGENTS.md`, like Codex and most other tools. I use multuple coding assistants, so for me my `CLAUDE.md` looks like that:

```markdown
@AGENTS.md
```

## What belongs in it

You don't describe the project in AGENTS.md. The
description belongs in the README, which the agent can read anyway.

What you put there:

- Commands, especially the non-obvious ones - how to run a single test,
  not just the whole suite
- Tooling rules - which package manager, which command form
- Constraints and cautions - what does not exist, and what must never
  be printed or committed
- Pointers to the real documents - where the spec, the process and the
  tasks live
- Corrections you got tired of repeating - anything you have typed more
  than once

`AGENTS.md` is not
documentation for humans (but it could be useful for them too).
It is the accumulated set of things the agent got wrong,
plus the things it cannot guess, or finding them out is not trivail.

Keep it short.

Here is one for the meeting cost calculator:

```markdown
Commands

- `npm run dev` - dev server
- `npm test` - the whole suite
- `npm test -- cost` - one test file

Rules

- Cost and rate calculations go in `src/cost/`, not in components
- Money is integer cents everywhere.
- Do not add dependencies without asking
- Commit regularly
```

I try to avoid putting markup tehre like sections or bold formatting, tables, etc. They don't add any value and only result in higher token consumption.



## What does not belong in it

This is where beginners go wrong, and the failure always has the same
shape: the file grows until nobody, human or model, follows it.

Keep these out:

- Transient task state. "Currently working on the cost calculation" is a
  session note, not a project fact.
- Anything secret. Keys, tokens, internal URLs, customer names.
  This file is read by tools, copied into contexts and committed to
  git. Use `.env` for that.
- Long prose. 
- Rules nobody enforces. Delete it or enforce it programmatically.

A lean file that gets followed beats a long one that gets skimmed.
Every line you add makes the other lines slightly less likely to be
noticed. That cost is invisible until the file is already too big. If
yours is drifting past a couple of screens, the signal is to cut, not
to add a table of contents.


## The process document

`process.md` says how work moves through the project.

It could live inside `AGENTS.md`, and on day one it may as well. It
gets its own file for two reasons.

It changes for different reasons than everything else. You can rewrite
how you work without touching a line of the project, and restructure
the project without changing how you work. Things that change
separately are easier to keep in separate files.

And it is the section that grows. Three lines today, but as soon as
more than one agent is involved it turns into roles, handoffs, and
rules about who is allowed to commit. Keeping it out of `AGENTS.md` is
what stops `AGENTS.md` growing along with it.

For now it can be three lines:

```markdown
- Tasks are GitHub issues, one at a time
- Read the acceptance criteria before starting and before closing
- Do not commit until the tests pass
```

Let's include it in our AGENTS.md:

```md
The working process in `_docs/process.md`. When implementing a task, read this file.
```


## Other documents

In addition to `AGENTS.md`, you can keep a separate document for each
thing you find yourself explaining over and over. The ones that come up
most often:

- `testing-guidelines.md` - what counts as a real test, and the ways
  agents write fake ones
- `design-system.md` - colours, typography, spacing, so the UI does not
  drift every session
- `setup.md` - how to get the project running from nothing
- `api.md` - the endpoints, and what they return

I keep them together in a `_docs/` folder and link them from `AGENTS.md`.

The agent reads `AGENTS.md` at the start of every session, so it learns that these documents exist. 
It does not read them yet, only when it's needed for the task.

The section with document can look like:

```markdown
Documents

- `_docs/plan.md` - what we are building
- `_docs/process.md` - how work moves through the project
- Before writing tests, read `_docs/testing-guidelines.md`
- For anything touching the UI, read `_docs/design-system.md`
```

It then opens the document relevant for the task: 

- A task about the UI pulls in the design system.
- A task about tests pulls in the testing guidelines.

it keeps `AGENTS.md` short while the project's written
context keeps growing.

## Keep it alive

The file rots like any other documentation, and the signal that it
needs attention is specific:

> When the agent gets something wrong twice in the same way, the file
> is missing a line.

Not the first time - that might be luck. The second time is a pattern,
and a pattern means the project has a rule that exists only in your
head. When you catch yourself typing a correction you have typed
before, add the line instead. Over a few weeks this converges: the
corrections get rarer, and the ones left are genuinely one-offs.

The reverse also happens. When a constraint stops being true, delete
the line. Stale instructions are worse than none, because the agent
will follow them.

## The first layer of a bigger system

Instruction files are the base. Several things build on top of them,
and the words are worth knowing now even though we are not setting
them up here:

- Reusable commands and skills - packaging a repeated workflow so
  you invoke it by name instead of describing it again
- Permission modes - deciding in advance what the agent may do
  without asking you
- Hooks - running your own checks automatically at fixed points in
  the agent's work

All three are covered properly in [Module 3](../../03-mcp/), and all
three are less useful than they sound if the base is missing. An agent
with elaborate hooks and no idea how to run your tests is not ahead of
one with a good `AGENTS.md`.

## Your deliverable

This is the artifact for this module. Before you move on:

1. Write `AGENTS.md` for your own project: the commands, the rules,
   and pointers to your spec and process docs. Keep it under two
   screens.
2. Add a `CLAUDE.md` containing `@AGENTS.md`, or the equivalent
   pointer for your tool.
3. Start a fresh session, give the agent a small task, and watch what
   it still gets wrong. Those are your missing lines.

Step 3 is the one people skip, and it is the only one that tells you
whether the file works.

[← Bootstrapping a Project](04-bootstrapping.md) | [Implementing a Task →](06-implementing-a-task.md)

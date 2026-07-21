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

`process.md` says how work moves through the project. It could live inside `AGENTS.md`, but I keep a separate file for that specifically. 

For now we can only add three lines there, but it will certainly grow as our project gets bigger.


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

In addition to `process.md`, you can keep a separate document for each
thing you need to explain over and over again.

In my projects I often have these files:

- `testing-guidelines.md` - how to write tests
- `design-system.md` - colours, typography, spacing, so the UI does not
  drift every session
- `setup.md` - how to get the project running
- `api.md` - the endpoints, and what they return

I keep them together in a `_docs/` folder and link them from `AGENTS.md`.

The agent reads `AGENTS.md` at the start of every session, so it learns that these documents exist. 
It does not read them immediately, only when it's actually needed for the task.

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


[← Bootstrapping a Project](04-bootstrapping.md) | [Grooming a Task →](06-grooming-a-task.md)

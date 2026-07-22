# Context Engineering

Video: TBA

## Definition

Context engineering is the practice of making your project
understandable to an agent before the agent starts working.

It's not "writing better prompts". A prompt is one message in one
session, while context is everything the agent needs to know before it starts the task.

## AGENTS.md

Every session starts from a clean slate, and the agent doesn't remember what happened before.

The agent that refactored your test suite yesterday doesn't know today
that you use `pytest` and not `unittest`. So it has to discover it over and over again.

You can help it by specifying these things in `AGENTS.md`.
`AGENTS.md` is a plain Markdown file at the root of the repo
describing the project to any coding agent that opens it.

You can put anything you want to this file, and the agents read it at startup.

Note: Claude Code reads `CLAUDE.md`, not `AGENTS.md` like Codex and most other tools do.

I use multiple coding assistants, so my `CLAUDE.md` looks like this:

```markdown
@AGENTS.md
```

## Contents of AGENTS.md

You don't describe the project in AGENTS.md. The
description belongs in the README, which the agent can read anyway.

What you put there:

- Commands, especially the non-obvious ones - how to run a single test,
  not just the whole suite
- Tooling rules - which package manager, which command form
- Constraints and cautions - what doesn't exist, and what must never
  be printed or committed
- Pointers to the real documents - where the spec, the process and the
  tasks live
- Corrections you got tired of repeating - anything you have typed more
  than once

`AGENTS.md` isn't documentation for humans, though it can be useful for
them too. It collects the things the agent got wrong, plus the things
it can't guess or would spend time discovering.

Keep it short.

Here's one for the meeting cost calculator:

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

I try to avoid putting markup there like sections, bold formatting, or tables. They don't add any value and only result in higher token consumption.



## Things to leave out

This is where beginners go wrong, and the failure is always the same:
the file grows until nobody, human or model, follows it.

Keep these out:

- Transient task state. "Currently working on the cost calculation" is a
  session note, not a project fact.
- Anything secret. Keys, tokens, internal URLs, customer names.
  This file is read by tools, copied into contexts and committed to
  git. Use `.env` for that.
- Long explanations.
- Rules nobody enforces. Delete it or enforce it programmatically.

A lean file that gets followed beats a long one that gets skimmed.
Every line you add makes the other lines slightly less likely to be
noticed. That cost is invisible until the file is already too big. If
yours is drifting past a couple of screens, cut it rather than add a
table of contents.


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
- `design-system.md` - colours, typography, spacing, so the UI doesn't
  drift every session
- `setup.md` - how to get the project running
- `api.md` - the endpoints, and what they return

I keep them together in a `_docs/` folder and link them from `AGENTS.md`.

The agent reads `AGENTS.md` at the start of every session, so it learns that these documents exist. 
It doesn't read them immediately, only when it's actually needed for the task.

In `AGENTS.md` we list them like this:

```markdown
Documents

- `_docs/plan.md` - what we are building
- `_docs/process.md` - how work moves through the project
- Before writing tests, read `_docs/testing-guidelines.md`
- For anything touching the UI, read `_docs/design-system.md`
```

The agent then opens the document relevant to the task:

- A task about the UI pulls in the design system.
- A task about tests pulls in the testing guidelines.

This keeps `AGENTS.md` short while the project's written context keeps
growing.


[← Bootstrapping a Project](04-bootstrapping.md) | [Grooming a Task →](06-grooming-a-task.md)

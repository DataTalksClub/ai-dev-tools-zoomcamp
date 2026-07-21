# Context Engineering

Video: TBA

## Definition

**Context engineering** is the practice of making your project
understandable to an agent before the agent starts working.

It is not "writing better prompts". A prompt is one message in one
session. Context is everything that is true about the project every
time anyone opens it with any tool.

In practice it means four things: conventions are explicit instead of
inferred from whichever file the agent read first, commands are
discoverable, constraints are visible, and review criteria are
repeatable.

The point of all four is the same: you stop repeating yourself.

## Anything you explain twice belongs in a file

A session starts with no memory of the last one. The agent that
refactored your test suite yesterday does not know today that you use
`pytest` and not `unittest`, that the migrations live somewhere
unusual, or that you asked it three times not to comment every line.

So every session you pay the same tax: a few messages of setup, or a
few corrections after it does the wrong thing. The rule I use:

> If I have explained something to an agent more than twice, it goes
> in a file.

Writing it down costs five minutes once. Explaining it costs two
minutes every session, forever, and some sessions you will forget and
get the wrong thing instead.

## AGENTS.md

`AGENTS.md` is a plain Markdown file at the root of the repo
describing the project to any coding agent that opens it.

Be precise about what it is. It is a **convention that spread across
tools**, not a formal standard with a spec and a compliance test. Some
agents look for it and read it automatically, some read a different
filename, some need to be told about it. Support varies and it changes.

We use it anyway, for one reason: of all the options it is the most
portable. It is a normal Markdown file with a name several tools
already recognize, and any tool that does not recognize it can still
be pointed at it. Tools change fast, and you do not want your project
knowledge locked into the file format of whichever one you picked in
lesson 2.

## One source of truth

Claude Code reads `CLAUDE.md`. So if that is your tool, do not
maintain two files. Make `CLAUDE.md` one line long:

```markdown
@AGENTS.md
```

That imports `AGENTS.md`. One file holds the content, and a one-line
pointer sends the tool to it.

Other tools have their own instruction-file conventions, with their
own filenames and locations. The move is the same in each case: keep
the content in `AGENTS.md` and have the tool-specific file point at
it. Then switching tools, or two people on a team using different
tools, costs nothing.

## What belongs in it

Seven things, each of them short:

1. **What the project is** - one or two sentences
2. **How to run it** - the actual commands
3. **How to test it** - including how to run a single test
4. **The stack, and why** - the "why" stops the agent helpfully
   introducing a second HTTP client
5. **Conventions to follow** - the things you would comment on in
   review
6. **Constraints and things it must not do** - the most valuable
   section, and the one people forget
7. **Where the important code lives** - a short map, not a file
   listing

Here is a realistic one for the Snake game we have been using:

```markdown
# Snake

A browser Snake game built with React and Vite. Used as a teaching
example for this course, so readability beats cleverness.

## Commands

- `npm install` - install dependencies
- `npm run dev` - start the dev server
- `npm run build` - production build
- `npm run lint` - ESLint

## Stack

React 19, Vite 7, Tailwind CSS. No backend, no router, no state
management library. Keep it that way unless there is a real reason
not to.

## Layout

- `index.html` - Vite entry point
- `src/main.jsx` - mounts the React app
- `src/App.jsx` - app shell
- `src/components/SnakeGame.jsx` - the game itself: state, game loop,
  keyboard handling and rendering

## Conventions

- Function components with hooks. No class components
- Game state stays in the component that owns it
- Tailwind utility classes for styling. Do not add new CSS files

## Constraints

- There is no test suite. If you change how the game behaves, tell me
  what you changed and how I can check it by hand
- Do not add dependencies without asking
- Do not commit. Leave changes staged so I can review them
```

That is about thirty lines, and it answers most of what an agent would
otherwise guess wrong about. Everything in it is specific to this
project. None of it is generic advice about writing good code.

Look at the constraints section. "There is no test suite" is an
uncomfortable thing to write down, and it is the most useful line in
the file. It tells the agent it cannot prove its own work, which is
exactly what you want it to know. We come back to why in
[lesson 7](07-tests-and-verification.md).

## What does not belong in it

This is where beginners go wrong, and the failure always has the same
shape: the file grows until nobody, human or model, follows it.

Keep these out:

- **Transient task state.** "Currently working on the pause menu" is a
  session note, not a project fact. Stale within a day.
- **Anything secret.** Keys, tokens, internal URLs, customer names.
  This file is read by tools, copied into contexts and committed to
  git. Treat it as public.
- **Long prose.** Three paragraphs on your testing philosophy will not
  change what the agent does. One line saying "game logic goes in
  `SnakeGame.jsx`, not `App.jsx`" will.
- **Rules nobody enforces.** A rule that has been broken for six
  months with no consequence is a wish. Delete it or enforce it.

A lean file that gets followed beats a long one that gets skimmed.
Every line you add makes the other lines slightly less likely to be
noticed. That cost is invisible until the file is already too big. If
yours is drifting past a couple of screens, the signal is to cut, not
to add a table of contents.

## This is what lesson 3 was for

In lesson 3 you pointed an agent at an unfamiliar codebase, asked it
to explain the entry points, the layout, the conventions and the build
commands, then checked the answer. That output is the raw material for
this file. The map you built, the conventions you confirmed, the
commands you verified actually work: that is `AGENTS.md`, minus the
parts that turned out to be wrong. Reading a codebase and writing its
context file are the same activity in two directions.

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

- **Reusable commands and skills** - packaging a repeated workflow so
  you invoke it by name instead of describing it again
- **Permission modes** - deciding in advance what the agent may do
  without asking you
- **Hooks** - running your own checks automatically at fixed points in
  the agent's work

All three are covered properly in [Module 3](../../03-mcp/), and all
three are less useful than they sound if the base is missing. An agent
with elaborate hooks and no idea how to run your tests is not ahead of
one with a good `AGENTS.md`.

## Your deliverable

This is the artifact for this module. Before you move on:

1. Write `AGENTS.md` for your own project, using the seven headings
   above. Keep it under two screens.
2. Add a `CLAUDE.md` containing `@AGENTS.md`, or the equivalent
   pointer for your tool.
3. Start a fresh session, give the agent a small task, and watch what
   it still gets wrong. Those are your missing lines.

Step 3 is the one people skip, and it is the only one that tells you
whether the file works.

[← Specs Before Code](04-specs.md) | [Steering a Session →](06-steering-a-session.md)

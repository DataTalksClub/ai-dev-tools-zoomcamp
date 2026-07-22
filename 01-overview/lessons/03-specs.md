# Specs Before Code

Video: TBA

## The spec decides the outcome

You decide the quality of what an agent builds before it writes the
first line of code.

If a task is vague, the agent fills the gaps with its own assumptions.
The result will be far from what you imagined.

This gets worse as models get better. A weak agent that misunderstands
you writes fifty lines of broken code and you notice in a minute. A
strong agent that misunderstands you writes eight files and wires them
together. It adds tests that pass and gives you a working version of
the wrong thing. The more capable the agent, the further in the wrong
direction it goes before you notice it.

So you need to think in detail about what you want to build, and give
explicit instructions. Then the result will be close to what you want.

## Start in a chat assistant

Don't start your coding session with a coding agent. Coding agents write code, but you don't know what you want yet, so you'll only waste time and tokens.

Instead, open a chat assistant and talk the idea through. I use
dictation for this. It's faster than typing and it keeps me in the
mode of explaining rather than specifying.

In that conversation, cover:

- what the thing is
- who it's for
- what it should do
- what it shouldn't do
- what you're unsure about

Also ask it about what's already out there, so you don't spend a
weekend rebuilding something that exists.

As you progress through your session, you'll get a clearer vision of what you want to build.

At the end of the session, ask:

```text
Save this to a markdown file I can download.
```

That file is your spec.

This is how I built [SQLiteSearch](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight),
a small SQLite-backed search library. First it was a long chat
session to get the design straight. Then I downloaded the `plan.md` file, and started coding.

## Inside the spec

We write the spec once and keep it with the project.

Mine usually covers:

- what the project is, in a couple of sentences
- who it's for, and what they're trying to do
- what it doesn't do
- the stack, and the constraints it has to live inside
- a rough architecture: the main pieces and how they relate

The [`plan.md` for SQLiteSearch](https://github.com/alexeygrigorev/sqlitesearch/blob/main/plan.md)
had all five. It opened with what the library is, then a section on how
it differs from `minsearch`, the in-memory library it's a sibling to.
After that came explicit "when should you use this" and "when should
you not use this" sections, and it ended with the architecture.

## Two tiers

This approach has a name: spec-driven development.

You start with the specification, treat it as the canonical version,
and write the code from it.

There are two levels of specifications:

- Project-level - what the project is. We create it once and don't modify often.
- Feature-level - what a change should do and how you'll know it
  worked, written per task and thrown away after.

In my case the project level specs live in `plan.md`, `process.md` and `AGENTS.md`. I put these files in the `_docs` folder.

The feature level specs are tasks in a task tracking system. I usually use GitHub issues for that.


[← The Tool Map](02-tool-map.md) | [Bootstrapping a Project →](04-bootstrapping.md)

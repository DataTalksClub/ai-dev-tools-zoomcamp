# Specs Before Code

Video: TBA

## Why the spec decides the outcome

The quality of what an agent builds depends on the work you do before it writes
the first line of code.

If a task is vague, the agent will fill the gaps in the task with its own assumptions, and the result will be very different from what you imagined.

This gets worse as models get better. A weak agent that misunderstands
you writes fifty lines of broken code and you notice in a minute. A
strong agent that misunderstands you writes eight files, wires them
together, adds tests that pass, and hands you a working implementation
of the wrong thing. The more capable the agent, the further in the
wrong direction it goes before you notice it.

So you need to think in detail what exactly you want to build, and you 
need to give very explicit instuctions. Then the result will be close to 
what you want.

## Start in a chat assistant

Don't start your coding session with a coding agent. Coding agents write code, but you do not know what you want yet, so you will only waste time and tokens. 

Intead, open a chat assistant and talk the idea through. I use
dictation for this. It's faster than typing and it keeps me in the
mode of explaining rather than specifying.

Say what the thing is, who it is for, what it should do, what it shouldn't, and what you are unsure about.

Also ask it about what's already out there, so you do not spend a
weekend rebuilding something that exists.

As you progress thorugh your sessoin, you will get a more clear vision of what you want to build.

At the end of the session, ask:

```text
Save this to a markdown file I can download it.
```

That file is your spec.

This is how I built [SQLiteSearch](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight),
a small SQLite-backed search library. First it was a long chat
session to get the design straight. Then I donwloaded the `plan.md` file, and started coding. 

## What goes in it

The spec is the durable, project-level document.

Mine usually covers:

- what the project is, in a couple of sentences
- who it is for, and what they are trying to do
- what it does not do
- the stack, and the constraints it has to live inside
- a rough architecture: the main pieces and how they relate

The [`plan.md` for
SQLiteSearch](https://github.com/alexeygrigorev/sqlitesearch/blob/main/plan.md)
had all five. It opened with what the
library is, spent a section on how it differs from `minsearch` - the
in-memory library it is a sibling to - then had explicit "when should
you use this" and "when should you not use this" sections, and ended
with the architecture.

## Two tiers

This approach has a name: spec-driven development.

You start with the specification first, treat it as the source of
truth, and derive the implementation from it.

There are two levels of specifications:

- Project-level - what the project is. We create it once and don't modify often.
- Feature-level - what a change should do and how you will know it
  worked. Written per task, thrown away after. 

In my case the project level specs live in `plan.md`, `process.md` and `AGENTS.md`. I put these files in the `_docs` folder.

The feature level are task in a task tracking system. I usually use GitHub issues for that.  


[← The Tool Map](02-tool-map.md) | [Bootstrapping a Project →](04-bootstrapping.md)

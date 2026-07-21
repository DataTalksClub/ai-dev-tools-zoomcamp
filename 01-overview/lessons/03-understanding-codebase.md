# Understanding an Unfamiliar Codebase

Video: TBA

Most of the work you do as a developer happens in code somebody else
wrote. A new job, a new team, an inherited service, an open-source
project you want to contribute to - in all of those cases the first
task is not writing anything. It is figuring out what is already
there.

Reading code has always been slower than writing it. That is the part
AI tools changed most immediately, and it is the reason this lesson
comes before the ones about building things. Every later lesson
assumes you can reason about the repo in front of you. In a moment
you get handed a Snake codebase you did not write, and in
[Module 2](../../02-end-to-end/) you inherit more.

## The orientation questions

When you open an unfamiliar repo, you are trying to answer a small
fixed set of questions. They are the same questions every time. The
value of an agent here is that it can read the whole tree in the time
it takes you to read one file.

Ask them one at a time, not all at once. A single question gets you a
focused answer you can check. Seven questions at once get you an essay.

**What does this project do?**

```text
Read this repository and tell me what it does, in five sentences,
as if I am a developer who just joined the team.
```

**How is it structured?**

```text
Give me a directory tree of the main source folders and one line
per folder explaining what belongs in it.
```

**Where does execution start?**

```text
What is the entry point of this application? Trace what happens
from process start to the first thing a user sees.
```

This one matters more than it looks. Once you know where execution
begins, you can follow any behaviour by hand instead of asking about
it.

**How do I run it? How do I test it?**

```text
What are the exact commands to install dependencies, run this
locally, and run the tests? Tell me where you found each command.
```

Then actually run them. This is the cheapest verification in the whole
lesson: a wrong command fails in two seconds.

**Where does the important logic live?**

```text
Which files contain the core logic of this project, as opposed to
configuration, boilerplate and glue? Rank them by importance.
```

**What would I have to touch to change X?**

```text
If I wanted to add a pause button, which files would need to
change and why?
```

This is the question that turns understanding into work. Ask it before
you ask for the change itself. The answer tells you whether the agent
has the map right, and it costs nothing to correct at this stage.

## The exercise: two Snake games

This repository has two versions of the same game:

- [snake-chatgpt/](../snake-chatgpt/) - built by pasting code out of a
  chat window
- [snake-claude-code/](../snake-claude-code/) - built by a terminal
  agent working in the folder

Pick one and run the orientation questions above against it. Then run
them against the other.

Now the part that is genuinely worth doing:

```text
Compare the implementations in snake-chatgpt/ and
snake-claude-code/. Same game, two codebases. Describe how they
differ in structure: file layout, where state lives, how the game
loop is organized, and what each one leaves out.
```

A person doing that by hand needs to hold both codebases in their head
at once. It takes a while. An agent does it in one pass. This is the
shape of task where these tools earn their place - broad reading,
narrow conclusion.

Then open the files it points at and see whether you agree. You will
often disagree with part of it, and that part is the interesting one.

## Verification

Here is the thing to take away from this lesson.

An agent describing a codebase is generating plausible text about
code. Plausible is not the same as true. It has read some of the
files, some of the time, and the summary reads exactly the same
whether it read them or not. Confidence in the output tells you
nothing about whether it looked.

So build habits that force the claims back onto the code.

**Ask for citations.** Make every claim carry a file path and a line
range:

```text
For each claim, cite the file and line range it comes from.
```

Then open two or three of them. Not all - the point is spot-checking,
not re-doing the work. If the citations are real and say what the
summary says, the rest is probably fine. If one is a file that does
not exist, throw the whole answer away and start again.

**Ask how it knows.** When something sounds important:

```text
How do you know that? Which file did you read?
```

The answer separates "I read it" from "that is how projects like this
usually work". Both are useful, but you need to know which one you
got.

**Check what you are about to build on.** You do not have to verify
everything. Verify the claims that the next hour of work depends on.
If the agent says all database access goes through one module and you
are about to add a query, that claim is load-bearing. Check it. If it
says the project has 14 files and it has 15, let it go.

**Be most suspicious of confident summaries of code the agent never
opened.** Large repos, deep directories, generated code, anything
behind a build step. Ask which files it actually read before you
believe a summary of them.

## The failure mode worth naming

The specific way this goes wrong is worth a name, because you will see
it repeatedly:

> The agent describes the architecture the project *ought* to have,
> not the one it has.

Models have read an enormous amount of well-organized code. When a
real repo is messier than that - a service layer that only half
exists, business logic in a route handler, a config file nobody has
loaded since 2023 - the tidy version is a much more likely-looking
piece of text than the actual one.

So you get a description of a clean layered architecture, and it is
wrong in the exact way that matters: it is missing the mess, and the
mess is where the bugs live.

The tell is usually vagueness at the boundary. Crisp language about
layers and responsibilities, no file paths. Ask for the paths.

## This is what goes in AGENTS.md

Everything you just worked out - what the project does, how it is laid
out, how to run it, how to test it, where the real logic lives - is
exactly the content of an `AGENTS.md` file. That is the deliverable
for this module, and we build it properly in
[lesson 5](05-context-engineering.md).

So do not throw this away. Take notes as you go. Orienting yourself in
a repo and briefing an agent about a repo are the same activity done
once.

## Beyond toy repos

The technique scales up, and it is most valuable where it is hardest to
do by hand.

Before contributing to a large open-source project, clone it and run
the same questions. Where is the entry point, how do I run the tests,
which module owns the thing I want to change, where are the
contribution rules written down. That is an afternoon of reading
compressed into a session, and it gets you to the point where you can
ask a sensible question in the issue tracker.

The verification habits matter more there, not less. A big repo has
more places for a plausible wrong answer to hide.

Next: now that you can read a codebase, what to write down before you
let anything change it.

[← The Tool Map](02-tool-map.md) | [Specs Before Code →](04-specs.md)

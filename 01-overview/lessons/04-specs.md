# Specs Before Code

Video: TBA

## The claim

let's avoid generic titles and be specific about what we cover

The quality of what an agent builds is mostly decided before it writes
a line of code.


describe my process. take my sqlitesearch article - and describe the process from there

it's 

- talk to chat assistant first to be clear what you want to produce 
- create a clear specification
- produce a md file 
- put it inside an empty folder 
- ask the coding agent to read it and decompose it into tasks 
- create tasks with acceptance criteria  (take them from my article about coding agents)
- start executing it (loop with /goal)

let's do that: first you describe this workflow, then we have a lesson progression like that (so multiple lessons)

- specs for creating the specs 
- bootstraping the project folder
- context engineering - what it is 
- implement one task 
- test the task
- loop engineering (/goal) 
- graph engineering (define two agents and loop through the backlog)

what we want to have in the end: 
start a fresh session, launch 
/goal work though the backlog
and it will know what to do 


let's rework the rest of the module with this plan in mind and rearrange files.


A vague ask does not produce a vague answer - it
produces a confident, detailed, plausible answer to a question you did
not ask. The agent fills the gaps you left with its own assumptions,
and it does not flag them. It just builds.

The uncomfortable part is that this gets worse as models get better. A
weak agent that misunderstands you writes fifty lines of broken code
and you notice in a minute. A strong agent that misunderstands you
writes eight files, wires them together, adds tests that pass, and
hands you a working implementation of the wrong thing. The more capable
the agent, the further in the wrong direction it travels before anyone
notices.

So the leverage is not in prompting harder mid-session. It is in what
you wrote down before the session started.

## Spec-driven development

Through 2026 this settled into a named practice: spec-driven
development. Write the specification first, treat it as the source of
truth, and derive the implementation from it rather than the other way
round.



Tier 1: the durable project document. What the project is, who it
is for, what stack it uses, what constraints it operates under, what it
deliberately does not do. This is written once, changes rarely, and
applies to every piece of work in the repo. Some tools and courses call
this a *constitution*. Others call it a product spec, steering docs, or
project rules.

Tier 2: the per-feature spec. What this one change should do, how
you will know it worked, and what it must not touch. It is written
before the change, used during the change, and retired after the change
lands. It is disposable by design.

```text
tier 1   project-level     rarely changes    applies to all work
tier 2   feature-level     written per task  thrown away after
```

in our case, project-level would be instructions in process.md and agents.md, and feature-level will be stored in GitHub issues.


## Plan, implement, validate

The cycle around a feature spec has three steps:

```text
plan       agree on what should happen, before any edits
implement  the agent writes the code
validate   check the result against what was agreed
```

Validation has to be a gate, not a summary. An agent will tell you it
is done - the feature works, the tests pass, everything is wired up.
That is a claim, not evidence. Work is done when it meets the criteria
you wrote down before it started, not when the agent announces that it
is.

This is also why the criteria have to exist *before* implementation. If
you write them afterwards you will write them to match what was built -
everyone does. Writing them first is what makes them a test rather than
a description. We go deeper on the mechanics of checking in [lesson
7](07-tests-and-verification.md).

## What goes in a small feature spec

Four things. That is genuinely all.

1. Goal - one or two sentences on what should be true afterwards.
2. Acceptance criteria - checkable statements. Not "works well" but
   things where you can point at the screen and say yes or no.
3. Out of scope - what this change must not do.
4. Constraints - files it should stay inside, libraries it may not
   add, patterns it must follow.

If it takes more than a few minutes to write, the task is too big.
Split it.

## A worked example

Take the Snake game we use throughout this module and add a pause
control. Here is the whole spec:

```markdown
# Feature: pause

## Goal
The player can pause and resume the game with the spacebar.

## Acceptance criteria
- Pressing space during play freezes the snake and stops the timer
- Pressing space again resumes from exactly the same state
- The word PAUSED is visible on screen while paused
- Arrow keys do nothing while paused
- Pressing space before the game starts does nothing

## Out of scope
- No pause button in the UI, keyboard only
- No pause menu, no settings, no restart option
- Do not touch scoring or collision logic

## Constraints
- Existing input handling only, do not add a library
- Changes stay in the game loop and input files
```

Fifteen lines. Two minutes to write.

Notice what those acceptance criteria buy you. "Resumes from exactly
the same state" rules out the common bug where the snake jumps a cell
on resume. "Arrow keys do nothing while paused" rules out the version
where you queue up three turns while paused and die instantly on
resume. Neither of those is obvious from "add a pause feature", and
both are things you would otherwise only discover by playing. That is
the real function of acceptance criteria: they make you think about the
edges for two minutes, which is two minutes more than the agent will.

## Non-goals deserve their own section

Telling an agent what *not* to do is unusually effective, and almost
nobody thinks to do it.

Left to itself, an agent asked to add a pause control will reasonably
decide that the game could also use a settings panel, that the input
handling would be cleaner as a state machine, and that while it is in
there it may as well reformat the file. Every one of those decisions is
defensible. Together they turn a fifteen-line change into a four-file
diff you now have to review.

Useful non-goals are specific:

- No new dependencies
- Do not change the existing save format
- Do not refactor anything you are not directly editing
- Do not touch the tests for other features

A one-line non-goal saves you a long review. Relative to how long it
takes to write, this is the highest-return thing in the lesson.

## Where I got this wrong

The strongest argument for any of this is a project where I skipped it.

I had wanted to rewrite Jekyll in Rust for months, and earlier this
year I finally started - a project called
[Rustkyll](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software).
I had a working multi-agent setup at that point, with a requirements
step built into the process. I skipped it. I pointed the agents at the
DataTalks.Club website and effectively said: reimplement this in Rust.

The next day I looked at what they had built. It worked. It rendered
our site correctly. And it was tailored to our site - the agents had
been optimizing against the one example I gave them, so the
implementation had quietly grown around the specific features, layouts
and plugins that DataTalks.Club happens to use. It was not a Jekyll
engine. It was a DataTalks.Club engine that resembled one.

No agent misbehaved. They did what I asked. The word "general" was
never in the requirements because there were no requirements. I had to
stop, go back, tell them to find other Jekyll sites, and make it work
across all of them - a correction that cost far more than the
requirements step I skipped would have.

The lesson is narrower than "write specs". It is that the assumptions
you do not write down are the ones the agent gets to make for you. It
has to pick something, and it picked "like the example I was shown",
because that was the only signal available.

## The boundary with Module 2

This lesson is about specifying a *small change in a codebase that
already exists*. One feature, one spec, written in a couple of minutes,
retired when the change lands.

The full product spec - what the whole application is, its users, its
data model, its screens, its deployment - belongs to [Module
2](../../02-end-to-end/), where you build and ship a complete app. Do
not attempt that treatment here. The skill you want out of this lesson
is the small one, practiced often.

## Try it

Pick the next change you plan to make and write the four sections
first: goal, acceptance criteria, out of scope, constraints. Then hand
it over, and compare the review time against what usually happens when
you just ask.

Next: how to get the right information in front of the agent in the
first place.

[← Understanding an Unfamiliar Codebase](03-understanding-codebase.md) | [Context Engineering →](05-context-engineering.md)

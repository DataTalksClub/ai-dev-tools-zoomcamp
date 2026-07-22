# Introduction

Video: TBA

In this module we work with AI developer tools in a way you can defend
later.

Tools change every month, but the way you work with them lasts. You
give a tool context before it starts, steer it while it runs, and check
what came back.

Before you start, go through the course documentation:

- [Zoomcamp Logistics](https://datatalks.club/docs/courses/zoomcamp-logistics/)
- [AI Dev Tools Zoomcamp](https://datatalks.club/docs/courses/ai-dev-tools-zoomcamp/)

Places where you can find me:

- [My substack](https://alexeyondata.substack.com/)
- [LinkedIn](https://www.linkedin.com/in/agrigorev/)
- [X](https://x.com/Al_Grigor)

## Not vibe coding

In the previous edition, we called the first module "Introduction to Vibe Coding".
Nowadays, "vibe coding" means that you describe what you
want, accept whatever the model produces, and never read it.

This year we call it the "AI-native developer workflow". We show how to
use AI tools with context, constraints, and verification.

## The workflow

The difference between the two isn't how much AI you use. You can
delegate almost everything - the typing, the tests, the refactor, the
commit message. That's fine, and this module does exactly that.

We specify the work before it starts and check it when it ends.

Over the module we build these steps:

- Brainstorm - work out what you actually want
- Specs - write it down, concretely
- Decompose - turn the spec into a backlog of tasks
- Implement - one task at a time
- Verify - a separate session checks the work
- Loop - `/goal` works through the backlog

By the end you can open a fresh session in your project, type `/goal
work through the backlog`, and watch the agent do its work.

The agent will:

- read `AGENTS.md` to learn how to run and test the project
- take the next open task from the backlog
- implement it against the acceptance criteria
- run the tests, and fix the code if something breaks
- send the result to a QA agent for validation
- commit, close the task, and pick up the next one
- stop when the backlog is empty


## You become an agent manager

When writing code, typing is no longer the bottleneck. Deciding what to
build and confirming it was built correctly is.

As a developer, your role moves toward a manager of a fast junior developer who never gets tired. You tell it what to do, you watch it work, check the output, send it back when it's wrong.

## The lessons

We work through the rest of the module in ten lessons:

- [The tool map](02-tool-map.md) - what an agent is, the five
  categories, and picking yours for the cohort
- [Specs before code](03-specs.md) - talking a design through, then
  writing it down
- [Bootstrapping a project](04-bootstrapping.md) - a spec into an empty
  folder, decomposed into a backlog
- [Context engineering](05-context-engineering.md) - what the agent
  knows before it starts
- [Grooming a task](06-grooming-a-task.md) - raw task to acceptance
  criteria, as the PM
- [Implementing a task](07-implementing-a-task.md) - writing the code,
  as the engineer
- [Testing a task](08-testing-a-task.md) - checking the work, as the QA
  engineer
- [Loop engineering](09-loop-engineering.md) - `/goal`, and running the
  agent repeatedly
- [Graph engineering](10-graph-engineering.md) - the three roles as
  agents, working the backlog
- [Wrap-up](11-wrap-up.md) - what transfers when the tools change again

We stay at the fundamentals level here, and the next modules build on
that:

- in [Module 2](../../02-end-to-end/) we build an app end to end
- in [Module 3](../../03-mcp/) we discuss more advanced topics like MCP, skills, hooks, subagents, and plugins


## The running example

Throughout the module we build a meeting cost calculator.

Meetings in the company have taken over the calendar, and nobody
notices because a meeting feels free. So we put a number on it. You add
the people in the room with their salaries, start the timer, and watch
what the meeting costs while it runs. Put it on the screen in the room
and let it argue on your behalf.

It's a good teaching app. It's small enough to hold in your head, and
you can see whether it works in a second.

The core still needs a real spec:

- turning salaries into a per-second rate
- accruing cost over time
- pausing without losing the total

You build it yourself over the module, starting from a spec in an empty
folder in [lesson 4](04-bootstrapping.md). There's no version in this
repo to copy. You learn the process that produces it, and you can only
see that by running it.


## Prerequisites

You should be able to program in some language, any language, well
enough to read code and tell when something looks wrong. You also need
a computer where you can install things and use a terminal.

No prior AI experience is required. If you've never used a coding agent
before, this module is exactly where to start.


[← Back to module](../) | [The Tool Map →](02-tool-map.md)

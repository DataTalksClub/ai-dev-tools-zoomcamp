# Introduction

Video: TBA

This module is about working with AI developer tools in a way you can
defend later.

Tools change
every month. What lasts is the workflow: what you give a tool before it
starts, how you steer it while it runs, and how you check what came
back.

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
want, accept whatever the model produces, and never really read it.

This year, we name it "AI-native developer workflow": we show how to use AI tools
with context, constraints, and verification.

## The workflow

The difference between the two is not how much AI you use. You can
delegate almost everything - the typing, the tests, the refactor, the
commit message. That is fine, and this module does exactly that.

The difference is that the work gets specified before it starts and
checked when it ends. Here is the loop we build over the module:

- Brainstorm - work out what you actually want
- Specs - write it down, concretely
- Decompose - turn the spec into a backlog of tasks
- Implement - one task at a time
- Verify - a separate session checks the work
- Loop - `/goal` works through the backlog

The end state is a project where you can open a fresh session, type
`/goal work through the backlog`, and watch the agent do its work.

It will:

- read `AGENTS.md` and learn how to run and test the project
- take the next open task from the backlog
- implement it against the acceptance criteria
- run the tests, and fix the code if something breaks
- hand the result to a QA agent for validation
- commit, close the task, and pick up the next one
- stop when the backlog is empty


## You become an agent manager

When writng code, typing is no longer the bottleneck.
But deciding what should be built and confirming that it was built correctly is.

As a developer, your role moves toward a manager of a very fast junior developer who never gets tired. You tell it what to do, you watch it work, check the output, send it back when it's wrong.

## What we cover

| Lesson | |
|---|---|
| 2. [The tool map](02-tool-map.md) | What an agent is, the five categories, and picking yours for the cohort |
| 3. [Specs before code](03-specs.md) | Talking a design through, then writing it down |
| 4. [Bootstrapping a project](04-bootstrapping.md) | Spec into an empty folder, decomposed into a backlog |
| 5. [Context engineering](05-context-engineering.md) | What the agent knows before it starts |
| 6. [Grooming a task](06-grooming-a-task.md) | Raw task to acceptance criteria, as the PM |
| 7. [Implementing a task](07-implementing-a-task.md) | Writing the code, as the engineer |
| 8. [Testing a task](08-testing-a-task.md) | Checking the work, as the QA engineer |
| 9. [Loop engineering](09-loop-engineering.md) | `/goal`, and running the agent repeatedly |
| 10. [Graph engineering](10-graph-engineering.md) | The three roles as agents, working the backlog |
| 11. [Wrap-up](11-wrap-up.md) | What transfers when the tools change again |


We stay at the fundamentals level here and in the next modules we built upon that:

- in [Module 2](../../02-end-to-end/) we build an app end to end
- in [Module 3](../../03-mcp/) we discuss more advanced topics like MCP, skills, hooks, subagents, and plugins


## The running example

Throughout the module we build a meeting cost calculator.

The premise is that meetings in the company have got out of hand, and
nobody notices because a meeting feels free. So we put a number on it:
add the people in the room with their salaries, start the timer, and
watch what the meeting costs while it runs. Put it on the screen in the
room and let it argue on your behalf.

It is a good teaching app. It is small enough to hold in your head, you
can see whether it works in a second, and it has a real core worth
specifying: turning salaries into a per-second rate, accruing cost over
time, and pausing without losing the total.

You build it yourself over the module, starting from a spec in an empty
folder in [lesson 4](04-bootstrapping.md). There is no version in this
repo to copy - the point is the process that produces it, and you can
only see that by running it.


## What you need to know

Very little. You should be able to program in some language - any
language - well enough to read code and tell when something looks
wrong. You need a computer where you can install things and use a
terminal.

No prior AI experience is required. If you've never used a coding agent
before, this module is exactly where to start. 


[← Back to module](../) | [The Tool Map →](02-tool-map.md)

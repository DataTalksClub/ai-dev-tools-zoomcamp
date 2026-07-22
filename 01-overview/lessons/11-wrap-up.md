# Wrap-up

Video: TBA

## The files you built

You didn't only build the meeting cost calculator, you built the
structure around it:

```text
_docs/plan.md            what the project is, and what it is not
_docs/process.md         how work moves through it
AGENTS.md                how to run it, the rules, and what to read when
team/pm.md               how a task gets groomed
team/software-engineer.md how it gets implemented
team/qa-engineer.md      how it gets verified
team/task-template.md    the shape of a groomed issue
GitHub issues            the backlog
```

Seven files and a backlog. You added every one of them because a
session needed it, and together they let you type one command and walk
away.

## The arc

Each lesson set up the one after it:

- [Lesson 2](02-tool-map.md) - what an agent is, the five categories,
  the harness behind them, and picking one tool
- [Lesson 3](03-specs.md) - talk the idea through in a chat assistant,
  then write the spec
- [Lesson 4](04-bootstrapping.md) - putting the spec in an empty folder
  and decomposing it into a backlog
- [Lesson 5](05-context-engineering.md) - what an agent knows before it
  starts, and which documents it opens when
- [Lesson 6](06-grooming-a-task.md) - raw task to acceptance criteria
- [Lesson 7](07-implementing-a-task.md) - implementing against those
  criteria without changing them
- [Lesson 8](08-testing-a-task.md) - checking the work from a session
  that didn't write it
- [Lesson 9](09-loop-engineering.md) - running the agent repeatedly,
  with a stop condition a machine can evaluate
- [Lesson 10](10-graph-engineering.md) - the roles as agents, and the
  orchestrator that dispatches them

Read that list backwards and it's one argument. The loop only works
because QA outputs PASS or FAIL. QA can only do that because the issue
has checkable acceptance criteria. The issue has those because grooming
is its own step. Grooming is possible because there's a spec to groom
against.

Take out any one step and the ones after it stop working.

## You delegate the typing, not the responsibility

"The AI wrote it" isn't a defence, any more than "I copied it off
Stack Overflow" ever was. The code is in your repo, with your name on
the commit.

Keep this test in mind:

> If you cannot explain a change in review, you are not finished with
> it, however well it works.

You don't need it line by line, only what it does, why it does it that
way, and what breaks if it's wrong. That's a low bar, and a surprising
amount of AI-assisted work fails it.

## Areas to slow down

Some areas get read carefully regardless of how good the acceptance
criteria looked:

- Authentication and authorization
- Secrets, tokens, credentials, anything near `.env`
- Payments and billing
- Anything that deletes or migrates data
- CI configuration and workflow files
- Deployment, infrastructure, access permissions

In all of these, the cost of being wrong has nothing to do with the
size of the change. A one-line edit to a permission check is one line.
It's also the whole security model of your application.

In these areas, ask for a plan first, keep the changes small, and don't
point an unattended loop at them. That's the rule from [lesson
9](09-loop-engineering.md) seen from the other side. You can delegate
as far as your checks reach, and here they don't reach far.

## The homework

[Build a Django TODO app](../../cohorts/2026/01-overview/homework.md)
with the tool you picked in lesson 2.

You don't need to know Django. That's the point: you can't check the
result by recognising it, so you have to check it the other ways. Run
it. Make it tested. Ask the agent to explain the parts you don't
recognise, and read the files it points at.

Finish it, and be able to explain what each part of the app does.

## Next modules

Two modules follow this one:

- [Module 2](../../02-end-to-end/) builds and ships a full-stack
  application end to end, with these habits applied to something bigger
- [Module 3](../../03-mcp/) goes deep on the machinery we only named
  here - MCP and skills, hooks and subagents, plugins and custom agents

## The parts that transfer

Some of the tools named in this module will have changed by the end of
this course, and one or two won't exist. That's not a problem with
the module. It's why we built it this way.

What lasts is smaller and duller than any product:

- Specify before building
- Give durable context instead of repeating yourself
- Verify with something that didn't do the work
- Keep the judgment, delegate the typing

That works with a coding agent, with a colleague, and with whatever
ships next year. Everything else is an interface over it.

See you in Module 2.

[← Graph Engineering](10-graph-engineering.md) | [Back to module →](../)

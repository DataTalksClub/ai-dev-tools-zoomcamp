# Module 1 — AI-Native Developer Workflow

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what
> we are preparing, but the final videos, exercises, homework, and
> requirements may change before the cohort starts.

This module is about working with AI developer tools in a way you can
defend later.

Tools change every month. What lasts is the workflow: what you give a
tool before it starts, how you steer it while it runs, and how you check
what came back. We call this an **AI-native developer workflow** - using
AI tools with context, constraints, verification, and human review.

By the end of the module you should be able to answer three questions
about any change that lands in your repo: what you asked for, what
actually changed, and how you know it works.

## Lessons

**The map.** Where the tools sit and which one you'll use.

1. [Introduction](lessons/01-intro.md) - What this module is for and how
   it's organized
2. [The Tool Map](lessons/02-tool-map.md) - Five categories of AI
   developer tools, how to place a new one, and picking yours for the
   cohort

**The working practices.** The core of the module, in the order you hit
them on real work.

3. [Understanding an Unfamiliar Codebase](lessons/03-understanding-codebase.md) -
   Using an agent to get oriented, and verifying what it tells you
4. [Specs Before Code](lessons/04-specs.md) - Deciding what you want
   before anything is built
5. [Context Engineering](lessons/05-context-engineering.md) - Writing the
   `AGENTS.md` that every session starts from
6. [Steering a Session](lessons/06-steering-a-session.md) - Plans, small
   steps, course-correcting, and knowing when to stop
7. [Tests and Verification](lessons/07-tests-and-verification.md) - What
   you can check automatically, and why that sets your limit

**The vocabulary.** Terms you'll meet in blog posts and on X, usually
without a definition attached.

8. [Loop Engineering](lessons/08-loop-engineering.md) - Running one agent
   repeatedly against a check
9. [Graph Engineering](lessons/09-graph-engineering.md) - Splitting work
   across several agents with defined roles

**Closing.**

10. [Judgment and Wrap-up](lessons/10-wrap-up.md) - When to ask, when to
    inspect, when to simplify, and what transfers

## What you'll produce

One artifact:

```text
AGENTS.md    project context that any agent reads
CLAUDE.md    one line: @AGENTS.md
```

We build it in lesson 5 and refine it as the module goes. There are no
reports or comparison documents to write.

## Scope

This is the fundamentals module. Agent capabilities proper - MCP, skills,
hooks, subagents, plugins and custom agents - are
[Module 3](../03-mcp/). Building and shipping a full-stack app is
[Module 2](../02-end-to-end/).

## Homework

- [2026 Homework](../cohorts/2026/01-overview/homework.md) - Build a
  Django TODO app with the AI tool of your choice. You don't need to know
  Django.

## Previous Cohort Materials

The 2025 version of this module was a fuller tour of the tool landscape.
The specific tools it names have moved on, but the categories still hold,
so it's worth reading for the shape of each category rather than for the
product list.

- [2025 archived Module 1](../cohorts/2025/01-overview/)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

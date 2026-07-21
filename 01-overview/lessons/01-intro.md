# Introduction

Video: TBA

This module is about working with AI developer tools in a way you can
defend later.

Not "here are twenty tools and what their buttons do". Tools change
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

You have probably seen the term "vibe coding": you describe what you
want, accept whatever the model produces, and never really read it.
It's a real cultural moment and it's genuinely fun. It also falls apart
the moment the code has to be maintained, reviewed, or run in front of
other people.

What we teach here is the same speed with a different discipline. The
name we use for it is **AI-native developer workflow**: use AI tools
with context, constraints, verification, and human review.

## The three questions

The difference between the two is not how much AI you use. You can
delegate almost everything - the typing, the tests, the refactor, the
commit message. That is fine.

The difference is whether you can answer three questions about any
change that lands in your repo:

1. **What did I ask for?**
2. **What actually changed?**
3. **How do I know it works?**

If you can answer all three, it does not matter that a model wrote the
code. If you cannot, it does not matter that you wrote it yourself.

Almost everything in this module is one of those three questions in
more detail. Specs and context are question one. Reading diffs and
steering a session are question two. Tests and verification are
question three.

## You become an agent manager

There's a shift underneath this that's worth naming early.

When AI tools were autocomplete, your job was still typing. Now a
single instruction can produce a plan, twelve file edits and a test
run. The typing is no longer the bottleneck. Deciding what should be
built and confirming that it was built correctly is.

So your role moves toward something closer to a manager of a very fast,
very literal junior developer who never gets tired and never says "I'm
not sure". You brief it, you watch it work, you check the output, you
send it back when it's wrong.

That's not a metaphor about the future. It's how the rest of this
module is organized.

## What we cover

Ten lessons, in three groups.

**The map** - lesson 2. Five categories of AI developer tools: chat
assistants, terminal coding agents, agentic IDEs, cloud agents and
project bootstrappers. What each is good at, where each hurts, and how
to place a tool you've never seen before. You also pick the tool you'll
use for the rest of the course.

**The working practices** - lessons 3 to 7. This is the core of the
module, and it follows the order of real work:

| Lesson | Question it answers |
|---|---|
| 3. Understanding an unfamiliar codebase | Where am I? |
| 4. Specs before code | What am I asking for? |
| 5. Context engineering | What does the agent know before it starts? |
| 6. Steering a session | What do I do while it runs? |
| 7. Tests and verification | How do I know it works? |

These transfer to every tool in every category, including the ones that
don't exist yet.

**The vocabulary** - lessons 8 and 9. [Loop
engineering](08-loop-engineering.md) and [graph
engineering](09-graph-engineering.md). These are terms you will meet on
X and in blog posts, usually without a definition attached. They name
real practices: running one agent repeatedly against a check, and
splitting work across several agents with defined roles. You should be
able to say what they mean and judge whether your repo is ready for
either.

Lesson 10 closes with judgment: when to reach for an agent, when to
write it yourself, and what stays true when the tools change again.

We stay at the fundamentals level here. Agent capabilities proper -
MCP, skills, hooks, subagents, plugins - are [Module
3](../../03-mcp/). Building and shipping a real app end to end is
[Module 2](../../02-end-to-end/).

## The running example

Throughout the module we use a small Snake game. It's a good teaching
app: you can see it working or not working in a second, it's small
enough to read end to end, and it still has real parts - game logic,
rendering, state, tests.

This repository has two versions of it, both generated during the
previous cohort:

- [snake-chatgpt/](../snake-chatgpt/) - built by pasting code out of a
  chat window
- [snake-claude-code/](../snake-claude-code/) - built by a terminal
  agent working directly in the folder

Same game, two very different workflows. Open both when you get to
lesson 2 - the difference between them is the whole point of the tool
map.

In [Module 2](../../02-end-to-end/) this game grows into a full-stack
app with a backend, a database and a deployment. The habits you build
here are the habits you'll use for the rest of the course.

## What you produce

One thing:

```text
AGENTS.md    project context that any agent reads
CLAUDE.md    one line: @AGENTS.md
```

`AGENTS.md` is where you write down what your project is, how to run
it, how to test it, and what an agent should not do. Most tools read it
directly. Claude Code reads `CLAUDE.md`, so the one-line file imports
the same content instead of duplicating it.

That's the deliverable. No reports, no comparison documents. We build
it up over lesson 5 and refine it as the module goes.

The [homework](../../cohorts/2026/01-overview/homework.md) is separate:
you build a Django TODO app with the AI tool of your choice.

## What you need to know

Very little. You should be able to program in some language - any
language - well enough to read code and tell when something looks
wrong. You need a computer where you can install things and use a
terminal.

No prior AI experience is required. If you've never used a coding agent
before, this module is exactly where to start. And you do not need to
know Django for the homework. That's rather the point of it.

[← Back to module](../) | [The Tool Map →](02-tool-map.md)

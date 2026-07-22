# Graph Engineering

Video: TBA

We already have three roles and a way to run tasks in a loop.

But we're still moving manually between roles. You read the QA verdict and decide whether it goes back to the engineer or you pick up the next task.

Now we'll automate it.

## The definition

Graph engineering is structuring work across several specialized
agents. You define what each one is responsible for, what order the
work moves in, and how they pass results along.

You can draw any such workflow as a graph. Each agent is a node, each
handoff is an edge, and the design work is in the structure rather than
in any single agent's behaviour.

The term appeared on X around 18 July 2026, a month after loop
engineering.

> Loop Engineering Is Dead ...

TODO - screenshots of the X thread

To me this definition makes little sense as a new idea. People have
been building multi-agent systems and state machines for a long time,
and specialized workers passing work between them isn't new.

In the
same discussion, people who build agent-orchestration tools said the
term was being used loosely, and they were right.

Loop engineering is actually not dead, because we still need a way to run our tasks. But on top of that, we add roles.

## You already built the graph

What we built so far is already a graph:

```text
groom (PM)  ->  implement (engineer)  ->  test (QA)  ->  done
                       ^                        |
                       +--------- FAIL ---------+
```

Three nodes and four edges, including the one that sends failed work
back for another pass. That's a graph, and you drew it without needing
the term.

- Each role has a file saying what it does and doesn't do
- Each role has a definition of done
- The handoff is the issue, not a conversation
- One role's output is another role's input, and the FAIL edge exists

In our case, the issue has all the context, so we can easily start
each node as a separate session.

## The orchestrator

One thing we're still missing is the orchestrator, which so far has
been you. Something has to pick the next issue, dispatch each role in
order, read the verdict, and route on it.

We make the main session do it, so it dispatches the roles rather than
doing the work.

Let's update our orchestrator:

```markdown
Lifecycle

1. Orchestrator picks the next open issue from the backlog
2. PM grooms it, following `team/pm.md`
3. Engineer implements it, following `team/software-engineer.md`
4. QA verifies it, following `team/qa-engineer.md`
5. On FAIL, back to step 3 with the QA comment as input
6. On PASS, commit and close the issue
7. Repeat until the backlog is empty

The orchestrator does not groom, implement or test. It dispatches.
Do not skip step 2, even when the task looks obvious.

The main session is the orchestrator and it launches PMs, SWEs and QAs
as subagents.
```

Now we're ready for our loop:


```text
/goal work through the backlog
```

The agent reads `AGENTS.md`, finds `process.md`, follows the lifecycle,
and dispatches the roles it finds in `team/`. Every piece of that
sentence is something you built in an earlier lesson.


So if someone asks you about graph engineering, you can say that it's
several agents with defined roles passing work to each other.

The term is from July 2026, but the practice is much older. It works
because the roles are explicit, the lifecycle is explicit, and the
specifications come before the implementation.

## Going further

You can learn about my own multi-agent setup here:

- [I Built an AI Agent Team for Software Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software)

It's the same three roles plus an on-call agent watching CI, running
across five real projects.

[← Loop Engineering](09-loop-engineering.md) | [Wrap-up →](11-wrap-up.md)

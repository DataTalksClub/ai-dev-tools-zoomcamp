# Graph Engineering

Video: TBA

We already have three roles and a way to execute tasks in a loop.

But we're still moving manually between roles: you read the QA verdict, decide if it goes back to the engineer or if you can pick up the next task.

Now we will automate it.

## The definition

Graph engineering is structuring work across several specialized
agents: what each one is responsible for, what order the work moves in,
and how they hand results to each other.

You can draw any such workflow as a graph. Each agent is a node, each
handoff is an edge, and the design work is in the structure rather than
in any single agent's behaviour.

The term appeared on X around 18 July 2026, a month after loop
engineering.

> Loop Engineering Is Dead ...

TODO: screenshots of the X thread

To me this definition makes very little sense as a new idea. People have
been building multi-agent systems and state machines for a long time,
and specialized workers passing work between them is not new.

In the
same discussion, people who build agent-orchestration tools said the
term was being used loosely, and they were right.

Loop engineering is actually not dead, because we still need a way to run our tasks. But on top of that, we add roles.

## You already built the graph

Let's see what we build so far. It's actually already a graph:

```text
groom (PM)  ->  implement (engineer)  ->  test (QA)  ->  done
                       ^                        |
                       +--------- FAIL ---------+
```

Three nodes and four edges, including the one that sends failed work
back for another pass. That is a graph, and you drew it without needing
the term.

- Each role has a file saying what it does and does not do
- Each role has a definition of done
- The handoff is the issue, not a conversation
- One role's output is another role's input, and the FAIL edge exists

In our case, the issue has all the context, so we can easily start 
each node as a separate section.

## The orchestrator

One thing we're still missing is the orchestrator. Previously we were doing it.  Something has to
pick the next issue, dispatch each role in order, read the verdict, and
route on it.

We make the main sessoin do it: it dispatches,
it does not do the work. 

Let's update our orchestartor:

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

The main session is the orhestrator and it launches PMs, SWEs and QAs
as subagents.
```

Now we're ready for our loop:


```text
/goal work through the backlog
```

The agent reads `AGENTS.md`, finds `process.md`, follows the lifecycle,
and dispatches the roles it finds in `team/`. Every piece of that
sentence is something you built in an earlier lesson.


So if now someone asks you about graph engineering, you can say: it is several
agents with defined roles handing work to each other, the term is from
July 2026, the practice is much older, and what makes it work is
explicit roles, an explicit process, and specifications written before
implementation.

## Going further

You can learn about my own multi-agent setup here:

- [I Built an AI Agent Team for Software
  Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software)

It is the same three roles plus an on-call agent watching CI, running
across five real projects.

[← Loop Engineering](09-loop-engineering.md) | [Wrap-up →](11-wrap-up.md)

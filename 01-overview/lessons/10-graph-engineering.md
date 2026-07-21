# Graph Engineering

Video: TBA

You have three roles and a loop. The one thing still done by hand is
moving work between them: you read the QA verdict, you decide it goes
back to the engineer, you start that session.

This lesson hands that over too.

## The definition

Graph engineering is structuring work across several specialized
agents: what each one is responsible for, what order the work moves in,
and how they hand results to each other.

You can draw any such workflow as a graph. Each agent is a node, each
handoff is an edge, and the design work is in the structure rather than
in any single agent's behaviour.

Where loop engineering asks "how does one agent keep working on its
own", graph engineering asks "who does what, and in what order".

## An honest note on the term

The name is from a post on X in July 2026 - roughly "are we still
talking loops, or did we shift to graphs yet?" - from the same person
who popularized loop engineering a month earlier.

To me the definition makes very little sense as a new idea. People have
been building multi-agent systems and state machines for a long time,
and specialized workers passing work between them is not new. In the
same discussion, people who build agent-orchestration tools said the
term was being used loosely, and they were right.

It is in this module because it is getting traction and you will meet
it. The technique underneath is genuinely useful. The word is just a
word.

## You already built the graph

Look at what lessons 6 to 8 produced:

```text
groom (PM)  ->  implement (engineer)  ->  test (QA)  ->  done
                       ^                        |
                       +--------- FAIL ---------+
```

Three nodes and four edges, including the one that sends failed work
back for another pass. That is a graph, and you drew it without needing
the term.

The parts that make it work are not exotic:

- Each role has a file saying what it does and does not do
- Each role has a definition of done
- The handoff is the issue, not a conversation
- One role's output is another role's input, and the FAIL edge exists

The last two matter most. Because the issue carries everything, no
agent needs another agent's context - which is what makes it possible
to run them as separate sessions at all.

## The orchestrator

The missing node is the one you have been playing. Something has to
pick the next issue, dispatch each role in order, read the verdict, and
route on it.

That becomes your main session, and its job is narrow: it dispatches,
it does not do the work. An orchestrator that gets impatient and
implements a small task itself has collapsed the graph back into one
agent grading its own homework.

Write the order down in `_docs/process.md` - the file that was three
lines in [lesson 5](05-context-engineering.md), and that I said would
grow when a second agent appeared. This is that moment:

```markdown
## Lifecycle

1. Orchestrator picks the next open issue from the backlog
2. PM grooms it, following `team/pm.md`
3. Engineer implements it, following `team/software-engineer.md`
4. QA verifies it, following `team/qa-engineer.md`
5. On FAIL, back to step 3 with the QA comment as input
6. On PASS, commit and close the issue
7. Repeat until the backlog is empty

The orchestrator does not groom, implement or test. It dispatches.
Do not skip step 2, even when the task looks obvious.
```

Then the command from [lesson 1](01-intro.md):

```text
/goal work through the backlog
```

The agent reads `AGENTS.md`, finds `process.md`, follows the lifecycle,
and dispatches the roles it finds in `team/`. Every piece of that
sentence is something you built in an earlier lesson.

## Subagents, worktrees and teams

Three mechanisms get described as "running agents in parallel", and
they are not the same thing:

| Mechanism | What it isolates | What it is for |
|---|---|---|
| Subagents | Context windows | Delegating a focused task and getting a result back |
| Git worktrees | Files on disk | Stopping parallel edits from colliding |
| Agent teams | Whole sessions | Agents that need to talk to each other |

For our pipeline, subagents are the relevant one: each role runs with
its own context and reports back. Worktrees matter as soon as two
issues are in flight at once, because two agents editing the same
checkout will overwrite each other. Agent teams are heavier and mostly
unnecessary here, because the issue is already the communication
channel.

Starting is not complicated - you ask:

```text
Review this branch with three subagents in parallel: one for security,
one for performance, one for test coverage. Wait for all three and
summarize what they found.
```

Try that once on real code. Seeing three reviews come back with
genuinely different findings is the fastest way to understand why
anyone bothers with roles. We build these properly in [Module
3](../../03-mcp/).

## What goes wrong

I ran this setup across five real projects before the term existed, and
wrote it up in [I Built an AI Agent Team for Software
Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software).
On the AI Shipping Labs website it processed 41 of 46 tasks overnight.
These are the things that actually broke:

**The process gets skipped.** The orchestrator sometimes launched the
engineer directly, without grooming - it ignored its own rules on the
tasks that looked small. That is why `process.md` above says not to.

**The agent stops and asks.** It pauses mid-workflow waiting for a
confirmation nobody is there to give, and the run is dead until you
come back. This is the same permissions problem from [lesson
7](07-implementing-a-task.md), and it is why unattended running needs
skip-permissions plus a contained environment.

**You cannot see inside.** A stuck subagent and a slow subagent look
identical from outside. With four running, this gets worse.

**Cost.** Several agents cost several times as much as one. A pipeline
that grooms, implements and verifies every task is three to four
sessions per issue.

And the one worth repeating: on Rustkyll I skipped the requirements
step, and the agents built something tailored to the single example I
gave them. The process failed at exactly the step this module keeps
coming back to - writing down what you want before anything builds it.
More agents did not save it. More agents made it faster.

## Loop or graph

- Loop when the work is a queue of similar things. Fix these twelve
  failing tests. Same job, many times.
- Graph when the work contains different kinds of thinking. Specify,
  build, verify. Different jobs, handed between.

A single-agent loop is simpler, cheaper and easier to debug. Reach for
roles when the work genuinely has them in it, not because it sounds
more advanced.

## What to take from this

If someone asks you about graph engineering, you can say: it is several
agents with defined roles handing work to each other, the term is from
July 2026, the practice is much older, and what makes it work is
explicit roles, an explicit process, and specifications written before
implementation.

That last sentence is this whole module, restated with more agents.

[← Loop Engineering](09-loop-engineering.md) | [Wrap-up →](11-wrap-up.md)

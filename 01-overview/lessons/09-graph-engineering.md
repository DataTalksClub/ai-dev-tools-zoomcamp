# Graph Engineering

Video: TBA

## Definition

**Graph engineering** is the practice of structuring work across several
specialized agents: defining what each agent is responsible for, what
order the work moves in, and how agents hand results to each other.

The name comes from the shape that produces. Each agent is a node. Each
handoff or dependency between them is an edge. The design work lives in
the structure connecting the agents, not in any single agent's behaviour.

Where loop engineering asks "how does one agent keep working on its own?",
graph engineering asks "who does what, and in what order?"

## Where the term came from

It started with a post on X in July 2026 - roughly "are we still talking
loops, or did we shift to graphs yet?" - from the same person who
popularized loop engineering a month earlier. It spread quickly.

The definition is still settling. In the same discussion, people who build
agent-orchestration tools noted that the term was being used loosely, and
others pointed out that specialized agents passing work between them
describes multi-agent systems and state machines, which are decades old.

Both observations are fair, and neither makes the technique less useful.
It's a new name for an older idea, and the idea works.

## The practice came before the name

In April 2026 - three months before anyone said "graph engineering" - I
wrote up a system I'd been running across five real projects:

- [I Built an AI Agent Team for Software Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software)

The setup was a small team of agents with fixed roles:

- **Product Manager** turns a raw task into a specification with user
  stories, acceptance criteria and test scenarios, and does the final
  acceptance review at the end
- **Software Engineer** implements the code and writes tests
- **QA** runs the tests, checks the acceptance criteria, and reports pass
  or fail with evidence
- **On-Call Engineer** watches CI and fixes failures

Work moves through them in a fixed order:

```text
PM grooming -> SWE implementation -> QA verification -> PM acceptance -> commit
                     ^                                       |
                     +--------------- rejected --------------+
```

That diagram is a graph. Four nodes, five edges, including the one that
sends rejected work back for another pass. Nobody called it graph
engineering at the time because the phrase didn't exist yet.

It worked. On one project, the AI Shipping Labs website, it processed 41
of 46 tasks overnight. Tasks ran in small parallel batches, and the
orchestrator pulled the next batch as the current one finished.

The point of showing you this isn't the specific roles. It's that the
useful part was never the vocabulary - it was having explicit roles, an
explicit process, and specifications written down before implementation
started.

## Why split the roles at all

This is the part worth understanding, because it's the reason the
structure helps rather than just adding overhead.

If one agent writes the code and then decides whether the code is
correct, it is grading its own homework. It has just spent its whole
context convincing itself that its approach was right, and it will bring
that conviction to the review.

Splitting the roles breaks that. QA is a different agent, with a different
context window, whose entire job is to check claims against evidence. The
PM acceptance step at the end catches a different class of problem again:
a feature can pass every test and still not be what was asked for.

You'll recognize this from lesson 7. Verification only means something
when it comes from somewhere the work didn't. Roles are one way to
guarantee that.

## Loop or graph?

Lesson 8 was about loops: one agent, iterating against a check, until a
stop condition. This lesson is about graphs: several agents, different
jobs, passing work along.

The rule of thumb:

- **Loop** when the work is a queue of similar things. Fix these twelve
  failing tests. Same job, many times.
- **Graph** when the work contains genuinely different kinds of thinking.
  Specify, build, verify, accept. Different jobs, handed between.

A loop with one worker is simpler, cheaper, and easier to debug. Reach for
the graph when the work actually has distinct roles in it - not because it
sounds more advanced.

## How this is built in practice

There are three separate mechanisms, and they get confused constantly
because all three are described as "running agents in parallel":

| Mechanism | What it isolates | What it's for |
|---|---|---|
| Git worktrees | Files on disk | Stopping parallel edits from colliding |
| Subagents | Context windows | Delegating a focused task, getting a result back |
| Agent teams | Whole sessions | Agents that need to talk to each other |

For this module, knowing the distinction is enough. Worktrees give each
agent its own checkout so they don't overwrite each other. Subagents keep
a side task's noise out of your main context. Agent teams are full
sessions that can message each other and share a task list.

In both Claude Code and Codex, the way you start is the same: you ask.
There is no special command to learn for the simple case.

```text
Review this branch with three subagents in parallel: one for security,
one for performance, one for test coverage. Wait for all three and
summarize what they found.
```

Both tools will split that into separate agents with their own context
windows and collect the results. In Codex, subagents are on by default
and you can switch between the running threads with `/agent` to watch
them work. Claude Code also has a heavier option, agent teams, where the
agents can message each other rather than only reporting back - that one
is experimental and off by default.

Try that prompt once. Seeing three reviews come back with genuinely
different findings is the fastest way to understand why anyone bothers
with this.

We build all three mechanisms properly in [Module 3](../../03-mcp/),
which is where subagents, hooks and agent capabilities live. Here, the
goal is that you know what the words mean and can tell which one someone
is talking about.

## What actually goes wrong

The write-up is honest about failure modes, and you'll hit all of these if
you try it:

- **The agent stops and asks.** Claude Code frequently paused mid-workflow
  waiting for confirmation instead of continuing.
- **You can't see inside.** There was no good visibility into what
  subagents were doing, which made a stuck agent hard to distinguish from
  a slow one.
- **The process gets skipped.** The orchestrator sometimes launched the
  engineer directly without the PM grooming step - it skipped its own
  rules.
- **Limits.** Usage limits ran out quickly. Several agents cost several
  times as much as one.

And the most instructive one: on Rustkyll, skipping the requirements phase
led the agents to tailor the implementation to specific sites instead of
building something general. The process failed at exactly the step this
module keeps returning to - writing down what you actually want before
letting anything build it.

## What to take from this

If someone asks you about graph engineering, you can now say: it's several
agents with defined roles handing work to each other, the term is from
July 2026, the practice is older, and the parts that make it work are
explicit roles, an explicit process, and specs written before
implementation.

That last sentence is the fundamentals of this whole module, restated with
more agents. The tooling changes fast. That doesn't.

[← Loop Engineering](08-loop-engineering.md) | [Judgment and Wrap-up →](10-wrap-up.md)

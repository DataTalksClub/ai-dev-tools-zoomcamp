# AI-Native Development: Specifications, Loop and Graph Engineering

This is the first article in a series based on
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

This year I wanted to do an experiment and publish a series of course notes as articles on Substack. My plan is to have one per module, and each one should be independent from others. I start with the first one: AI-native developer workflows.

Coding agents now write code faster than I can read it. 

When we give an agent a task, it can quickly implement it.
But if a task is vague, the agent fills the gaps with its own assumptions.
A weak agent that misunderstands us writes fifty lines of broken code. A strong
agent that misunderstands us creates eight files and wires them
together. It adds tests that pass and gives us a thing that works great,
but is not what we needed.

Typing is no longer the bottleneck. Saying precisely what we want, and
checking what came back, is.

In this article, I show how to make the request specific, so the agents
don't need to guess. Then we decompose the request into tasks, and assign each one to a team of agents: a product manager, a software engineer and a tester. 
Finally, we implement all the tasks in a backlog through a loop.

We cover topics like:

- Spec-driven development
- Context engineering
- Loop engineering
- Graph engineering


## Specs before code

We need to understand what we want to build before the agent produces
the first line of code. So we think it through in detail, and give
explicit instructions. If we do that, the result will be close to what
we want.

This approach has a name: spec-driven development. We start with the
specification, treat it as the canonical version, and write the code
from it.

There are two levels of specifications:

- Project-level - what the project is. We create it once and don't
  modify often.
- Feature-level - what a change should do and how we'll know it
  worked, written per task and thrown away after.

In my case the project level specs live in `plan.md`, `process.md` and
`AGENTS.md`, in a `_docs` folder. The feature level specs are tasks in
a task tracking system, usually GitHub issues.

## Start in a chat assistant

Don't start the coding session with a coding agent. Coding agents
write code, but we don't know what we want yet, so we'll only waste
time and tokens.

Instead, open a chat assistant and talk the idea through. I use ChatGPT in
dictation mode for this. It's faster than typing and it keeps me in the mode
of explaining rather than specifying.

In that conversation, cover:

- what the thing is
- who it's for
- what it should do
- what it shouldn't do
- what we're unsure about

Also ask it about what's already out there, so we don't spend a
weekend rebuilding something that exists.

As the session progresses, we get a clearer vision of what we want to
build. At the end, ask:

```text
Save this to a markdown file I can download.
```

That file is the spec. Mine usually covers:

- what the project is, in a couple of sentences
- who it's for, and what they're trying to do
- what it doesn't do
- the stack, and the constraints it has to live inside
- a rough architecture: the main pieces and how they relate

I describe this process in some detail in the
[SQLiteSearch](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight) article.

First, I had a long chat to get the design straight,
then I downloaded the
[`plan.md`](https://github.com/alexeygrigorev/sqlitesearch/blob/main/plan.md)
file and started coding.
It had all five sections - what the library is, how it
differs from [minsearch](https://alexeyondata.substack.com/p/minsearch-the-small-search-library),
when to use it, when not to, and the architecture.

## Bootstrapping a project

We have a spec, and now we turn it into a repo with a backlog the
agent can work through.

Make a folder, initialise git, and drop the spec in.

```bash
mkdir project-name && cd project-name
git init
mkdir _docs
mv ~/Downloads/plan.md _docs/plan.md
```

Open the coding agent in that folder.

If we didn't decide on the tech stack in the previous conversation, we need
to do it now.

If we don't have any tech stack in the plan, the agent will pick 
the technologies itself. Which is fine if we don't care how it's implemented,
but I'd still suggest to use something we're familiar with.

Let's do it:

```text
Read plan.md. Propose multiple options for the tech stack and explain each option.

Do not write any code yet.
```

Now break the plan into tasks:

```text
Propose a backlog of tasks. Create a document `tasks.md`

Each task should be small enough to finish in one session, and
independent enough that I could hand it to someone who has not read
the others.

Use this template for each task:

## <number>. <title>
Goal: <one line>
Description: <two or three sentences on what the task involves>

Make the first task setting up an empty project, with a
test that runs and passes.

Do not write any code yet.
```

Next, we review a few tasks ourselves. Check that they're granular enough
without being too granular, and that they make sense. We can merge
some tasks into bigger ones, split big ones into smaller tasks, or say
that some things are out of scope.

When the tasks are ready, save them in a task tracker. I usually use GitHub issues for this:

```text
Create a GitHub issue for each task.
```

For that to work, we need the `gh` CLI tool authenticated.

Now we can do the first task, the project init:

```text
Do task 1: set up an empty project on the chosen stack - the folder
layout, the dependencies, and one test that runs and passes. No
features yet.
```

From here on, every task starts from a project that already runs, so a
failing test means the task broke something rather than that nothing
exists yet.


## Context engineering

The repo has a backlog now, but the agent that works through it still
starts every session knowing nothing about the project.

Context engineering is the practice of making the project
understandable to an agent before the agent starts working. It's not
"writing better prompts". A prompt is one message in one session, while
context is everything the agent needs to know before it starts the
task.

We can help it by specifying these things in `AGENTS.md`, a plain
Markdown file at the root of the repo describing the project to any
coding agent that opens it. Agents read it at startup.

Note: Claude Code reads `CLAUDE.md`, not `AGENTS.md` like Codex and
most other tools do. I use multiple coding assistants, so my
`CLAUDE.md` looks like this:

```markdown
@AGENTS.md
```

## `AGENTS.md`

We don't describe the project in `AGENTS.md`. The description belongs
in the README, which the agent can read anyway.

What we put there:

- Commands, especially the non-obvious ones - how to run a single test,
  not just the whole suite
- Tooling rules - which package manager, which command form
- Constraints and cautions - what doesn't exist, and what must never
  be printed or committed
- Pointers to the real documents - where the spec, the process and the
  tasks live
- Corrections we got tired of repeating - anything we have typed more
  than once

It collects the things the agent got wrong, plus the things it can't
guess or would spend time discovering. Keep it short.

Here's an example:

```markdown
Commands

- `npm run dev` - dev server
- `npm test` - the whole suite
- `npm test -- cost` - one test file
- `npm run lint` - lint and format check, run it before committing

Rules

- Cost and rate calculations go in `src/cost/`, not in components
- Money is integer cents everywhere, never floats
- All time comes from `src/clock.ts`, do not call `Date.now()` anywhere
  else
- Salaries are entered as annual figures, the per-second rate is derived
- Tests live next to the code they cover, as `*.test.ts`
- Do not add dependencies without asking
- Do not edit `src/generated/`, it is rebuilt from the schema
- Commit regularly
```

I avoid markup there like sections, bold formatting, or tables. They
don't add any value and only result in higher token consumption.

Don't add these things to `AGENTS.md`:

- Transient task state. "Currently working on the cost calculation" is
  a session note, not a project fact.
- Anything secret. Keys, tokens, internal URLs, customer names. This
  file is read by tools, copied into contexts and committed to git. Use
  `.env` for that.
- Long explanations.

Keep this file short. If it becomes larger than a couple of screens,
move parts of it outside to separate markdown documents.

## The other documents

In addition to `AGENTS.md`, I usually have a few other markdown documents in 
my projects. 

One of them is `process.md` - it descrives how work is done in this project.

It could live inside `AGENTS.md`, but I keep a separate file for it:

```markdown
- Tasks are GitHub issues, one at a time
- Read the acceptance criteria before starting and before closing
- Commit regularly
```

As I continue working on a project, I create a separate document for
each thing we need to explain over and over again.

In my projects I often have

- `testing-guidelines.md` for testing
- `design-system.md` so the UI doesn't drift every session
- `setup.md`
- `api.md`

I keep them together in `_docs/` and link them from `AGENTS.md`:

```markdown
Documents

- `_docs/process.md` - how work is organized
- Before writing tests, read `_docs/testing-guidelines.md`
- For anything touching the UI, read `_docs/design-system.md`
```

The agent reads `AGENTS.md` at the start of every session, so it learns
that these documents exist.

It doesn't the content them immediately, only when
the task actually needs them. A task about the UI pulls in the design
system, a task about tests pulls in the testing guidelines. This keeps
`AGENTS.md` short while the project's written context keeps growing.


## Grooming: The product manager agent

We have a backlog of tasks, but they are not precise enough. 

The next step is "grooming", or making them more specific.
Grooming turns a placeholder task into something an engineer can
implement without asking a single question.

In teams, usually product managers do that. We will also have our own product
manager. 

For that, we need to describe the role. Let's create a doucment for that:

```text
_docs/team/
  pm.md
```

Inside, write the description:

```markdown
You're a Product Manager

You groom a task before anyone implements it.

- Read the issue as written
- Rewrite it using the template in `_docs/task-template.md`
- Make the acceptance criteria checkable - someone should be able to
  point at the screen and say yes or no
- Think about the edge cases the person who filed it did not
- Do not write any code

Definition of done:

- The issue has all four sections filled in
- Every acceptance criterion can be checked by looking at the result
- Everything moved out of scope links to a follow-up issue
- An engineer who has never spoken to you could implement it from the
  issue alone

If something does not belong in this task, do not silently drop it -
file a follow-up issue, and list it under out of scope with a link to
that issue, so it is clear what was moved and where it went.
```

The PM needs a structure to fill in, so a groomed issue always looks
the same. A groomed task has four sections:

1. Goal - one or two sentences on what should be true afterwards.
2. Acceptance criteria - checkable statements.
3. Out of scope - what this change must not do.
4. Constraints - files it should stay inside, libraries it should or
   shouldn't use, prior decisions it has to follow.

We save that as `_docs/task-template.md`:

```markdown
## Goal

One or two sentences on what should be true when this is done.

## Acceptance criteria

- [ ] A statement you can check by looking at the result
- [ ] One line per case, including the awkward ones

## Out of scope

- Something that does not belong in this task, moved to #12

## Constraints

- Files this should stay inside
- Libraries it may not add, patterns it must follow
```

Grooming is a part of the process, so let's add it to `process.md`:

```markdown
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
```

Let's work through an issue:

```text
Groom issue #4
```

Read the result before moving on.

Grooming is the cheapest place in
the whole process to catch a misunderstanding: the issue is a
paragraph, and correcting it costs one sentence. The same
misunderstanding found after implementation costs a rewrite, and found
after release costs considerably more.

Check that the goal matches what we actually wanted, that every
acceptance criterion is something we could check, and that nothing
important got scoped out. If the groomed issue surprises us, fix it
now.

## Implementation: The software engineer agent

Now the issue is groomed, so let's implement it. For that we need a software engineer.

The second role sits next to the first:

```text
_docs/team/
  pm.md
  software-engineer.md
```

`_docs/team/software-engineer.md`:

```markdown
You're a Software Engineer

You implement one groomed task at a time.

- Read the issue and implement what it describes
- Implement against the acceptance criteria, do not change them
- Stay inside the files and constraints the issue names
- Write tests for what you built
- Do not close the issue
- Commit regularly

Definition of done:

- Every acceptance criterion in the issue is implemented
- Tests are written for the new behaviour, and the whole suite passes
- The work is committed
- The issue is still open, with a comment saying what you did

If an acceptance criterion is wrong, impossible, or contradicts
another one, create a comment on the issue about it.
```

Add one more like to `process.md`:

```markdown
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
- Engineer - implements one groomed task, follows _docs/team/software-engineer.md
```

Then, in a fresh session:

```text
Implement issue #4
```

Make the agent work through it one change at a time, and make sure it
commits after every major step. Frequent commits give us a simple way
to go back: if the last commit was five minutes ago and something went
wrong, throwing the current code away and rewinding is easy. If it was
an hour ago, we'll have to re-create it.

The engineer session ends when the code is written and its own tests
pass. That's not the same as the task being done.

## testing: The QA engineer agent

An agent that writes the code and then judges this code is grading its own homework.

If we ask "is this correct?" we'll get "yes". But it might have missed 
a lot of the edge cases. 

So we need to test it in a separate sessoin. In teams, this is often done by QA engineers. That's the third role:

```text
_docs/team/
  pm.md
  software-engineer.md
  qa-engineer.md
```

The description:

```markdown
You're a QA Engineer

You check finished work against the issue that specified it.

- Read the acceptance criteria from the issue
- Check each one against what the code actually does
- Run the tests, and say which ones you ran
- Look for the cases the criteria describe but the tests do not cover
- Do not fix anything you find. Report it by creating a comment

Your output is a verdict: PASS or FAIL. It is FAIL if a single
acceptance criterion fails. Post it as a comment on the issue:

## QA: FAIL

- [x] Salary is entered as an annual figure - PASS
- [ ] Removing an attendee stops their cost accruing - FAIL
      Removed someone mid-meeting, the total kept rising

Tests: `npm test`, 14 passed, 0 failed

Definition of done:

- The comment starts with PASS or FAIL
- Every acceptance criterion has a verdict against it
- Every FAIL says what you did and what happened
- The test command and its result are included
- Nothing in the code was changed

Ignore what the implementation says it does. Only the acceptance
criteria and the running code count.
```

And the last line in `process.md`:

```markdown
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
- Engineer - implements one groomed task, follows _docs/team/software-engineer.md
- QA - checks the result against the acceptance criteria, follows _docs/team/qa-engineer.md
```

Then, in a new session:

```text
Test issue #4
```

If we get a `PASS`, it's great. If we get a `FAIL`, it's also good: 
we caught a regression. So we get back as a new engineer session, use 
the QA comment as the input, implement it, and iterate until QA says
`PASS`.


## Loop engineering

So far we have typed every prompt ourselves, running three sessions per
task. That's the right way to learn it, but it doesn't scale to many
issues.

Loop engineering is designing the system that runs a coding agent
repeatedly, instead of driving the agent prompt by prompt. The "system"
is the harness that controls the agent, plus whatever we wrap around
it. It decides what the agent picks up next, checks the result, and
decides whether to go again.

It's usually presented as one step on a ladder:

- Prompt engineering - what we say in one message
- Context engineering - what the agent knows before it starts
- Loop engineering - how often it runs, on what, and when it stops
- Graph engineering - who does what, when there's more than one agent

In June 2026 Addy Osmani published the
[Loop Engineering essay](https://addyo.substack.com/p/loop-engineering)
that gave it a name, and Peter Steinberger compressed the whole idea
into one sentence:

> stop prompting your agents and start designing the loops that
> prompt them.

The simplest useful loop is one command:

```text
/goal all tests pass
```

The agent works, runs the suite, and reads the failures. It works again
and stops when the suite is green or it hits the turn limit. We're not
in that cycle.

Something more realistic:

```text
/goal refactor src/cost so no file is over 200 lines, tests stay green
```

The stop condition has to be something a model can evaluate. "All tests
pass" is checkable, and so is "no file over 200 lines". "Make the code
better" isn't, so the agent can run forever, or stop too early.

Many harnesses ship these primitives: Claude Code has `/goal` and
`/loop`, Codex only has `/goal`. If ours doesn't, we can build them:

- Stop hooks. A hook that fires when the agent finishes a turn can
  check a condition and prompt it again, which is how we implement
  `/goal`.
- Scheduled pings into a tmux session. If the agent is running in tmux,
  we can send keystrokes to that session on a timer, which is how we
  implement `/loop`.


## Graph engineering

We have three roles and a way to run tasks in a loop, but we're still
moving manually between the roles. We read the QA verdict and decide
whether it goes back to the engineer or we pick up the next task.

Graph engineering is structuring work across several specialized
agents. We define what each one is responsible for, what order the
work moves in, and how they pass results along. We can draw any such
workflow as a graph: each agent is a node, each handoff is an edge, and
the design work is in the structure rather than in any single agent's
behaviour.

The term appeared on X around 18 July 2026, a month after loop
engineering, under the headline "Loop Engineering Is Dead". To me it
makes little sense as a new idea. People have been building
multi-agent systems and state machines for a long time, and
specialized workers passing work between them isn't new. In the same
discussion, people who build agent-orchestration tools said the term
was being used loosely, and they were right. Loop engineering isn't
dead either, because we still need a way to run our tasks. On top of
that, we add roles.

And what we built so far is already a graph:

```text
groom (PM)  ->  implement (engineer)  ->  test (QA)  ->  done
                       ^                        |
                       +--------- FAIL ---------+
```

Three nodes and four edges, including the one that sends failed work
back for another pass. Each role has a file saying what it does and
doesn't do, each has a definition of done, one role's output is
another's input, and the handoff is the issue rather than a
conversation. Because the issue carries all the context, each node can
start as a separate session.

### The orchestrator

The one thing still missing is the orchestrator, which so far has been
us. Something has to pick the next issue, dispatch each role in order,
read the verdict, and route on it. We make the main session do that, so
it dispatches the roles rather than doing the work.

So far `process.md` only lists who the roles are. Now we say how work
moves between them, and who moves it:

```markdown
Orchestrator

The main session is the orchestrator. It launches the PM, the engineer
and QA as subagents. It does not groom, implement or test itself.

Lifecycle

1. Pick the next open issue from the backlog
2. PM grooms it
3. Engineer implements it
4. QA verifies it
5. On FAIL, back to step 3 with the QA comment as input
6. On PASS, commit and close the issue
7. Repeat until the backlog is empty

Rules

- One issue at a time
- Do not skip step 2, even when the task looks obvious
- The engineer does not close the issue, QA does not fix the code
- Do not commit until the tests pass
```

That's the whole process file: three roles, an orchestrator, a
lifecycle and four rules. Mine are longer - they also say which agent
may commit, what a reviewer has to run before approving, and the
anti-patterns worth naming out loud, like skipping review because a
task looked small.

Now we're ready for our loop:

```text
/goal work through the backlog
```

The agent reads `AGENTS.md`, finds `process.md`, follows the lifecycle,
and dispatches the roles it finds in `_docs/team/`. Every piece of that
sentence is something we built earlier.

So if someone asks about graph engineering: it's several agents with
defined roles passing work to each other. The term
is from July 2026, but the practice is much older. It works because the
roles are explicit, the lifecycle is explicit, and the specifications
come before the implementation.


## Next in the series

This was the first module. The ones after it build on the same
workflow:

- Building and shipping a full-stack app end to end: spec to frontend,
  backend, tests, Docker, deployment and CI/CD
- Coding agent capabilities: MCP, skills, plugins, hooks and custom
  agents
- AI for security, audit and DevOps
- Taking a project of your own from an empty folder to something
  running

If you'd rather do the course than read it, the materials, the
homework and the next cohort are here:
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp).
It's free.

You can also read about my own multi-agent setup, the same three roles
plus an on-call agent watching CI, running across five real projects:
[I Built an AI Agent Team for Software Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software).

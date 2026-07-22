# The AI-Native Developer Workflow

## Specs Before Code

### The spec decides the outcome

You decide the quality of what an agent builds before it writes the
first line of code.

If a task is vague, the agent fills the gaps with its own assumptions.
The result will be far from what you imagined.

This gets worse as models get better. A weak agent that misunderstands
you writes fifty lines of broken code and you notice in a minute. A
strong agent that misunderstands you writes eight files and wires them
together. It adds tests that pass and gives you a working version of
the wrong thing. The more capable the agent, the further in the wrong
direction it goes before you notice it.

So you need to think in detail about what you want to build, and give
explicit instructions. Then the result will be close to what you want.

### Start in a chat assistant

Don't start your coding session with a coding agent. Coding agents write code, but you don't know what you want yet, so you'll only waste time and tokens.

Instead, open a chat assistant and talk the idea through. I use
dictation for this. It's faster than typing and it keeps me in the
mode of explaining rather than specifying.

In that conversation, cover:

- what the thing is
- who it's for
- what it should do
- what it shouldn't do
- what you're unsure about

Also ask it about what's already out there, so you don't spend a
weekend rebuilding something that exists.

As you progress through your session, you'll get a clearer vision of what you want to build.

At the end of the session, ask:

```text
Save this to a markdown file I can download.
```

That file is your spec.

This is how I built [SQLiteSearch](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight),
a small SQLite-backed search library. First it was a long chat
session to get the design straight. Then I downloaded the `plan.md` file, and started coding.

### Inside the spec

We write the spec once and keep it with the project.

Mine usually covers:

- what the project is, in a couple of sentences
- who it's for, and what they're trying to do
- what it doesn't do
- the stack, and the constraints it has to live inside
- a rough architecture: the main pieces and how they relate

The [`plan.md` for SQLiteSearch](https://github.com/alexeygrigorev/sqlitesearch/blob/main/plan.md)
had all five. It opened with what the library is, then a section on how
it differs from `minsearch`, the in-memory library it's a sibling to.
After that came explicit "when should you use this" and "when should
you not use this" sections, and it ended with the architecture.

### Two tiers

This approach has a name: spec-driven development.

You start with the specification, treat it as the canonical version,
and write the code from it.

There are two levels of specifications:

- Project-level - what the project is. We create it once and don't modify often.
- Feature-level - what a change should do and how you'll know it
  worked, written per task and thrown away after.

In my case the project level specs live in `plan.md`, `process.md` and `AGENTS.md`. I put these files in the `_docs` folder.

The feature level specs are tasks in a task tracking system. I usually use GitHub issues for that.


## Bootstrapping a Project

You have a spec, and now we turn it into a repo with a backlog the
agent can work through.

### The empty folder

Make a folder, initialise git, and drop the spec in.

```bash
mkdir project-name && cd project-name
git init
mkdir _docs
mv ~/Downloads/plan.md _docs/plan.md
```

### Decompose the spec

Open your coding agent in that folder and give it this prompt:

```text
Read plan.md. Propose a backlog of tasks that would implement it.

Each task should be small enough to finish in one session, and
independent enough that I could hand it to someone who has not read
the others. For each one give me a goal, acceptance criteria, what is
out of scope, and any constraints.

Do not write any code yet.
```

If you haven't decided what the tech stack for this project is, you should also do it.

Add a paragraph to the prompt asking for the decision rather than
assuming it:

```text
The stack is not decided yet. Before the backlog, propose one, with a
sentence on why. Keep it boring and widely used - I want to be able to
run this in two years.

Then make the first task setting up an empty project on that stack,
with a test that runs and passes.
```

Settle the stack here rather than let it happen on its own:

- the stack decides what half the tasks look like, so you have to
  settle it before the backlog means anything
- if you say nothing, the agent picks one anyway, silently, somewhere
  in the middle of task four

Write the answer into `_docs/plan.md` once you agree with it, because
the next session won't remember this conversation.


Next, review the tasks yourself. Check that they're granular enough
without being too granular, and that they make sense.

You can decide to merge some tasks into a bigger ones, or split big ones into smaller tasks. Or say that some things are out of scope. The planning you did previously will help, and if you're not sure about some things, discuss them with your coding assistant.

### Anatomy of a good task

Every task has four sections:

1. Goal - one or two sentences on what should be true afterwards.
2. Acceptance criteria - checkable statements. Not "it works" but
   things where you can point at the screen and say yes or no.
3. Out of scope - what this change must not do.
4. Constraints - files it should stay inside, libraries it may not
   add, patterns it must follow.

If a task takes more than a few minutes to write down, it's too big.
Split it.

A whole task from the meeting cost calculator backlog looks like this:

```markdown
# Pause the meeting

## Goal
The running meeting can be paused and resumed, so a break does not get
billed.

## Acceptance criteria
- Pausing stops the cost increasing, and the displayed total stays put
- Resuming continues from exactly the total shown, nothing is added for
  the paused period
- The elapsed time and the cost stay consistent with each other after
  any number of pauses
- Pausing before the meeting has started does nothing
- The current state, running or paused, is visible on screen

## Out of scope
- No history of pauses, no breakdown of paused time
- Do not touch the attendee list or the rate calculation

## Constraints
- Changes stay in the timer and cost modules
- Do not add a library for this
```


### Put the backlog in GitHub issues

After we decomposed the specs into backlog, we need to persist it.

GitHub issues work well for this, and the agent can create them:

```text
Create a GitHub issue for each task, using the four sections. Label
them so I can see the order you would do them in.
```

For that to work, you need the `gh` CLI tool authenticated.


## Context Engineering

The repo has a backlog now, but the agent that works through it still
starts every session knowing nothing about the project.

### Definition

Context engineering is the practice of making your project
understandable to an agent before the agent starts working.

It's not "writing better prompts". A prompt is one message in one
session, while context is everything the agent needs to know before it starts the task.

### AGENTS.md

Every session starts from a clean slate, and the agent doesn't remember what happened before.

The agent that refactored your test suite yesterday doesn't know today
that you use `pytest` and not `unittest`. So it has to discover it over and over again.

You can help it by specifying these things in `AGENTS.md`.
`AGENTS.md` is a plain Markdown file at the root of the repo
describing the project to any coding agent that opens it.

You can put anything you want to this file, and the agents read it at startup.

Note: Claude Code reads `CLAUDE.md`, not `AGENTS.md` like Codex and most other tools do.

I use multiple coding assistants, so my `CLAUDE.md` looks like this:

```markdown
@AGENTS.md
```

### Contents of AGENTS.md

You don't describe the project in AGENTS.md. The
description belongs in the README, which the agent can read anyway.

What you put there:

- Commands, especially the non-obvious ones - how to run a single test,
  not just the whole suite
- Tooling rules - which package manager, which command form
- Constraints and cautions - what doesn't exist, and what must never
  be printed or committed
- Pointers to the real documents - where the spec, the process and the
  tasks live
- Corrections you got tired of repeating - anything you have typed more
  than once

`AGENTS.md` isn't documentation for humans, though it can be useful for
them too. It collects the things the agent got wrong, plus the things
it can't guess or would spend time discovering.

Keep it short.

Here's one for the meeting cost calculator:

```markdown
Commands

- `npm run dev` - dev server
- `npm test` - the whole suite
- `npm test -- cost` - one test file

Rules

- Cost and rate calculations go in `src/cost/`, not in components
- Money is integer cents everywhere.
- Do not add dependencies without asking
- Commit regularly
```

I try to avoid putting markup there like sections, bold formatting, or tables. They don't add any value and only result in higher token consumption.



### Things to leave out

This is where beginners go wrong, and the failure is always the same:
the file grows until nobody, human or model, follows it.

Keep these out:

- Transient task state. "Currently working on the cost calculation" is a
  session note, not a project fact.
- Anything secret. Keys, tokens, internal URLs, customer names.
  This file is read by tools, copied into contexts and committed to
  git. Use `.env` for that.
- Long explanations.
- Rules nobody enforces. Delete it or enforce it programmatically.

A lean file that gets followed beats a long one that gets skimmed.
Every line you add makes the other lines slightly less likely to be
noticed. That cost is invisible until the file is already too big. If
yours is drifting past a couple of screens, cut it rather than add a
table of contents.


### The process document

`process.md` says how work moves through the project. It could live inside `AGENTS.md`, but I keep a separate file for that specifically. 

For now we can only add three lines there, but it will certainly grow as our project gets bigger.


```markdown
- Tasks are GitHub issues, one at a time
- Read the acceptance criteria before starting and before closing
- Do not commit until the tests pass
```

Let's include it in our AGENTS.md:

```md
The working process in `_docs/process.md`. When implementing a task, read this file.
```


### Other documents

In addition to `process.md`, you can keep a separate document for each
thing you need to explain over and over again.

In my projects I often have these files:

- `testing-guidelines.md` - how to write tests
- `design-system.md` - colours, typography, spacing, so the UI doesn't
  drift every session
- `setup.md` - how to get the project running
- `api.md` - the endpoints, and what they return

I keep them together in a `_docs/` folder and link them from `AGENTS.md`.

The agent reads `AGENTS.md` at the start of every session, so it learns that these documents exist. 
It doesn't read them immediately, only when it's actually needed for the task.

In `AGENTS.md` we list them like this:

```markdown
Documents

- `_docs/plan.md` - what we are building
- `_docs/process.md` - how work moves through the project
- Before writing tests, read `_docs/testing-guidelines.md`
- For anything touching the UI, read `_docs/design-system.md`
```

The agent then opens the document relevant to the task:

- A task about the UI pulls in the design system.
- A task about tests pulls in the testing guidelines.

This keeps `AGENTS.md` short while the project's written context keeps
growing.


## Grooming a Task

We saw that you decide the quality of what an agent builds before it
writes any code, and then we turned the spec into a backlog.

Those backlog items are still rough. A task like "add attendees" is a
placeholder - it names the work without saying what done looks like.
In grooming we turn it into something an engineer can implement without
asking you a single question.

It's the same idea as the project spec, but for an individual task, not the entire project.

### Product manager

In a product team, grooming is usually the responsibility of the Product Manager. So let's create our own product manager to do it.

Create a `team/` folder with a `pm.md` file:

```text
team/
  pm.md
```

Here's what's inside:

```markdown
You're a Product Manager

You groom a task before anyone implements it.

- Read the issue as written
- Rewrite it using the template in `team/task-template.md`
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

If something does not belong in this task, do not silently drop it - file a follow-up issue, and list it under out of scope with a link to that issue, so it
is clear what was moved and where it went.
```

### The task template

The PM needs a structure to fill in, so a groomed issue always looks
the same.

Put it in `team/task-template.md`:

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

Checkboxes are worth the two extra characters. They give the QA session
later a list to tick off one by one. They
also make an unfinished task visible at a glance.

Link the folder from `AGENTS.md`, the same way as the `_docs` files:

```markdown
Team

- To groom a task, follow `team/pm.md`
```

The agent learns the role exists when it starts, and opens the file
when you ask it to groom something.

### Running the session

Start a fresh session:

```text
Groom issue #4
```

Read and understand the result before you move on.

Grooming is the cheapest place in the whole process
to catch a misunderstanding: the issue is a paragraph, and correcting
it costs one sentence.

The same misunderstanding found after
implementation costs a rewrite, and found after release costs
considerably more.

Check that:

- the goal matches what you actually wanted
- every acceptance criterion is something you could check
- nothing important got scoped out

If the groomed issue surprises you, fix the result.


## Implementing a Task

The issue is groomed, so now we write the code.

### Software engineer

The next role in the team is the one that does the implementation.

Add `software-engineer.md` next to `pm.md`:

```text
team/
  pm.md
  software-engineer.md
```

Here's what's inside:

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

And add it to `AGENTS.md`:

```markdown
Team

- To groom a task, follow `team/pm.md`
- To implement a task, follow `team/software-engineer.md`
```

Then start a fresh session:

```text
Implement issue #4
```


### Small steps

Make the agent work through it one change at a time, and make sure it commits after every major step.

Frequent commits give you a cheap way to go back. If the last commit was
five minutes ago, and something went wrong, throwing the current code away and rewinding is easy. If it
was an hour ago, you'll have to re-create it.

The engineer session ends when the code is written and its own tests
pass. That's not the same as the task being done - it's the agent
marking its own homework, which is what we deal with next.


## Testing a Task

The code is written and the engineer says it works. Now we check whether that's true.

### The best tester is not the author

An agent that writes the code and then judges whether the code is
correct is grading its own homework.

By the time it finishes, it has spent its entire context building the
case that its approach was the right one. If you ask "is this correct?"
you'll get "yes, this correctly handles the edge case".

But the edge cases are only the ones that it thought of, handled the way it decided to handle it.

In software engineering teams we have QA engineers: people who specialize
on testing software.

We follow the same idea here. Testing gets its own session, with no
memory of how the code was written. It checks the result against the
acceptance criteria independently.

### QA engineer

Add `qa-engineer.md` to the team:

```text
team/
  pm.md
  software-engineer.md
  qa-engineer.md
```

Here's what's inside:

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

And add it to `AGENTS.md`:

```markdown
Team

- To groom a task, follow `team/pm.md`
- To implement a task, follow `team/software-engineer.md`
- To test a task, follow `team/qa-engineer.md`
```

Then, in a new session:

```text
Verify issue #4
```

### Tests as the guardrail

The "don't fix anything" rule keeps the roles apart. A QA
session that repairs the findings becomes the author
again, so you're back to marking your own homework.

A FAIL goes back as a new engineer session, with the QA comment as the
input. Then QA runs again. You repeat the process until it passes.

You close the issue only on a PASS.

"Mostly works, a couple of small things" isn't an outcome. Only `PASS` or `FAIL` are accepted.


Tests let you delegate the implementation to agents without reading every line.


## Loop Engineering

So far you have typed every prompt yourself, running three sessions per
task to groom, implement, and test.

That's the right way to learn it, but it doesn't scale to many issues.

Loop engineering helps with that.

Loop engineering is designing the system that runs a coding agent
repeatedly, instead of driving the agent prompt by prompt.

The "system" is the harness that controls your agent, plus whatever you
wrap around it. It decides what the agent picks up next, checks the
result, and decides whether to go again.


### The ladder

Loop engineering is usually presented as one step on a ladder:

- Prompt engineering - what you say in one message
- Context engineering - what the agent knows before it starts
- Loop engineering - how often it runs, on what, and when it stops
- Graph engineering - who does what, when there's more than one agent

In June 2026 Addy Osmani published the [Loop Engineering essay](https://addyo.substack.com/p/loop-engineering) that gave it a name and Peter Steinberger compressed the whole idea into one
sentence:

> stop prompting your agents and start designing the loops that
> prompt them.

TODO - screenshots of the original X posts

Many harnesses have built-in support for loops like
`/goal`, `/loop` and `/schedule`.

That's what puts this term on firmer ground than the one in the next
section. The vendors shipped features for it, rather than only arguing
about it on X.

### /goal in practice

The simplest useful loop is one command:

```text
/goal all tests pass
```

The agent works, runs the suite, and reads the failures. It works again
and stops when the suite is green or it hits the turn limit. You're not
in that cycle.

Something more realistic for our project:

```text
/goal refactor src/cost so no file is over 200 lines, tests stay green
```

The stop condition has to be something a model can evaluate: "all tests
pass" is checkable, and so is "no file over 200 lines".

"Make the code better" isn't checkable, so your agent can run forever (or stop too early).

### Building the loop yourself

Many harnesses have the primitives you need to implement loops:

- Claude Code has `/goal` and `/loop`
- Codex only has `/goal`

But some harnesses may not have it, so it could be useful to know how to write them yourself.

You need these:

- Stop hooks. A hook that fires when the agent finishes a turn can
  check a condition and prompt it again, which is how you implement `/goal`.
- Scheduled pings into a tmux session. If the agent is running in tmux,
  you can send keystrokes to that session on a timer, which is how you implement `/loop`.


## Graph Engineering

We already have three roles and a way to run tasks in a loop.

But we're still moving manually between roles. You read the QA verdict and decide whether it goes back to the engineer or you pick up the next task.

Now we'll automate it.

### The definition

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

### You already built the graph

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

### The orchestrator

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
sentence is something you built earlier.


So if someone asks you about graph engineering, you can say that it's
several agents with defined roles passing work to each other.

The term is from July 2026, but the practice is much older. It works
because the roles are explicit, the lifecycle is explicit, and the
specifications come before the implementation.

### Going further

You can learn about my own multi-agent setup here:

- [I Built an AI Agent Team for Software Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software)

It's the same three roles plus an on-call agent watching CI, running
across five real projects.

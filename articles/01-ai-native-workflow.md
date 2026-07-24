# AI-Native Development: Specifications, Loop and Graph Engineering

This is the first article in a series based on
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

This year I wanted to do an experiment and publish a series of course notes as articles on Substack. I plan to publish one independent article per module. I start with the first one: AI-native developer workflows.

Coding agents now write code faster than I can read it. 

When we give an agent a task, it can quickly implement it.
But if a task is vague, the agent fills the gaps with its own assumptions.
A weak agent that misunderstands us writes fifty lines of broken code. A strong
agent that misunderstands us creates eight files, wires them together, and adds
tests that pass. The code works, but it isn't what we needed.

We no longer spend most of our time typing. We spend it saying precisely what
we want and checking what came back.

In this article, I show how to make the request specific, so the agents
don't need to guess. Then we decompose the request into tasks, and assign each one to a team of agents: a product manager, a software engineer and a tester. 
Finally, we implement all the tasks in a backlog through a loop.

We cover topics like:

- Spec-driven development
- Context engineering
- Loop engineering
- Graph engineering


## Running example

We use a deliberately vague project idea: a tool for weekly feedback for
projects. It doesn't say who gives the feedback, who receives it, or what
"projects" means.

First, we give the idea to Claude Code exactly as written:

```text
Implement a tool for weekly feedback for projects.
```

We let the agent work without answering questions or correcting its
assumptions. While it does that, we work out what we want to build.


## Specs before code

We need to understand what we want to build before the agent produces the first
line of code for the intended project. So we think it through in detail and
give explicit instructions. If we do that, the agent will produce something
close to what we want.

We call this spec-driven development. We start with the
specification, treat it as the canonical version, and write the code
from it.

There are two levels of specifications:

- Project-level - what the project is. We create it once and don't
  modify often.
- Feature-level - what a change should do and how we'll know it
  worked, written per task and thrown away after.

For this project, we save the project-level spec in `_docs/plan.md` and turn
the feature-level specs into tasks in GitHub issues.

## Start in a chat assistant

Don't use the one-shot implementation as the foundation for the real project.
The coding agent is already making decisions, but we still don't know what we
want.

Instead, open a chat assistant and talk the idea through. I use ChatGPT in
dictation mode for this. It's faster than typing, and I keep explaining rather
than switching into specification mode.

We begin with the same vague idea:

```text
I want to build a tool for weekly feedback for projects. Help me set
the scope for this project precisely. I want to brainstorm with you
and understand how the tool should work. Give me some options and ask
me some questions.
```

ChatGPT answers at length and asks several questions in one batch. We want a
conversation we can follow without reading a wall of text.

Ask ChatGPT to slow down:

```text
Ask me one question at a time and keep your output short.
```

ChatGPT now asks who contributes feedback. We choose all team members rather
than only the project owner. We therefore design a retrospective where the team
discusses the feedback together.

As we answer the next questions, we make the product more specific and choose
Start/Stop/Continue feedback. Submissions show the contributor's name by default,
but someone can choose to submit anonymously. Before the facilitator reveals
the feedback, each person sees only their own cards.

The facilitator reveals all cards at the same time. The team clusters them and
votes for the topics to discuss. Each person gets three votes and may put more
than one vote on the same topic. The team records decisions and action items
after the discussion.

We also limit the first version. The facilitator uploads audio, video, or a
transcript after the meeting. We don't add built-in recording yet.

We could continue answering questions for a long time. Once the important
choices are clear, we delegate the remaining ones.

Ask ChatGPT to finish the open decisions:

```text
Make the remaining decisions yourself. Explain why you chose each
option, why you chose it over the alternatives, and which other
options you considered.
```

We review those decisions instead of accepting them blindly. In the finished
specification, we describe the product and its roles. We also record the main
screens, the first version, and what we have left out.

At the end, ask:

```text
Save everything to a markdown file that I can download.
```

We save the file as `_docs/plan.md` without discussing the stack or code, so we
know what we want to build but not how we'll build it.

## One line, different product

By the time we finish the specification, Claude Code has also finished its
one-shot implementation.

The agent writes a complete zero-dependency Python CLI. You can register
projects, record their status, generate a Markdown digest, and list the people
who haven't reported. It also writes tests and documentation.

![The one-shot weekly-feedback CLI](images/01-wrong-implementation.png)

You can read and run the
[`weekly-feedback` source](../01-ai-native-workflow/weekly-feedback/).
The code works, but I had a team retrospective app in mind rather than a
personal status-reporting CLI. Claude Code had no way to know that because the
prompt said nothing about teams or anonymity. It also omitted
Start/Stop/Continue cards, clustering, voting, and action items.

The CLI is useful, but it solves a different problem. We keep it as the
comparison and use the specification to start the intended project.

## Bootstrapping a project

We spend substantial time on bootstrap because every later agent session
depends on it. We first turn the specification into a versioned project and
choose the architecture. We then create the backlog, publish the repository,
and leave the first task running with a passing test.

Create a folder, initialise Git, and add the specification:

```bash
mkdir project-feedback
cd project-feedback
git init
mkdir -p _docs
mv ~/Downloads/plan.md _docs/plan.md
git add _docs/plan.md
git commit -m "Add project plan"
```

Commit after every meaningful decision. With those commits, we can review what
the agent changed and return to the last good state.

## Choose the stack and architecture

We don't choose technologies in the product specification.

Ask the coding agent to compare several options before it writes code:

```text
Read _docs/plan.md. Propose multiple options for the tech stack and
explain each option.

Don't write code yet.
```

We choose Django because we know it well enough to review.

Record the decision:

```text
We'll use Django. Create architecture.md with the chosen technologies
and architecture decisions. Commit when you finish.
```

The agent includes infrastructure that we don't need in its first architecture
draft.

We correct it before creating tasks:

- Use current stable Python and PostgreSQL versions.
- Use username and password authentication without email.
- Don't add Redis or background workers.
- Process uploaded recordings and discard them instead of storing them.
- Use OpenAI Whisper for transcription.
- Keep deployment out of scope and use Docker Compose for local services.

After the corrections, verify that the technology choices haven't gone stale:

```text
For every technology choice in architecture.md, check whether a newer
stable version is available. Update the document where needed.
```

If the agent changes its conclusions without changing the file, correct it:

```text
Update architecture.md before you commit.
```

In `plan.md`, we describe what we want to build, and in `architecture.md`, we
describe how we'll build it.

## Turn the decisions into a backlog

Ask the agent to read both documents and split the work:

```text
Read _docs/plan.md and _docs/architecture.md. Create a backlog in
_docs/tasks.md.

Each task should be small enough to finish in one session, and
independent enough that I could hand it to someone who has not read
the others.

Use this template for each task:

## <number>. <title>
Goal: <one line>
Description: <two or three sentences on what the task involves>

Make the first task setting up an empty project, with a
test that runs and passes.

Don't write code yet.
```

Review a few tasks before creating the backlog. Merge tasks that are too small,
split tasks that don't fit one session, and move unrelated work out of scope.

I used the same plan-first sequence for
[SQLiteSearch](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight).
In its
[`plan.md`](https://github.com/alexeygrigorev/sqlitesearch/blob/main/plan.md),
I explain what the library is, how it differs from
[minsearch](https://alexeyondata.substack.com/p/minsearch-the-small-search-library).
I also explain when to use each library and how SQLiteSearch is organized.

When the tasks are ready, create the
[`retroloop`](https://github.com/alexeygrigorev/retroloop) GitHub repository.
You can review what we have created so far in its
[`plan.md`](https://github.com/alexeygrigorev/retroloop/blob/main/_docs/outdated/plan.md),
[`architecture.md`](https://github.com/alexeygrigorev/retroloop/blob/main/_docs/outdated/architecture.md),
and
[`tasks.md`](https://github.com/alexeygrigorev/retroloop/blob/main/_docs/outdated/tasks.md).

We use these documents to seed the backlog. We move the actual work to GitHub
issues, so the plan, architecture, and task list may become stale later.

## Publish the project and bootstrap the first task

Before publishing the repository, choose a name that describes the product:

```text
I want to publish this project on GitHub, but I don't like the name.
Help me choose a name that reflects its purpose. Read plan.md to
understand what we're building.
```

We choose `retroloop`, create it in a personal GitHub account, and make it
public:

```text
Create a public GitHub repository named retroloop in my personal
account.
```

We use GitHub issues as the task tracker:

Give the agent this instruction:

```text
Create a GitHub issue for each task in _docs/tasks.md.
```

For that to work, we need the `gh` CLI tool authenticated and the repo
connected to the GitHub remote.

Start the first task with the short instruction used in the project:

```text
Implement task number one.
```

We left an important detail out of this instruction. The agent finds task 1 in
`tasks.md` instead of opening the GitHub issue.

Tell it where the task lives:

```text
Implement task number one, which is a GitHub issue.
```

For the first task, the agent creates the Django project, dependencies, and a
passing test. From here on, every task starts from a project that already runs.
A failing test now means the task broke something rather than that the project
never worked.


## Context engineering

The repo has a backlog now, but the agent that works through it still
starts every session knowing nothing about the project.

When the agent implemented the first task, we saw what was missing. We wrote
`Implement task number one`, and the agent had to guess where the task lived.
It found the archived task list even though GitHub issues were supposed to hold
the canonical tasks.

With prompt engineering, we control one message in one session. With context
engineering, we give every new session the project facts and working rules it
would otherwise have to rediscover.

We can put these details in `AGENTS.md`. Coding agents read this plain
Markdown file from the repo root when they start.

Claude Code reads `CLAUDE.md`, while Codex and most other tools read
`AGENTS.md`. I use multiple coding assistants.

My `CLAUDE.md` contains one line:

```markdown
@AGENTS.md
```

## `AGENTS.md`

The agent that bootstrapped the project already knows the stack and useful
commands.

Ask it to preserve that information before starting a fresh session:

```text
Commit what you have. Then create AGENTS.md with content similar to
this example.
```

Agents tend to fill the generated file with project descriptions, markup,
speculative rules, and details relevant to only one task. We pay the token cost
of that text in every session.

Review and trim the file:

```text
Do we really need all these rules? Every agent session in this
repository will read this file. Keep only the most important
information that every session needs.
```

We don't repeat the project description in `AGENTS.md`. We put it in the
README, which the agent can read when it needs that context. We also remove
statements about tools or services that don't exist. Saying that the project
doesn't use five unrelated technologies doesn't help an agent complete a task.

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

Use it to collect the things the agent got wrong, plus the things it can't
guess or would spend time discovering. Keep it short.

For example:

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

If `AGENTS.md` becomes larger than a couple of screens, move parts of it into
separate Markdown documents.

## The other documents

In addition to `AGENTS.md`, I usually have a few other markdown documents in 
my projects. 

I use `process.md` to describe how work is done in the project. It could live
inside `AGENTS.md`, but I keep it separate.

We start with a short version:

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

The agent reads `AGENTS.md` at the start of every session, so it knows where to
find the process, testing, and design rules.

It loads the design system only for a UI task and the testing guidelines only
for a testing task. By loading each document only when it's relevant, we keep
`AGENTS.md` short while we continue adding written context to the project.

Whenever we have to correct an agent, we decide whether the correction belongs
in the written process:

```text
Based on the corrections I made, find the relevant project documents
and update them so the next agent follows the right process. Commit
the current work before changing the documents.
```

Review process changes as carefully as code because agents will apply one
incorrect rule to every task that follows it.

## Grooming: The product manager agent

We have a backlog of tasks, but they're not precise enough.

Next, we "groom" the tasks, or make them more specific.
When we groom a placeholder task, we turn it into something an engineer can
implement without asking a single question.

Product managers usually do this work, so we'll define that role for our
agent team.

Create a document for the role:

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

We give the PM a structure to fill in so every groomed issue looks the same.

A groomed task has four sections:

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

Because we groom every task, let's add that work to `process.md`:

```markdown
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
```

First, ask the PM to work through the backlog one issue at a time:

```text
Groom all GitHub issues, starting with issue #4. If something is
unclear, consult plan.md in the outdated documents folder. The issues
should become self-contained.

Process one issue at a time for now.
```

Read issue 4 before moving on. During the first pass, the PM creates follow-up
issues before it finishes rewriting the original issue.

Correct the order:

```text
First update the original issue. After that, create follow-up issues
for work moved out of scope.
```

The PM also creates `MVP` and `post-MVP` labels. We assign the original backlog
to the MVP and usually schedule follow-up work created during grooming for
later.

Label the issues explicitly:

```text
Create MVP and post-MVP labels. Mark issues 1 through 26 as MVP and
mark the remaining issues as post-MVP.
```

Review those labels rather than assuming every new issue belongs in the first
version.

We can catch a misunderstanding most cheaply while grooming: the issue is a
paragraph, and correcting it costs one sentence. If we catch the same
misunderstanding after implementation, we need a rewrite. If we catch it after
release, fixing it costs considerably more.

Check that the goal matches what we actually wanted, that every
acceptance criterion is something we could check, and that nothing
important got scoped out. If the groomed issue surprises us, fix it
now.

## Loop engineering

We introduce loop engineering here, as soon as we have groomed one issue and
can see the repeated work. We don't wait until the whole agent team exists.

Instead of prompting the PM for each issue ourselves, we can give the agent a
goal:

```text
/goal groom all MVP issues. Make clear, documented decisions for any
loose ends.
```

The agent works through the issues and checks its progress against the goal. If
it stops early, the harness prompts it to continue. It stops when every MVP
issue is groomed or when it reaches the turn limit.

When we engineer a loop, we design the system that runs a coding agent
repeatedly instead of driving it prompt by prompt.

We add one layer at a time:

- Prompt engineering - what we say in one message
- Context engineering - what the agent knows before it starts
- Loop engineering - how often it runs, on what, and when it stops
- Graph engineering - who does what when there's more than one agent

In June 2026 Addy Osmani published the
[Loop Engineering essay](https://addyo.substack.com/p/loop-engineering)
that gave it a name, and Peter Steinberger compressed the idea into one
sentence:

> stop prompting your agents and start designing the loops that
> prompt them.

The stop condition must be something the model can evaluate. "All MVP issues
are groomed" is checkable, as are "all tests pass" and "no file is over 200
lines." "Make the code better" isn't, so the agent can stop too early or run
forever.

Claude Code provides `/goal` and `/loop`, while Codex provides `/goal`.
`/loop` sends a scheduled prompt, while `/goal` prompts the agent again when it
tries to stop before meeting the goal.

If our harness doesn't provide them, we can build them:

- Stop hooks can check a condition when the agent finishes a turn and prompt
  it again.
- Scheduled pings can send keystrokes to an agent running in a tmux session.

## Implementation: The software engineer agent

After grooming the issue, we give it to a software engineer.

Define the second role next to the first:

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

The agent discovers that issue 4 depends on the project setup from issues 2
and 3. We let it finish those technical prerequisites before returning to the
first user-facing feature. We skip the full PM, engineering, and QA sequence for
small setup tasks, but use it for user-facing work.

Ask the agent to implement the issue in small changes and commit after each
major step. By committing frequently, we can go back. Rewinding five minutes of
work is easy, while re-creating an hour of work isn't.

The engineer stops when the code is written and its own tests pass.
That's not the same as the task being done.

## Testing: The QA engineer agent

An agent that writes the code and then judges this code is grading its own homework.

If we ask "is this correct?" we'll get "yes," but the agent might have missed
many edge cases.

We test it in a separate session, as a QA engineer would.

Add the third role:

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

- [x] A visitor can create an account with a username and password - PASS
- [ ] A duplicate username shows a visible error - FAIL
      Submitted an existing username and received an unhandled error

Tests: `uv run pytest`, 18 passed, 0 failed

Definition of done:

- The comment starts with PASS or FAIL
- Every acceptance criterion has a verdict against it
- Every FAIL says what you did and what happened
- The test command and its result are included
- Nothing in the code was changed

Ignore what the implementation says it does. Only the acceptance
criteria and the running code count.
```

If you adapt a role description from another project, update its commands and
examples. A QA role that tells a Django project to run `npm test` will fail
before it checks any acceptance criteria.

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


## Graph engineering

We have three roles and a way to run tasks in a loop, but we're still
moving manually between the roles. We read the QA verdict and decide
whether it goes back to the engineer or we pick up the next task.

When we engineer a graph, we structure work across specialized agents. We
define each agent's responsibility and the order in which they work. We also
define how they pass results between roles.

We can draw this workflow as a graph. Each agent is a node, each handoff is an
edge, and the connections determine how the team works.

The term appeared on X around 18 July 2026, a month after loop
engineering, under the headline "Loop Engineering Is Dead". To me it
makes little sense as a new idea. People have been building
multi-agent systems and state machines for a long time, and
specialized workers passing work between them isn't new.

In the same discussion, people who build agent-orchestration tools said the
term was being used loosely, and they were right. Loop engineering isn't dead
either because we still need a way to run our tasks. We add roles on top of
that loop.

And what we built so far is already a graph:

```text
groom (PM)  ->  implement (engineer)  ->  test (QA)  ->  done
                       ^                        |
                       +--------- FAIL ---------+
```

The graph has three nodes. When QA returns `FAIL`, the orchestrator sends the
issue back to the engineer for another pass. Each role has its own instructions
and definition of done, and each role passes its output to the next role as
input.

The agents hand off an issue rather than a conversation. Because we put the
required context in the issue, we can start each role in a separate session.

## The orchestrator

We have acted as the orchestrator so far. We pick the next issue, dispatch each
role in order, read the verdict, and route the issue. The main session can do
this work and leave grooming, implementation, and testing to its subagents.

In `process.md`, we have only listed the roles, so we now add the sequence and
name the orchestrator.

Add these sections:

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
- Focus on MVP issues
```

In `process.md`, we now define three roles and an orchestrator along with the
lifecycle and its rules. In larger projects, I specify which agent may commit
and what a reviewer must run before approving. I name known failure modes too,
such as skipping review because a task looked small.

We can now run the backlog:

```text
/goal work through the backlog. Focus on MVP issues only.
```

The agent reads `AGENTS.md`, finds `process.md`, follows the lifecycle,
and dispatches the roles it finds in `_docs/team/`. We added each of those
instructions earlier.

![The goal continues from one backlog issue to the next](images/01-goal-is-not-met.png)

The orchestrator continues until it meets the backlog-level goal, and its
commits and issue discussions remain visible in
[`retroloop`](https://github.com/alexeygrigorev/retroloop).

We won't anticipate every failure in the first version of `process.md`. When we
have to steer the orchestrator manually, we update the process so the next run
knows what to do. Over time, we expand a short lifecycle into the project's
working instructions by adding those corrections.

An agent can spend hours on a backlog-level goal and use several times more
tokens than direct implementation. The PM grooms each issue, the engineer
implements it, and QA tests it. When QA returns `FAIL`, the engineer makes
another implementation pass.

So if someone asks about graph engineering: it's several agents with
defined roles passing work to each other. The term
is from July 2026, but people have worked this way for much longer. It works
because we explicitly define the roles and lifecycle, then write the
specifications before we implement them.


## Next in the series

We have now finished the first module.

In later modules, we build on the same workflow:

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

My own multi-agent setup runs the same three roles across five real projects.
It also adds an on-call agent that watches CI:
[I Built an AI Agent Team for Software Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software).

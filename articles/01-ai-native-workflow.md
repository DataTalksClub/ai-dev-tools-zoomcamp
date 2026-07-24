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

We will use a deliberately vague project idea: a tool for weekly feedback for
projects. It doesn't say who gives the feedback, who receives it, or what
"projects" means.

You can see the final result here (todo link the retroloop project here)

## Specs before code

We need to understand what we want to build before the agent produces the first
line of code. We have to think it through in detail and give explicit instructions.
If we do that, the agent will produce something close to what we want.

We call this "spec-driven development". We start with the
specification, make sure it aligns with our vision, and only then
write the code from it.

In our example, "a tool for weekly feedback for
projects", many things are not clear.

- Who are the users for this tool?
- What  is the problem they will solve?
- How are they going to use it?

If we don't speficy these things, and just give it to a coding agent,
it will fill the gaps by itself. 

When I asked Claude Code to implement this project, the only prompt I gave 
was "a tool for weekly feedback for projects". It came up with  [`weekly-feedback`](../01-ai-native-workflow/weekly-feedback/) [todo: full guthub path] - a command line tool for ... 
It created documentation and covered the app with tests (X of them) which all pass.

![The one-shot weekly-feedback CLI](images/01-wrong-implementation.png)

It all works perfectly. But that's very far from what I actually needed.
I needed a web tool for a team retrospective that captures feedback
from teams in the form of "stop, start, continue". And it was my fault 
that I didn't tell that to Claude.


## Start in a chat assistant

Instead of giving a prompt directly to the coding assistant,
I start first in a chat application and talk the idea through.
I use ChatGPT in dictation mode for this. 

There I begin with the same vague idea:

```text
I want to build a tool for weekly feedback for projects.

Help me set the scope for this project precisely. I want to brainstorm with you
and understand how the tool should work. Give me options.

Ask me one question at a time and keep your output short.
```

This way we can use AI as our brainstorming partner and find out precisely what we want:

- Who is the user? "our answer"
- ... continue in the same way. question - short answer.
- TODO finish the list

When we finish, I want to download a file with all the specs:

```text
Save everything to a markdown file that I can download.
```

Download this file and save it as `plan.md`.


## Bootstrapping a project

Now let's create a project from this specification:

```bash
mkdir project-name
cd project-name

git init
```

Copy the `plan.md` file: 

```bash
mkdir -p _docs
mv ~/Downloads/plan.md _docs/plan.md
git add _docs/plan.md
git commit -m "Add project plan"
```

You can find the plan [here](inclide the link to the plan). 

I try to commit as often as possible. Commit after every meaningful decision.
With those commits, we can review what the agent changed. If something is not
working well, we can easily return to the last good state.

## Choose the stack and architecture

During the brainstorming session we didn't choose the tech stack. 

Let's do it now. Ask the coding agent to come up with several options:

```text
Read _docs/plan.md. Propose multiple options for the tech stack and
explain each option.

Don't write code yet.
```

It proposed multiple options: option 1, 2, 3 ...

I choose Django because I know it well enough to review. In your case,
you can select any technology you're comfortable with. It's also okay 
to not have preferences and let the agent select what it things works best.


## Turn the decisions into a backlog

Now we settled on the tech stack and can ask the agent to decompose the specs
into a backlog with tasks:

```text
Create a backlog with tasks in _docs/tasks.md.

Each task should be small enough to finish in one session, and
independent enough that I could hand it to someone who has not read
the others.

Use this template for each task:

## <number>. <title>
Goal: <one line>
Description: <two or three sentences on what the task involves>

The first task should be setting up an empty project with a passing test.

Don't write code yet.
```

It created these tasks: [`tasks.md`](TODO add link).

Now review the tasks. Ask the agent to merge tasks that are too small, or
split tasks that don't fit one session. If something is out of scope for your 
vision of the MVP (the first version of your app), remove it.

When we're okay with the tasks, ask the coding assistant to create 
tasks in a task tracker. I use GitHub issues for that.  

Ask the agent to do it:

```text
Create a public GitHub repo for this project.
Then create an issue in that repo for each task in _docs/tasks.md.
```

For that to work, we need the `gh` CLI tool authenticated and the repo
connected to the GitHub remote.

You can see the project that came out of it here: [`retroloop`](https://github.com/alexeygrigorev/retroloop).


## Context engineering

The repository has a backlog now. But when we start a new session and ask it
to implement a task, it has no idea which task we mean.
Every time it will need to figure that out. 

These details go to `AGENTS.md`. Coding agents like Codex or OpenCode
read it when they start a new session.

But Claude Code reads `CLAUDE.md`. I use multiple coding assistants, so I want
my workflow to be tool agnostic. That's why I also create `CLAUDE.md`
that contains one single line:

```markdown
@AGENTS.md
```

It tells Claude to read AGENTS.md. 

This is called context engineering. TODO explan the term more. We had some explanation about it.

Prompt engineering is the prompts we give to our agents. This way we control one message in one session.

With context engineering, we contol what the agents know about the project
when they start a new session. We include useful facts and working rules
it would otherwise have to rediscover.


## `AGENTS.md`

This is how the initial version of `AGENTS.md` can look like: 

```text
TODO include the initial version of agents.md that we had in retroloop 
```

You can copy this file, and ask the coding assistnat to create somethin similar but tailored to your project.

We don't repeat the project description in `AGENTS.md`. We put it in 
README.md, which the agent can read also when it needs that context. 

What we put there:

- Commands - how to run all tests and a single test
- Tooling rules - which package manager we use
- Corrections we don't want to repeat - anything that could be useful in every session

Don't add these things to `AGENTS.md`:

- Transient task state. "Currently working on task #4" is
  a session note, not a project fact.
- Anything secret. Keys, tokens or internal URLs. Use `.env` for that.
- Long explanations.

I avoid markup like sections (`##`), bold formatting (`**`), or tables. It doesn't add
any value and only result in higher token consumption.

If `AGENTS.md` becomes larger than a couple of screens, move parts of it into
separate Markdown documents.

## The other documents

In addition to `AGENTS.md`, I usually have a few other markdown documents in 
my projects. 

The main one is `process.md` that I use to describe how work is organized. It could live inside `AGENTS.md`, but I keep it separate.

Let's create `_docs/process.md`:

```markdown
- Tasks are GitHub issues, one at a time
- Read the acceptance criteria before starting and before closing
- Commit regularly
```

As I continue working on a project, I may create other documents
like

- `testing-guidelines.md` for testing
- `design-system.md` so the UI doesn't drift every session
- `api.md` that describes how API should look like 

I keep them together in `_docs/` and link them from `AGENTS.md`:

```markdown
Documents

- `_docs/process.md` - how work is organized
- Before writing tests, read `_docs/testing-guidelines.md`
- For anything touching the UI, read `_docs/design-system.md`
```

The agent reads `AGENTS.md` at the start of every session, so it knows where to
find the process, testing, and design rules if it needs them.

This way, it will load the design system only for a UI task and the
testing guidelines only for a testing task.
By loading each document only when it's relevant, we keep
`AGENTS.md` short while we continue adding written context to the project.

These documents are live documents and I update them often. If I need to correct
an agent during a coding session, I can ask it to modify the documents.
Next time it knows what I need, so I don't have to correct it again.

You can use a prompt like that:

```text
Based on the corrections I made, find the relevant documents
and update them.

Commit the current work before changing the documents.
```

## Bootstrap the first task

Now with `AGENTS.md` and `process.md` in place, we can start a new session and ask the agent to implement the first task:

```text
Implement task 1.
```

For this project, the agent creates the Django app, dependencies, and a
passing test.


## Grooming: The product manager agent

We have a backlog of tasks, but they're not precise enough.

We discussed this problem already: if the task is not specific, the agent
will fill in the gaps during implementation. This way, we risk spending time
and tokens on something we don't need.

Instead, we should ask the AI assistant to fill these gaps before writing any
code. Then we review the specification, correct it, and hand it over to the
coding agent to implement it.

This process is called "grooming" - we groom a task to make it more specific.
Then an engineer can implement it without asking a single question.

In real teams, product managers usually do this work. So let's define that
role for our agent team.

Create a document:

```text
_docs/team/
  pm.md
```

Inside, write the description for the product manager agent:

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

A groomed task has four sections:

1. Goal - one or two sentences on what should be true afterwards.
2. Acceptance criteria - checkable statements.
3. Out of scope - what this change must not do.
4. Constraints - files it should stay inside, libraries it should or
   shouldn't use, prior decisions it has to follow.

We save the issue template as `_docs/task-template.md`:

```markdown
## Goal

One or two sentences on what should be true when this is done.

## Acceptance criteria

- [ ] A statement you can check by looking at the result
- [ ] One line per case, including the awkward ones

## Out of scope

- Something that does not belong in this task, moved to #TASK-NUMBER

## Constraints

- Files this should stay inside
- Libraries to use
- Guidelines to follow
```

We will need to groom every task, so let's add it to our `process.md`:

```markdown
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
```

Now we can start a new session and ask the agent to groom an issue:

```text
Groom issue #4
```

After it finishes, review the result. 

We can catch a misunderstanding most cheaply while grooming: the issue is a
paragraph, and correcting it costs one sentence. If we catch the same
misunderstanding after implementation, we need a rewrite.


## Loop engineering

We have groomed one issue. Next, we can groom the rest. We can ask the agent
to do it:

```text
Groom all GitHub issues. Process one issue at a time.
```

This will mostly work, but at some point the agent may stop and tell you
something like "I've groomed issues 1, 2 and 3. Do you want me to proceed?". 

The answer is almost always "yes", but the agent has stopped and is waiting for us
to explicitly say that. In many cases I want the agent to continue automatically. 

To do it, we can give the agent a goal:

```text
/goal groom all issues
```

The "/goal" command will prompt the agent to continue, so we won't need to do
it manually. Instead, we delegate it to the harness - the system around your agent like Claude Code or Codex. When the agent stops, the harness will check if the goal is met, and if it's not, it will resume working.

![The goal prompts the agent to continue](images/01-goal-is-not-met.png)

This approach is called "loop engineering". It's similar to a while loop:
we iterate over a loop until a condition is met. 

With loop engineering, we system runs a coding agent by itself
repeatedly instead of driving it manually prompt by prompt.

There are multiple "engineering" levels when we work with coding agents: 

- Prompt engineering - what we say when we interact with the agent
- Context engineering - what the agent knows before it starts and what it can get during the session
- Loop engineering - when it stops working
- Graph engineering - who does what when there's more than one agent (we'll talk about it later)

In June 2026 Addy Osmani published the
[Loop Engineering essay](https://addyo.substack.com/p/loop-engineering)
that gave it a name, and Peter Steinberger compressed the idea into one
sentence:

> stop prompting your agents and start designing the loops that
> prompt them.

TODO: add tweet URL here

The stop condition must be something the model can evaluate. "All issues
are groomed", "all tests pass" and "no file is over 200 lines" are checkable,
but "make the code better" is not. If the stop condition is not checkable,
the agent can stop too early or run forever.

Claude Code and Codex provide the `/goal` loop out of the box.
If your harness doesn't provide it, you can implement it yourself
using stop hooks. 


## Implementation: The software engineer agent

After grooming the issue, we can give it to a software engineer. This is the agent
who will do the actual coding.

Define the second role:

```text
_docs/team/
  software-engineer.md
```

Put this definition inside:

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

Add one more line to `process.md`:

```markdown
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
- Engineer - implements one groomed task, follows _docs/team/software-engineer.md
```

Then ask the agent to implement a task in a fresh session:

```text
Implement issue #2
```

The engineer stops when the code is written and its own tests pass.
But it's still too early to say that the task it properly implemented.
We need to test it.

## Testing: The QA engineer agent

An agent that writes the code and then judges this code is grading
its own homework.

If we ask "is this correct?" we'll get a definite "yes".
But the agent might have missed many edge cases.

In real word, we ask other people to validate our work. We have code reviews
and many teams have designated QA engineers whos focus is to
make sure the code is reliable. 

That's why we will also get a QA engineer to our team.

Let's the add third role:

```text
_docs/team/
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

Note: you may need to adjust this role to your project if you don't use uv and pytest.

And the last line in `process.md`:

```markdown
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
- Engineer - implements one groomed task, follows _docs/team/software-engineer.md
- QA - checks the result against the acceptance criteria, follows _docs/team/qa-engineer.md
```

Then, in a new session, ask:

```text
Test issue #2
```

If we get a `PASS`, it's great. If we get a `FAIL`, it's also good: 
we caught a regression. So we start a new engineer session, use the QA comment
as input, and ask to fix it. We iterate until QA says `PASS`.


## Graph engineering

We have three roles:

- Product manager grooms an issue
- Software engineer implements it
- QA engineer tests it, outputs `PASS` or `FAIL`

If QA says `FAIL`, the engineer will need to re-implement it. Otherwise, 
the task is done. 

We can visualize this process as a graph:

```text
groom (PM)  ->  implement (engineer)  ->  test (QA)  ->  done
                       ^                        |
                       +--------- FAIL ---------+
```

If we have an orchestrator that launches these agents automatically
instead of us doing it manually, we get "graph engineering".
We define a graph with specialized agents
as nodes and describe how the work goes from one to another. 

The term appeared on X around 18 July 2026, a month after loop
engineering, under the headline "Loop Engineering Is Dead".

TODO add link to tweet

I wouldn't call it a new idea though, and loop engineering is definitely not dead.
Even with graphs, we still need a loop to drive the work and orchestrate
it across multiple agents with different roles.

## The orchestrator

Let's implement it. For that we need the orchestrator.

Descibe it in `process.md`:

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

- Do not skip step 2
- The engineer does not close the issue
- QA does not fix the code, only outputs PASS or FAIL
```

We can now start a fresh session and lauch the loop:

```text
/goal work through the backlog
```

The agent reads `AGENTS.md`, finds `process.md`, follows the lifecycle,
and dispatches the agents according to the documents in `_docs/team/`. 

Because we combine it with a goal, the orchestrator runs until it's met. 

You can see the result in [`retroloop`](https://github.com/alexeygrigorev/retroloop).

Note: this approach takes significantly more time and tokens than a direct
loop with just sofware engineer. In many cases you don't need this complexity. 
Often a simple prompt or a simple loom is enough.

This tutorial is based on the process I have used for many projects like
[AI Shipping Labs website](link).
I describe it in [I Built an AI Agent Team for Software Development](https://alexeyondata.substack.com/p/i-built-an-ai-agent-team-for-software).
This is a distilled version from that article. 

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

You can find other materials for the course in the course repo:
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp).

It's free.

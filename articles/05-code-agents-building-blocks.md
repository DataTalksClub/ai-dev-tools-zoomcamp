# Coding Agent Building Blocks: Reusable Skills and Specialized Subagents

This is the fifth article in a series based on
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

All articles in the series:

- Part 1: [AI-Native Development: Specifications, Loop and Graph Engineering](https://aishippingblog.com/p/ai-native-development-specifications)
- Part 2: [Build and Ship a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with)
- Part 3: [Deploy a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/deploy-a-full-stack-app-with-ai-coding)
- Part 4: [DevOps and Observability for an AI-Built App](https://aishippingblog.com/p/devops-and-observability-for-an-ai)
- Part 5: Coding Agent Building Blocks: Reusable Skills and Specialized Subagents (this article)

In this article, I want to cover the two most important aspects of
working with coding assistants: skills and subagents.

- A skill describes how to perform a repeatable task.
- A subagent is an agent that runs in separate context with clear task instructions.

In addition, I'll cover my process for creating skills and show how to run multiple agents in parallel and turn your coding agent into a task orchestrator.

Getting these concepts is enough to work with coding agents productively, and you most likely won't need anything else.

This article is loosely based on a live workshop I did for the course. In the workshop, I had to improvise, so the content doesn't directly map to this article. But it's still going to be useful, so check it out.

https://www.youtube.com/watch?v=t8OrAjNO2Zs


## From Markdown Files to Skills and Subagents

In Part 1 of the course, [AI-Native Development: Specifications, Loop and Graph Engineering](https://aishippingblog.com/p/ai-native-development-specifications), we touched on both skills and subagents, but I didn't define them explicitly.

Specifically, we created a few documents:

- `_docs/process.md` and the other project documents contained
  reusable instructions (see [here](https://github.com/alexeygrigorev/retroloop/tree/main/_docs))
- `_docs/team/pm.md`, `_docs/team/software-engineer.md`, and
  `_docs/team/qa-engineer.md` described specialized roles for subagents (see [here](https://github.com/alexeygrigorev/retroloop/tree/main/_docs/team)).

I wanted to keep the discussion high-level and not focus on the mechanics of any specific implementation.

We didn't explicitly define them because we can tell a coding assistant:

```
Implement feature #101 following _docs/process.md
```

It will read the document and follow the steps there.

Or you can also speficy the role of the agent at the beginning of a session:

```text
You're a QA engineer. Your role is defined in `_docs/team/qa-engineer.md`. Review work for task #101.
```

Even better, you can ask it to start a subagent with this role:

```text
Start a QA engineer subagent. The role is defined in `_docs/team/qa-engineer.md`. Review work for task #101.
```

It will work. The coding assistant can just go read the file and do the task.

But if you define these things as skills and subagents explicitly, you'll be more effective in using them. In this article, I'll show you how.

Let's start with skills.

## Building Block 1: Skills

A skill is a structured set of instructions for a repeatable procedure.

If you need to follow a specific sequence of actions for completing a task, you can document the steps in a skill. Then later you can ask the agent to use this skill to perform a task. It will read the file and follow the steps from there.


### My Skills

I use skills a lot.

For example, one of my skills is for releasing a new vesion of a Python package. I maintain a lot of Python libraries that I need to regularly update and publish. I describe how I do it in [My PyPI Release Pipeline for Python Libraries](https://aishippingblog.com/p/my-pypi-release-pipeline-for-python).

It's a process with multiple steps:

- Run the tests
- Update the version in pyproject.toml
- Push the code to GitHib as a tag
- Verify that CI publishes the package

If I want to release a new version of [minsearch](https://aishippingblog.com/p/minsearch-the-small-search-library), I don't want to describe these steps each time I do it. Instead, I document this in a [release skill](https://github.com/alexeygrigorev/.agents/blob/main/skills/release/SKILL.md) and just say:

```text
release a new version
```

The agent understands what I need, read the skill, and follows the steps there.

<figure>
  <img src="images/05-release-skill.png" alt="A request to release minsearch prompts the coding agent to load the release skill and prepare version 0.2.0">
  <figcaption>The agent recognizes the release request and loads the relevant skill without an explicit skill command</figcaption>
</figure>

Internally, a skill is a markdown file that looks like that:

```markdown
---
name: release
description: Release a new version of the current project
---

Release

1. Inspect the project and determine its package registry.
2. Run the tests and other required checks.
3. Bump the version in the source of truth.
4. Commit the change and push a version tag.
5. Verify that the CI publishing job succeeds.
```

The main difference between a plain markdown file that we used previously and a skill is that the skill is automatically discoverable.

I can say:

```
Make a release. The process is described in _docs/release.md
```

And that will absolutely work. The agent will read the file, and follow the steps there.

However, with skills I don't need to say which file to use. The coding agent loads the list of skills into its context on the start time. When I need to release a library, it can see that there's a skill for that, so it goes ahead and uses it.

A skill is a markdown document, but in order to make it discoverable, we need to follow a convention:

- It must have a frontmatter section with name and description 
- It's saved in `.agents/skills/<NAME>/SKILL.md` 

And that's it - the rest is up to you. You can also add other markdown documents or scripts together with the `SKILL.md` file in the same directory and descride how the agent should use them. 

The [Agent Skills specification](https://agentskills.io/specification) describes
this structure and the format in more detail.

If you want to better understand how skills work, the best way is to build a small coding agent with skills. In the AI Shipping Labs workshop
[Build a Coding Agent with Tools, Skills and PydanticAI](https://aishippinglabs.com/workshops/coding-agent-v2) I show you how. We first learn about agents and function calls, and then see how to implement a special function for loading skills.


### Global Skills

There are some skills that all your projects need. But some are only needed for local work. 

Example of global skills:

- I use [`release`](https://github.com/alexeygrigorev/.agents/tree/main/skills/release) for releasing a new version of a library, [`init-library`](https://github.com/alexeygrigorev/.agents/tree/main/skills/init-library) to scaffold a new library or [`create-github-repo`](https://github.com/alexeygrigorev/.agents/tree/main/skills/create-github-repo) to create a GitHub repository
- I also [`fetch-youtube`](https://github.com/alexeygrigorev/.agents/tree/main/skills/fetch-youtube),
  [`fetch-loom`](https://github.com/alexeygrigorev/.agents/tree/main/skills/fetch-loom),
  and [`fetch-zoom`](https://github.com/alexeygrigorev/.agents/tree/main/skills/fetch-zoom),
  to fetch recordings or transcripts for the agent to analyze.
- For creating diagrams, I have a [`diagram-creator`](https://github.com/alexeygrigorev/.agents/tree/main/skills/diagram-creator) skills.

I use these skills across multiple projects, so it's better to make them global, so any agent on my computer can see and use them.

To create global skills, you need to put them in 

- `~/.codex/skills` for Codex
- `~/.claude/skills` for Claude
- other coding assistants have a similar structure

I use multiple assistants, so I want all of them to use the same skills. For that, I maintain one canonical copy of the skills in my
[`agents` repository](https://github.com/alexeygrigorev/.agents), and then create symlinks from there to `~/.codex/skills`, `~/.claude/skills` and other places. 


### Project-Specific Skills

Most skills are not useful globally though - they are project-specific.

For example, in my projects:

- [Course Management Platform](https://github.com/DataTalksClub/course-management-platform/tree/main/.agents/skills)
  has an [incident-response](https://github.com/DataTalksClub/course-management-platform/tree/main/.agents/skills/cmp-incident-response) skill. Every time there's an alert, it knows how to investigate and fix the problem, similar to what we covered in [Article 4](https://aishippingblog.com/p/devops-and-observability-for-an-ai).
- [DataTalks.Club FAQ](https://github.com/DataTalksClub/faq/tree/main/.agents/skills)
  has skills for fetching course questions from Slack and turning recurring
  questions into FAQ entries.

They work in the same way as global skills, but you place them in your project root:

- `./.agents/skills/` for all the assistants except Claude
- `./.claude/skills/` for Claude Code

It's annoying that Claude needs to have their own format - just like with `CLAUDE.md`. 

I solve this problem by creating a symlink from `.claude/skills/` to `.agents/skills/`.

I hope Anthropic starts listenining to their users and adopts the `.agents` convention too, so I can finally delete all these symlinks.


### Creating Skills

You don't need to create these skills manually. Coding assistants know the format, so you can ask them to create these skills.

However, I don't just start a session and say "create a skill for releasing a new version of this library". Usually, I do the task with the agent first, and see where I need to correct it.

We work together until the task is done, and then at the end I say:

```text
Save this as a skill. Cover the workflow we followed and keep all the corrections I made in mind, so the next agent can do the task correctly from the start.

This skill is specific to this project, so don't create a global skill.
```

If I don't include the last line, Codex will create a global skill, so I always have to add it. I didn't observe this behavior from other agents.

Improving an existing skill works in the same way. I trigger a skill, and if I see that something requires my intervention, I correct the agent. At the end of the session, I ask to update the process in the skill, so I don't have to do it next time.

## Building Block 2: Subagents

Most coding assistants allow you to start a session within a session. We usually call it "subagents" to make it clear that they are created inside your main coding session.

<figure>
  <img src="images/05-i-heard-you-like-prompts.jpg" alt="A meme reads, 'Yo dawg I heard you like agents, so I put an agent inside your agents, so you can prompt while you prompt'">
  <figcaption>Subagents let one coding agent prompt another agent inside its own session</figcaption>
</figure>

<figure>
  <img src="images/05-subagent-general.jpg" alt="A coding assistant shows a main session with a backgrounded general-purpose subagent grooming issue 69">
  <figcaption>The main session can keep working while a subagent handles a focused task in the background</figcaption>
</figure>

### Session Context

The context for a session is all the information the agent has about the current task and all the actions it has taken. 

In includes:

- AGENTS.md file
- Skills and tools definitions
- All the files it read 
- All the code it read and wrote 
- All the text you sent it and all the text it output 

That's a lot of information. As you go thought the session, and the session is getting longer, the agent starts "forgetting" things from the beginning. This is called "context rot".

That's why I start a new focused session for each task. In the article [From Idea to Production in 28 Prompts](https://aishippingblog.com/p/from-idea-to-production) I show the steps you need to take your idea to production, and recommend to start a new session for each of the steps.

Also, the current context will influence the future actions of the agent. If the agent implemented a feature, you shouldn't ask to test it in the same window. The implementation history will bias the agent and it can skip some checks. Instead, it's better to start a fresh session, and ask the agent there to check the work. 

### Agentic Team

This is what we did in Part 1 of the course, [AI-Native Development: Specifications, Loop and Graph Engineering](https://aishippingblog.com/p/ai-native-development-specifications). We defined multiple roles for our agentic team:

- Product manager (PM) - turns raw intake into specifications
- Software engineer (SWE) - based on the specifications implements the task
- QA engineer (QA) - validates that the task is implemeted correctly

Each of these agents live in a separate session: the context from SWE never gets into the QA session, so the QA engineer can independently test the system. 

If I have an issue #101 that's already groomed and I want to implement it, I can start a new session and say:

```text
You're a software engineer agent. Your role is described in `_docs/team/swe.md`. Work on issue #101.
```

But instead, I can also to launch it as a subagent:

```text
Launch a subagent to implement #101. Follow the process.
```

<figure>
  <img src="images/05-subagent-pm.jpg" alt="A coding assistant starts a PM agent to groom issue 69 in the background">
  <figcaption>A subagent can take on a specialized role, such as product-management work</figcaption>
</figure>

It will create a new agent with empty context (plus AGENTS.md) and automatically prompt it with something like that:

```
You're a software engineer. Your role is defined in `_docs/team/swe.md`.
Your task is to work on issue #101. Follow the process in `_docs/process.md
```

In some coding assistants you will also be able to look inside the subagent sessions. In others, you will only know that the subagent is doing something, but you won't know what exactly. 


### Defining Subagents

The coding assistant can read the agent definition from a markdown document (like `_docs/team/swe.md`) and launch a subagent. 

Just like with skills, you can also create a reusable and discoverable subaegnt definition. 

For example, for the software engineer, the definition could be:

```markdown
---
name: software-engieer
description: Use this agent to execute a well-scoped coding assignment.
---

Implement the assigned task, add or update tests, run the project checks, and
report the files changed and any remaining risks. Do not expand the scope.
```

Or even 

```markdown
---
name: software-engieer
description: Use this agent to execute a well-scoped coding assignment.
---

Read your role definition from _docs/team/swe.md
```


You put these definitions in:

- `.agents/agents/<NAME>.md` or 
- `.claude/agents/<NAME>.md` for Claude

You can also define subagents globally, but I never needed it. My subagents are always project-specific. 

Now you can ask:

```
Launch software engineer for #101
```

And it will start the software engineer agent

Note that for some coding agents like Claude you will have to restart a session to be able to discover the agent you just defined. 

### Orchestration Session

When you start using subagents, your main session becomes the orchestrator.

If have a process that we specify in `process.md`:

- PM grooms the issue 
- SWE implements it 
- QA checks it.
- If the issue passed the check, QA outputs `PASS`, otherwise `FAIL`
- If `FAIL`, SWE needs to reimplement it, until QA accepts it

This way we create a graph. 

This sequence needs to be enforced by something. Typically, we use the main coding session for that. 

If we descibe the process in our `process.md` document, and link it in `AGENTS.md`, then we can ask:

```text
Implement #101.
``` 

It will automatically run #101 through the PM -> SWE -> QA sequence, each step will run in its own fresh context, and the orchestrator will make sure that on `FAIL` the task goes to SWE who will fix the problems.

## Parallel Execution

In the first article, I only showed how to run this flow sequentially. And we can't have it in any other way: we always have to follow the PM -> SWE -> QA sequence.

But we can take care of multiple independent issues in parallel.

Our main agent is already the orchestrator, so it can run multiple subagents  in parallel. But we need to make sure that the agents aren't stepping on each other's toes.

For that we use git worktrees:

- For each new task create a new git worktree
- The agents work independently in these worktrees 
- You go though the entire PM -> SWE -> QA cycle in that worktree 
- When the cycle is ove rand the task is done, the orchestrator merges it back into main (alternatively you can have a conflict resolver agent)
- The worktree is deleted 

The orhcestrator's role here becomes more than just launching subagents in order.

It also needs to:

- keep track and status of each task
- schedule the agents
- create and merge worktrees 
- prevent logical conflicts by picking tasks that don't need to work on the same files 


<figure>
  <img src="images/05-parallel-worktrees.png" alt="The orchestrator assigns independent issues to as many as five isolated worktrees, then merges approved branches into main one at a time">
  <figcaption>Agents work concurrently in isolated worktrees while the orchestrator controls review and merge order</figcaption>
</figure>

To set it up, I put something like this in the `process.md` file:

```text
Work in isolated git worktrees and run up to five agents in parallel.

You are the orchestrator. Your job is to:

- Split the backlog into independent issue tracks.
- Give each agent a separate worktree and clear file ownership.
- Keep the agent slots full while eligible work remains.
- Send completed work to a fresh reviewer.
- Return review findings to the correct implementer.
- Merge approved work into the main branch one issue at a time.
- Coordinate the work. Never implement the issues yourself.
```

This is the approach I use for the majority of my projects.

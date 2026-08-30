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

# Release

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


## Global Skills

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


### Creating skills

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

A coding agent has a finite context window. In one session, it
plans, implements, and reviews a task. As that context fills, the agent can lose some important details. This is called "context rot".

That's why I often start each new task in a new session. This is also what I recommended in [From Idea to Production](https://aishippingblog.com/p/from-idea-to-production): start a new session for each of the 28 prompts.

Also, the actions that the agent has taken so far influence its future actions. If an agent implemented a feature, we don't want to ask the same agent to test it. Its implementation history can lead it to accept its own assumptions instead of checking the result independently against the specification.

In Article 1, I described the process:

- PM grooms an issue.
- SWE implements it.
- QA tests it and outputs `PASS` if everything is fine or `FAIL` if the task isn't done.
- If the result is `FAIL`, SWE needs to fix it.

If I have an issue #101 that's already groomed and I want to implement it, I can start a new session and say:

```text
You're a software engineer agent. Your role is described in `_docs/team/swe.md`. Work on issue #101.
```

But instead, I can have one main coding session that I'll treat as the orchestrator and ask it to launch the agent:

```text
Launch a subagent to implement #101. Follow the process.
```

It will create a new agent with an empty context and automatically prompt it. Some coding assistants also let you peek inside subagent sessions. With others, you only know that they are doing something, but you don't know exactly what.

Instead of launching only general-purpose agents, I can define reusable roles.
A simplified implementer definition looks like this:

```markdown
---
name: implementer
description: Use this agent to execute a well-scoped coding assignment.
model: implementation-model
---

Implement the assigned task, add or update tests, run the project checks, and
report the files changed and any remaining risks. Do not expand the scope.
```

Agent definitions can also select a model and restrict tools. I often use a
stronger reasoning model to audit a codebase or produce a plan, save that plan
in the repository, and hand it to a faster implementation agent. The model names
will change; the useful pattern is to separate analysis from execution.

I usually specify in my `process.md` document that the orchestrator should always run subagents, so my request could be:

```text
Implement #101.
``` 

It will automatically run #101 through the PM -> SWE -> QA sequence, and each step will run in its own fresh context.

Skills and subagents can be composed. For example, a `check-design` skill can
define the repeatable mechanics:

1. Start the application.
2. Open it in a browser at desktop and mobile sizes.
3. Capture screenshots.
4. Launch the designer subagent with the screenshots and the project's design
   system.
5. Save actionable findings for an implementer.

The skill preserves the sequence, the designer definition preserves the role,
and the fresh subagent context keeps the review independent.


## Parallel Subagents with Git Worktrees

In the first article, we run this sequentially. For one task, we can't do it in any other way: we have to keep the sequence from PM to SWE and from SWE to QA.

But we can take care of multiple independent issues in parallel.

For that, we need two concepts:

- Git worktrees
- The main session is the orchestrator

We need worktrees so agents can edit, test, and commit without
overwriting each other's changes.

The main session orchestrates everything: it keeps track of the status of each task, schedules the agents, and creates and merges worktrees. It also prevents logical conflicts. It can notice when two issues need to update the same files, so it's better not to run them in parallel because merging the changes will be difficult.



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
- Coordinate the work; do not implement the issues yourself.
```

I use this approach for most of my projects.


## Analysis and Implementation Models

I use skills and subagents to structure the work, and I choose models with the
same split in mind.

I pick models by role:

- For analysis, I use Fable or Sol. They read a spec, look at the current
  code, and produce a concrete plan before implementation starts.
- For implementation, I use Sonnet or Luna Max. Once the plan is clear, they
  write the code, run the checks, and fix what breaks.

These model names may change, but I keep the same split: analysis first,
implementation second. I can repeat both passes with skills. I run analysis
and verification passes in subagents so they don't inherit the implementer's
assumptions.


## Practical Takeaways

Keep these rules in mind when you structure your agent setup:

- Start with skills: identify repeated flows and encode them as Markdown
  playbooks
- Add subagents when context is a problem: if tasks are too large for a single
  agent session, break them into roles
- Keep skills simple: one flow per skill. If it branches, split it
- Give each subagent a fresh context window so details from another role don't
  interfere
- Build incrementally: start with one skill and one subagent. Add more as you
  discover what your flow needs
- Always verify: even the best models take shortcuts. I encode the "right way"
  in skills, and reviewer subagents catch what the implementer missed

## Resources

I use these resources for the course, workshop, and shared skills:

- [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) (free course)
- [Workshop 5: Coding Agent Capabilities](https://www.youtube.com/watch?v=t8OrAjNO2Zs)
- [Build a Coding Agent with Tools, Skills and PydanticAI](https://aishippinglabs.com/workshops/coding-agent-v2)
- [My agent configuration](https://github.com/alexeygrigorev/.agents) (shared skills for Claude Code, Codex, and OpenCode)

## Related Substack Articles

Read these for more detail on the examples:

- [How to Set Up Your Coding Agent](https://aishippingblog.com/p/how-to-set-up-your-coding-agent-a)
- [My Experiments with Claude Code](https://aishippingblog.com/p/my-experiments-with-agents-code)
- [AI-Native Development: Specifications, Loop and Graph Engineering](https://aishippingblog.com/p/ai-native-development-specifications)

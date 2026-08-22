---
title: "Coding Agent Building Blocks: Reusable Skills and Specialized Subagents"
created: 2026-02-17
updated: 2026-02-18
tags: [code-agents, skills, subagents, claude-code, ai-dev-tools-zoomcamp]
status: draft
---

# Coding Agent Building Blocks: Reusable Skills and Specialized Subagents

This is Article 5 in the [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) series. It focuses on two capabilities from Module 5 that make coding agents more reliable: reusable skills and specialized subagents.

The product around the agent can be an IDE, a terminal, or a hosted environment. That interface matters less than the workflow inside it. Skills make a good procedure repeatable. Subagents isolate focused work in fresh context and, when useful, run it in parallel.

## Running Example: The Telegram Writing Assistant

<figure>
  <img src="../../assets/images/code-agents-building-blocks/twa-github.png" alt="GitHub page of the Telegram Writing Assistant showing the README with logo and description">
  <figcaption>The Telegram Writing Assistant on GitHub: from scattered thoughts to publishable articles</figcaption>
</figure>

I use the [Telegram writing assistant](https://aishippingblog.com/p/telegram-assistant) as the running example.

It's a personal knowledge management system. I send voice messages, photos, links, and text to a Telegram bot throughout the day. The bot transcribes voice messages and stores everything in an inbox. When I type `/process`, a Claude Code agent reads the inbox and routes content to the correct article. It also fetches external URLs, verifies nothing was lost, and commits the result to Git.

This system uses both building blocks:

- Skills/commands: the [/process command](https://github.com/alexeygrigorev/telegram-writing-assistant/blob/main/.claude/commands/process.md) defines the full workflow for processing inbox materials
- Subagents: three specialized subagents handle URL research, resource descriptions, and content verification

<figure>
  <img src="../../assets/images/code-agents-building-blocks/telegram-process-command.png" alt="Telegram chat showing the /process command running: Read 35 files, Edited 16 files, Found 3 items, Launched 1 agents">
  <figcaption>The /process command reads 35 files, edits 16 articles, and launches research subagents</figcaption>
</figure>

The bot itself was built by Claude Code. I describe it in detail on [Substack](https://aishippingblog.com/p/telegram-assistant). Let me now show the two building blocks that make it work reliably.

## Building Block 1: Skills and Commands

Skills (also called playbooks or commands) are reusable, step-by-step workflows that encode best practices into repeatable procedures.

## What Are Skills?

A skill is a structured set of instructions that tells the agent exactly what to do for a specific type of task. Instead of giving the agent a vague instruction like "release this library," you give it a detailed playbook with every step spelled out.

## Skills vs Commands

In practice, there are two related concepts:

- Skills: agent-discovered workflows. The agent sees a list of available skills and autonomously decides when to load one. For example, when a user asks for a code review, the agent recognizes this matches the "review" skill and loads it.
- Commands: user-triggered shortcuts with `/command` syntax. When a user types `/release`, the system preprocesses this into a detailed prompt that the agent receives.

```mermaid
graph LR
    U1["User request"] --> A["Agent matches a listed skill"]
    A --> L["Agent loads the instructions"]
    L --> E1["Agent follows the workflow"]
    U2["User types /release"] --> R["System renders the command template"]
    R --> E2["Agent follows the workflow"]
```

Both encode reusable workflows. The difference is who initiates them: the agent (skills) or the user (commands).

In Claude Code, commands and skills are merged into a single system - both are markdown files in the `.claude/` directory, and the agent can discover skills while users trigger commands with `/name`. In other tools like [OpenCode](https://github.com/nicepkg/OpenCode), these may be separate systems with different configuration.

## How Skills Are Implemented

Skills are loaded automatically through a tool call. When an agent starts, it gets a list of all skill names and short descriptions. When a task comes in that matches a skill, the agent calls a `load_skill(name)` tool to get the full content. This is lazy loading - the agent only loads what it needs, keeping the context clean.

In the [agent-skills workshop](https://github.com/alexeygrigorev/workshops/tree/main/agent-skills), I built a coding agent with this exact mechanism. The `SkillsTool` class wraps a `SkillLoader` and exposes skill loading as a tool the agent can call:

<figure>
  <img src="../../assets/images/code-agents-building-blocks/skill-implementation.png" alt="Python code showing SkillsTool class that wraps SkillLoader and exposes skill() as a tool call returning name, description, and content">
  <figcaption>Skills implementation: a simple tool call that loads skill content on demand</figcaption>
</figure>

This is what makes skills powerful - the implementation is simple, yet it is now a standard pattern across most coding agents. Claude Code, GitHub Copilot, Codex CLI, and OpenCode all support skills or commands in some form.

## Examples from Practice

All my skills and commands are in a public GitHub repo: [github.com/alexeygrigorev/.claude](https://github.com/alexeygrigorev/.claude). Here are the ones I use most:

[/release](https://github.com/alexeygrigorev/.claude/blob/main/commands/release.md) - automates the full Python library release process:

- Run all tests to make sure nothing is broken
- Bump the version number using semantic versioning
- Build the package with [hatch](https://hatch.pypa.io/)
- Publish to [TestPyPI](https://test.pypi.org/) first
- Verify the package installs correctly from TestPyPI
- Publish to [PyPI](https://pypi.org/)
- Create a GitHub release with notes generated from the git log
- Group release notes by category: features, bug fixes, breaking changes
- Clean up build artifacts

Previously, I did this manually with some automation. Now the agent follows the playbook and handles everything.

[/init-library](https://github.com/alexeygrigorev/.claude/blob/main/commands/init-library.md) - creates new Python libraries with a consistent structure:

- Ask for library name, description, dependencies, and CLI preference
- Create the full file structure: `src/`, `tests/`, `pyproject.toml`, `Makefile`
- Set up [pytest](https://pytest.org/) for testing and [ruff](https://docs.astral.sh/ruff/) for linting
- Configure [hatch](https://hatch.pypa.io/) for building
- Add GitHub Actions CI/CD for Python 3.10-3.13
- Install dev dependencies with [uv](https://docs.astral.sh/uv/)

It was created by analyzing all my existing libraries ([minsearch](https://github.com/alexeygrigorev/minsearch), [toyaikit](https://github.com/alexeygrigorev/toyaikit)) to find common patterns. Libraries initialized this way follow the expected format for automated releases with `/release`.

[/create-github-repo](https://github.com/alexeygrigorev/.claude/blob/main/commands/create-github-repo.md) - handles creating GitHub repositories via the [GitHub CLI](https://cli.github.com/). Previously required going to the website, creating the repo, googling git commands. Now it asks for the name and handles everything.

[fetch-youtube](https://github.com/alexeygrigorev/.claude/tree/main/skills/fetch-youtube) - a skill (not a command) that fetches YouTube video transcripts. The agent discovers it when a user asks to process a YouTube link. Uses [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) to download timestamped subtitles.

<figure>
  <img src="../../assets/images/code-agents-building-blocks/command-process.png" alt="The /process command markdown file showing description and instructions for processing Telegram inbox">
  <figcaption>The /process command: a markdown file with step-by-step instructions for the agent</figcaption>
</figure>

[/process](https://github.com/alexeygrigorev/telegram-writing-assistant/blob/main/.claude/commands/process.md) - the Telegram writing assistant's main command.

This is the most complex skill I have:

- Pull latest changes from git
- Read all files from the inbox
- Categorize messages by theme and timing
- Route content to the correct article (or create a new one)
- Handle different content types: text, transcripts, URLs, images, videos
- For URLs: launch subagents to fetch and summarize content
- For GitHub URLs: use `gh` CLI instead of web fetching
- Preserve all voice message content verbatim (never summarize)
- Run a verification subagent to check nothing was missed
- Generate a summary of what was processed
- Move processed files from inbox/raw to inbox/used
- Create a git commit

The collection keeps growing. Each time I find myself repeating a workflow, it becomes a candidate for a new skill.

## Building Block 2: Subagents

When you start a Claude Code session, you interact with an agent. The agent is what takes your input and executes tasks - it can be a planner, an executor, a reviewer. The important thing to keep in mind is that agents have a context window. It is long but finite, and there is also context rot: the more context the agent uses, the worse it performs.

Consider the Telegram writing assistant. One of its tasks is to analyze an article or a YouTube transcript. These can be large - they go into the context window and occupy a significant portion of it. Once the agent finishes that one task and moves to the next, its memory is already overflowing. At some point it needs to run compaction, which essentially destroys the entire memory. The agent becomes less capable and needs to re-learn the context from a compressed summary.

This is where subagents help. A subagent is a separate agent that starts with a fresh context window. It does not occupy the main agent's context. I can tell it: "look at this article, summarize it, write the result to this file, and tell me when you're done." The main agent only sees "done" - none of the article content pollutes its context. The main agent stays focused on orchestrating the overall workflow, putting things in the right place, while the context-heavy work happens in isolation.

Subagents also enable parallelism. When you need to process multiple items (URLs, applications, batches) subagents can run in parallel while the main agent continues with other work.

There is also the problem of context rot. When an agent has a long session with many tasks, it starts forgetting things or accidentally skipping steps. This is why running a verifier as a separate subagent at the end of a flow is so helpful. When the main agent verifies itself, it tends to say "everything looks fine." But a fresh agent that starts with a clean context window is much better at catching what was missed or accidentally omitted.

## The Planner-Executor Pattern

The most common subagent pattern. First, the planner creates a detailed implementation plan. Then, for each step in the plan, a fresh executor agent handles the implementation.

<figure>
  <img src="../../assets/images/ai-engineer-my-vision/claude-code-backend-progress.jpg" alt="Claude Code showing a task list with checkmarks: restructure monorepo, initialize backend, implement database, implement API, implement AI service, update frontend">
  <figcaption>Planner-executor in action: Claude Code created a plan, then executes each step with progress tracking</figcaption>
</figure>

Why this works:

- A good plan from a strong model means even a weaker model can execute reliably
- Each execution step gets a clean context window
- Failed steps do not pollute the context of subsequent steps
- Progress is atomic - completed steps are committed, so failures do not lose work

## Subagents in the Telegram Writing Assistant

The Telegram writing assistant uses three subagents, each defined as a markdown file in [.claude/agents/](https://github.com/alexeygrigorev/telegram-writing-assistant/tree/main/.claude/agents):

<figure>
  <img src="../../assets/images/code-agents-building-blocks/subagent-article-summarizer.png" alt="The article-summarizer agent markdown file showing YAML frontmatter with name, description, tools, model fields and detailed instructions">
  <figcaption>The article-summarizer subagent: a markdown file with YAML frontmatter defining the agent's role, tools, and instructions</figcaption>
</figure>

[article-summarizer](https://github.com/alexeygrigorev/telegram-writing-assistant/blob/main/.claude/agents/article-summarizer.md) - deep analysis of URLs:

- Fetches content via [Jina Reader](https://jina.ai/reader/)
- Extracts key ideas, actionable patterns, code snippets, quotes
- Creates structured summaries with sections: overview, key insights, technical details
- Adds summaries to the correct research article
- Can run in parallel for multiple URLs

[resource-describer](https://github.com/alexeygrigorev/telegram-writing-assistant/blob/main/.claude/agents/resource-describer.md) - short descriptions for the [interesting resources](https://github.com/alexeygrigorev/telegram-writing-assistant/blob/main/articles/_interesting-resources.md) collection:

- Fetches content via Jina Reader
- Writes 2-4 sentence descriptions
- Inserts alphabetically into the resources article
- Can run in parallel for multiple resources

[verify-content](https://github.com/alexeygrigorev/telegram-writing-assistant/blob/main/.claude/agents/verify-content.md) - ensures nothing was lost during processing:

- Checks changed files via git diff
- Verifies all key ideas from text/transcript sources are present
- Confirms images exist and are placed correctly
- Flags any content that was improperly summarized
- Provides a verification report with issues found

```mermaid
graph LR
    M["Main agent: /process"] --> A["Article summarizer"]
    M --> R["Resource describer"]
    M --> V["Content verifier"]
    A --> C["Curated article changes"]
    R --> C
    V --> C
    C --> G["Reviewed Git commit"]
```

## Subagents for Batch Processing

For [reviewing 2,500+ scholarship applications](https://aishippingblog.com/p/how-i-reviewed-2500-ai-bootcamp-scholarship) for the AI Bootcamp, I used Claude Code with multiple commands running in parallel via subagents. Each subagent handled a batch of applications with consistent evaluation criteria defined in a markdown command file. The AI did preliminary screening, then I manually reviewed the top 50. This reduced the work from approximately two full days to 4-5 hours.

<figure>
  <img src="../../assets/images/code-agents-building-blocks/parallel-subagents-batches.png" alt="7 Task agents finished: Evaluate batches 1-6, 7-12, 38-42, 43-48, 49-54, 55-60, 65-69 - all Done with 11-20 tool uses each">
  <figcaption>7 parallel subagents evaluating scholarship application batches - each handles a batch independently</figcaption>
</figure>

## How to Create and Iterate on Skills

## Creating a New Skill

1. Interact with the agent and let it do the task
2. Observe how it behaves and correct it when it goes wrong
3. Go back and forth until the result is right
4. Tell the agent: "summarize all our discussion and all the corrections, and write them as a skill"
5. If the agent does not know the format, show it an example of an existing skill

If the project already has skills, the agent automatically follows the same format.

## Improving an Existing Skill

With the Telegram writing assistant, the `/process` command keeps getting better through use:

1. Trigger the command and let it run
2. When it does something wrong, correct it in the session
3. After fixing the issue, say: "analyze your actions and my corrections, and figure out what we should change in the process to avoid this in the future"
4. The agent analyzes everything and updates the command file

This way skills evolve through real usage. Each correction makes the next run better.

## Practical Takeaways

- Start with skills: identify repetitive workflows and encode them as markdown playbooks
- Add subagents when context is a problem: if tasks are too large for a single agent session, break them into roles
- Keep skills simple: one clear workflow per skill. If it branches, split it
- Fresh context is the key insight: the biggest improvement from subagents comes from giving each role a clean context window
- Build incrementally: start with one skill and one subagent. Add more as you discover what your workflow needs
- Always verify: even the best models take shortcuts. Skills encode the "right way" and subagent reviewers catch what the implementer missed

## Resources

- [AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp) (free course)
- [Agent Skills Workshop](https://github.com/alexeygrigorev/workshops/tree/main/agent-skills)
- [Coding Agent Workshop](https://github.com/alexeygrigorev/workshops/tree/main/coding-agent)
- [My Claude Code config](https://github.com/alexeygrigorev/.claude) (public repo with all skills and commands)
- [Telegram Writing Assistant](https://github.com/alexeygrigorev/telegram-writing-assistant) (the running example)

## Related Substack Articles

- [My Experiments with Claude Code](https://aishippingblog.com/p/my-experiments-with-claude-code)
- [Telegram Assistant](https://aishippingblog.com/p/telegram-assistant)
- [How I Reviewed 2,500 AI Bootcamp Scholarship Applications](https://aishippingblog.com/p/how-i-reviewed-2500-ai-bootcamp-scholarship)

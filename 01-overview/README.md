# Module 1 — AI-Native Developer Workflow

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what we are preparing, but the final videos, exercises, homework, and requirements may change before the cohort starts.

## Overview

This module gives students a practical map of the AI developer tooling landscape and a repeatable workflow for using these tools responsibly.

The framing for 2026 is **AI-native developer workflow**: use AI tools deliberately, with context, constraints, verification, and human review.

By the end of this module, you should be able to:

- choose between chat assistants, terminal coding agents, agentic IDEs, cloud agents, and project bootstrappers
- give an AI tool enough project context to work effectively
- complete a small feature with a disciplined AI development loop
- review AI-generated changes before accepting them
- document what you delegated to AI and how you verified it

## Tool Categories

### Chat Assistants

Examples:

- ChatGPT
- Claude
- Gemini
- Microsoft Copilot chat
- DeepSeek chat

Best for architecture discussion, explaining code, debugging ideas, design trade-offs, writing specs, reviewing pasted diffs, generating small snippets, and learning unfamiliar libraries.

### Terminal-Based Coding Agents

Examples:

- Claude Code
- Codex CLI
- Gemini CLI
- Aider

Best for working in an existing repo, multi-file edits, running tests, fixing lint/type errors, small refactors, debugging from logs, and creating commits.

### Agentic IDEs and Desktop Workbenches

Examples:

- Cursor
- Windsurf
- VS Code Copilot agent mode
- Zed agent panel
- Claude Code Desktop / Web
- Google Antigravity

Best for interactive coding, UI changes, exploring a repo visually, reviewing diffs, running an app, and browser-based checks.

### Cloud and GitHub-Native Agents

Examples:

- GitHub Copilot coding agent
- Codex cloud-style workflows
- Claude Code web/background sessions
- Devin-like tools

Best for assigning issues, background PRs, repo maintenance, documentation updates, and low-to-medium complexity tasks.

### Project Bootstrappers

Examples:

- Lovable
- Bolt
- Replit Agent
- v0-style UI generators

Best for fast prototypes, landing pages, CRUD apps, UI mockups, demo apps, and first drafts of frontend code.

## Lessons

### Lesson 1.1 — The AI Tool Landscape

Goal: understand the main tool categories and when each category is useful.

Exercise: classify 10 tools into categories and explain when you would use each one.

### Lesson 1.2 — The Same Task in Different Tool Styles

Goal: see how tool choice changes the workflow.

Task:

- add a leaderboard filter
- update a UI label
- fix one failing test
- update the README

Try at least two approaches:

- chat assistant
- terminal agent
- agentic IDE
- bootstrapper

Deliverable:

```text
docs/tool-comparison.md
```

### Lesson 1.3 — The AI Development Loop

Use this loop for AI-assisted development:

```text
spec -> context -> plan -> edit -> run -> test -> inspect diff -> review -> commit
```

Important habits:

- start with a small specification
- ask for a plan before broad edits
- ask what files will change
- make small commits
- review the diff
- run deterministic checks

### Lesson 1.4 — Context Engineering

Context engineering means making the project understandable to agents:

- make conventions explicit
- make commands discoverable
- make constraints visible
- make review criteria repeatable

Useful files:

```text
AGENTS.md
CLAUDE.md
.github/copilot-instructions.md
.cursor/rules
product-spec.md
architecture.md
testing.md
security-checklist.md
openapi.yaml
runbook.md
```

### Lesson 1.5 — Human-in-the-Loop Review

Topics:

- reviewing diffs
- checking unrelated changes
- detecting over-editing
- checking tests
- checking generated dependencies
- checking auth and secrets
- checking CI/deployment changes
- knowing when to stop the agent

Deliverable:

```text
docs/ai-usage-report.md
```

## Module Deliverables

At the end of Module 1, your repo should include:

```text
docs/tool-comparison.md
docs/ai-usage-report.md
AGENTS.md or equivalent project instructions
one small reviewed AI-assisted feature
```

## Previous Cohort Materials

The previous version of this module is archived here:

- [2025 archived Module 1](../cohorts/2025/01-overview/)
- [2026 homework](../cohorts/2026/01-overview/homework.md)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

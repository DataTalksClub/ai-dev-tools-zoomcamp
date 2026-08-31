# Module 5 — Coding Agent Capabilities: MCP, Skills, Plugins, and Custom Agents

## Overview

This module is about how modern coding agents are extended, customized, constrained, shared, and audited.

It is not a module about one specific coding tool. The examples can use a concrete environment, but the concepts should transfer across modern agentic coding systems such as Claude Code, Codex, OpenCode, Cursor, GitHub Copilot, Aider, Windsurf, and future tools.

The durable mental model:

```text
instructions
context
tools
permissions
reusable workflows
specialized agents
packaging and sharing
custom agent loops
audit trail
```

Different products use different names for these capabilities. For example, one tool may call a reusable workflow a skill, another may call it a command, prompt, rule, recipe, or extension. The course should teach the capability first and the product-specific syntax second.

You will:

- Understand the agent loop — context gathering, planning, tool calls, edits, tests, and iteration to a diff or PR — by pointing an agent at your Module 2/3 app and having it plan and ship a small feature
- Write portable project instructions (AGENTS.md, CLAUDE.md, or equivalent) covering architecture, commands, conventions, and security boundaries so any agent can reuse them
- Use MCP to expose a scoped set of tools, resources, and prompts to an agent, rather than giving it access to everything
- Turn a checklist or procedure you keep repeating into a reusable workflow — a skill, slash command, rule, or recipe depending on the tool
- Add hooks and guardrails so formatting, linting, and safety checks are automatic instead of relying on "please be careful"
- Build specialized subagents with scoped context and permissions for side tasks like API review, debugging, or testing
- Package shared configuration as a plugin or extension when it needs to move across teams or projects, not just live in one repo
- Decide when to build a custom agent — for CI/CD, scheduled jobs, or structured pipelines — instead of using an interactive coding agent

Module summary: The companion article covers two building blocks for working with coding
agents: reusable skills for procedures you keep repeating, and specialized
subagents that run in their own isolated context instead of polluting the main
session. It shows how to combine both with git worktrees so several agents can
work on separate tasks in parallel, with the main session acting as an
orchestrator that follows a defined process.

[Read the article: Coding Agent Building Blocks: Reusable Skills and Specialized Subagents](https://aishippingblog.com/p/coding-agent-building-blocks-reusable)

## Module Deliverable: Agent Extension Pack

Students extend the app they built in Modules 2 and 3 with an agent extension pack.

Minimum requirements:

```text
1 project instructions file
1 reusable workflow/skill/command
1 specialized subagent
1 MCP tool/server
1 hook or guardrail
1 small plugin/extension package OR custom agent
1 permission/security note
```

Suggested repo structure:

```text
AGENTS.md
CLAUDE.md or equivalent tool-specific instructions

agent-capabilities/
  review-api-change/
  debug-ci-failure/
  subagents/

agent-hooks/

mcp-server/
  server.py
  README.md

plugins/
  ai-devtools-agent-pack/

custom-agent/
  agent.py
  README.md

docs/
  agent-extension-pack.md
  permissions.md
  demo.md
```

Demo script:

1. The agent reads the project instructions.
2. A reusable workflow is invoked.
3. A specialized subagent reviews an API change.
4. The agent calls an MCP tool.
5. A hook or guardrail prevents, formats, checks, or logs an action.
6. The student reviews the final diff.

## Homework

> [!IMPORTANT]
> Module 5 has no graded homework. Complete the [Agent Extension Pack](#module-deliverable-agent-extension-pack) above and carry it into your [final project](../project/) instead.

## Previous Cohort Materials

The previous MCP-focused version of this module is archived here:

- [2025 archived Module 3](../cohorts/2025/03-mcp/)
- [MCP client configuration notes](clients.md)

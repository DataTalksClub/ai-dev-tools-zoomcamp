# Module 3 — Coding Agent Capabilities: MCP, Skills, Plugins, and Custom Agents

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what we are preparing, but the final videos, exercises, homework, and requirements may change before the cohort starts.

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

## Lessons

### Lesson 3.1 — How Coding Agents Work

Goal: understand the agent loop.

Concepts:

```text
user goal
context gathering
planning
tool calls
file edits
command execution
test execution
result inspection
iteration
diff/PR output
```

Lab: use the Module 2 app and ask an agent to:

- understand the repo
- summarize the architecture
- find test commands
- identify app entry points
- propose one small feature
- make a plan
- implement it
- run tests
- show the diff

Deliverables:

```text
docs/agent-workflow-notes.md
AGENTS.md or equivalent project instructions
```

### Lesson 3.2 — Project Instructions and Context Engineering

Goal: create project-level context that agents can reuse.

Useful files:

```text
AGENTS.md
CLAUDE.md
.github/copilot-instructions.md
.cursor/rules
docs/architecture.md
docs/testing.md
docs/agent-rules.md
docs/security-notes.md
```

The exact file names depend on the tool. The content should be portable:

- project overview
- stack and architecture
- commands for setup, tests, linting, and deployment
- coding conventions
- API contract rules
- review checklist
- security and permission boundaries

### Lesson 3.3 — MCP as One Integration Capability

Goal: teach MCP as a tool/context protocol, not as the whole module.

Concepts:

```text
MCP host/client/server
tools
resources
prompts
stdio transport
HTTP transport
remote vs local servers
project vs user config
approval and permissions
```

App-specific MCP server idea:

```text
tools:
  get_leaderboard
  get_recent_games
  create_bug_report
  run_backend_tests
  run_frontend_tests

resources:
  openapi.yaml
  product-spec.md
  latest-test-results.json

prompts:
  review-api-change
  generate-release-summary
```

Deliverables:

```text
mcp-server/
  server.py
  README.md
docs/mcp-tools.md
```

Teaching point: MCP should expose useful capabilities with safe boundaries. It should not mean giving the agent access to everything.

### Lesson 3.4 — Reusable Workflows: Skills, Commands, Rules, and Recipes

Goal: teach when repeated instructions should become a reusable capability.

Create one when you repeatedly paste the same:

- checklist
- review procedure
- debugging procedure
- deployment procedure
- project-specific convention
- multi-step workflow

Good course examples:

```text
review-api-change
debug-ci-failure
add-backend-endpoint
add-frontend-component
prepare-pr
check-generated-code
deploy-staging
```

Depending on the tool, this may be implemented as a skill, slash command, prompt, rule, recipe, script, or plugin extension.

Deliverables:

```text
agent-capabilities/review-api-change/
agent-capabilities/debug-ci-failure/
docs/reusable-workflows.md
```

### Lesson 3.5 — Hooks and Guardrails

Goal: show that agent workflows can be controlled and automated.

Hook and guardrail use cases:

- auto-format after edits
- run a linter after relevant file changes
- block dangerous shell commands
- block editing CI/CD files without confirmation
- log every shell command
- notify when a long task finishes
- run tests before commit

Deliverables:

```text
agent-hooks/
docs/hooks-and-guardrails.md
```

Teaching point: hooks turn "please be careful" into repeatable guardrails.

### Lesson 3.6 — Specialized Subagents

Goal: teach specialized agents with scoped context and permissions.

Subagents are useful when a side task would pollute the main context with logs, search results, or file contents.

Course subagents:

```text
api-contract-reviewer
debugger
browser-tester
security-reviewer
database-query-validator
release-note-writer
```

Deliverables:

```text
agent-capabilities/subagents/
docs/subagents.md
```

Teaching point: subagents are a permission and context management tool, not just a multi-agent feature.

### Lesson 3.7 — Plugins and Extension Packaging

Goal: teach when standalone project configuration should become a shareable package.

Use project-local configuration for:

- one project
- personal workflows
- experiments
- short local commands

Use plugins or extension packages for:

- team sharing
- versioned releases
- cross-project reuse
- community distribution
- namespaced commands and reusable capabilities

Deliverables:

```text
plugins/ai-devtools-agent-pack/
docs/plugin-usage.md
```

### Lesson 3.8 — Creating Custom Agents

Goal: teach when to build a custom agent instead of using an interactive coding agent.

Use a custom agent when you need:

- CI/CD integration
- a custom internal app
- scheduled automation
- team-specific workflow
- controlled tool access
- structured output
- a repeatable pipeline

Deliverables:

```text
custom-agent/
  agent.py
  README.md
docs/custom-agent-design.md
```

## Module Deliverable: Agent Extension Pack

Students extend their Module 2 app with an agent extension pack.

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

## Previous Cohort Materials

The previous MCP-focused version of this module is archived here:

- [2025 archived Module 3](../cohorts/2025/03-mcp/)
- [MCP client configuration notes](clients.md)
- [2026 homework](../cohorts/2026/03-mcp/homework.md)

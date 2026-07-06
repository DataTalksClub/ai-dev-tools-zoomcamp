# AI Dev Tools Zoomcamp 2026 Syllabus Proposal

**Prepared for:** DataTalks.Club / AI Dev Tools Zoomcamp  
**Date:** 2026-07-05  
**Status:** Draft proposal for discussion with instructors and contributors  
**Recommended course name:** **AI Dev Tools Zoomcamp: AI-Native Software Engineering**

---

## 1. Executive summary

The current AI Dev Tools Zoomcamp already has strong ingredients: a practical overview of AI developer tools, a full-stack end-to-end build, MCP, coding agents, CI/CD, and low-code automation. For the 2026 version, the course should be reframed around a more durable developer workflow:

> **Choose the right AI tool, give it the right context, extend it with the right capabilities, and ship safely with review, audit, security, and DevOps controls.**

The recommended 2026 course structure has **four modules**:

1. **AI-Native Developer Workflow**  
   Compare the main categories of AI developer tools and teach context engineering.

2. **Build and Ship an AI-Assisted Full-Stack App**  
   Keep the strong end-to-end app-building module: product spec, frontend, OpenAPI, backend, database, Docker, deployment, and CI/CD.

3. **Coding Agent Capabilities: MCP, Skills, Plugins, and Custom Agents**  
   Convert the old MCP-centered module into a broader module on extending and customizing coding agents. MCP becomes one capability alongside reusable workflows, hooks, subagents, plugins/extensions, and custom agents. The module should be tool-agnostic first; Claude Code, Codex, OpenCode, Cursor, GitHub Copilot, Aider, and similar tools can be used as examples.

4. **Open-Source AI Tools for Security, Audit, and DevOps**  
   Restrict this module to open-source AI-oriented security/audit/DevOps tools, because this is the area where we need a curated stack. No LLM evals. No general coding agents. No test-generation module. Focus on PR audit, security-tool orchestration, MCP/agent security scanning, Kubernetes diagnostics, incident investigation, and AI tool governance.

The course story becomes:

```text
Module 1: Learn the AI tool landscape and context engineering
Module 2: Build and deploy a real app with AI assistance
Module 3: Extend coding agents around the app
Module 4: Audit, secure, and operate the AI-assisted workflow
```

---

## 2. Course design principles

### 2.1 The course should teach workflows, not tool worship

Tools change quickly. The course should still mention important tools, but the durable skill is knowing which tool category fits the job.

For example:

```text
Use chat assistants when you need thinking, explanation, design, or review.
Use terminal agents when you need repo edits and command execution.
Use agentic IDEs when you need interactive coding inside an editor.
Use bootstrappers when you need prototypes quickly.
Use agent extension capabilities when a repeated workflow should become a reusable skill/tool/agent.
Use security/audit/DevOps AI tools when code is ready to be reviewed, diagnosed, or operated.
```

### 2.2 The course should be practical and repo-centered

Each module should produce files in the learner’s repo. This makes the work visible and reviewable.

A final project repo should include artifacts like:

```text
AGENTS.md
CLAUDE.md
product-spec.md
openapi.yaml
docker-compose.yml
.github/workflows/
agent-capabilities/
agent-hooks/
mcp-server/
security/
ops/
docs/
```

### 2.3 Module 3 should be tool-agnostic first

Module 3 should teach coding agent capabilities in a generic way. Concrete demos can use one or more tools, but the concepts should not depend on a single product:

```text
instructions
context
tools
permissions
reusable workflows
specialized agents
extension packaging
custom agent loops
audit trails
```

Different tools use different names for these capabilities. For example, one tool may call a reusable workflow a skill, another may call it a command, rule, recipe, prompt, or extension. This keeps the module useful for people who use Claude Code, Codex, OpenCode, Cursor, GitHub Copilot, Aider, Windsurf, Zed, Antigravity, or future tools.

### 2.4 Module 4 should be narrower and stricter

For Module 4, the constraint is intentional:

```text
Only open-source AI tools.
Only security / audit / DevOps.
No general coding agents.
No LLM application evals.
No test generation as the main topic.
```

This keeps the module focused and avoids duplicating Modules 1–3.

---

## 3. High-level 2026 syllabus

### Module 1: AI-Native Developer Workflow

Compare modern AI developer tools: chat assistants, terminal coding agents, agentic IDEs / desktop workbenches, cloud agents, and project bootstrappers. Learn how to choose the right tool for a task and how to give AI tools useful project context.

**Outcome:** configure a repo for AI-assisted development and complete one small feature using a disciplined AI workflow.

### Module 2: Build and Ship an AI-Assisted Full-Stack App

Build an end-to-end application with AI assistance: product spec, frontend prototype, OpenAPI contract, FastAPI or Django backend, database, tests, Docker, deployment, and CI/CD.

**Outcome:** a deployed full-stack app with tests, Docker setup, OpenAPI contract, and a reproducible development workflow.

### Module 3: Coding Agent Capabilities: MCP, Skills, Plugins, and Custom Agents

Learn how modern coding agents are extended and customized. Cover project instructions, MCP, reusable workflows/skills, hooks, specialized subagents, plugins/extensions, and custom agents in a tool-agnostic way, with concrete examples from modern coding agents.

**Outcome:** an agent extension pack for the Module 2 app, including project instructions, a custom skill, a subagent, a hook, an MCP tool/server, and either a small plugin or a custom agent.

### Module 4: Open-Source AI Tools for Security, Audit, and DevOps

Learn how to use open-source AI tools around the production workflow. Focus on AI PR audit, AI-accessible security scanning, agent/MCP/skill security scanning, Kubernetes diagnostics, incident investigation, and AI tool governance.

**Outcome:** a security/audit/DevOps hardening package for the final project, including PR audit output, Semgrep MCP findings, Agent Scan report, K8sGPT diagnosis, optional HolmesGPT incident summary, and an AI tool/data policy.

---

# Module 1 — AI-Native Developer Workflow

## 4. Module 1 positioning

The current “vibe coding” framing should be toned down. It is fine to mention vibe coding as a cultural term, but the course identity should be more professional:

> **AI-native developer workflow**: use AI tools deliberately, with context, constraints, verification, and human review.

The key problem Module 1 solves:

```text
Developers are overwhelmed by tools.
They do not know when to use chat vs terminal vs IDE vs bootstrapper.
They do not know how to give the tool enough context.
They do not know how to review AI-generated changes.
```

Module 1 should provide the map.

---

## 5. Tool categories for Module 1

### 5.1 Chat assistants

**Examples**

```text
ChatGPT
Claude
Gemini
Microsoft Copilot chat
DeepSeek chat
```

**Best for**

```text
architecture discussion
explaining code
debugging ideas
design trade-offs
writing specs
reviewing pasted diffs
generating small snippets
learning unfamiliar libraries
```

**Weaknesses**

```text
weak repo awareness unless context is pasted/uploaded
easy to produce plausible but unverified answers
manual copy/paste between chat and repo
not ideal for multi-file edits
```

**Teaching demo**

Ask three chat assistants to solve the same task:

```text
"Here is a small FastAPI endpoint and its failing test. Explain the bug, propose a fix, and suggest one additional test."
```

Then compare:

```text
quality of reasoning
specificity of the fix
test suggestions
hallucinated assumptions
need for repo context
```

---

### 5.2 Terminal-based coding agents

**Examples**

```text
Claude Code
Codex CLI
Gemini CLI
Aider
```

**Best for**

```text
working in an existing repo
multi-file edits
running tests
fixing lint/type errors
small refactors
debugging from logs
creating commits
```

**Weaknesses**

```text
can run commands and modify many files
requires permission discipline
must review diffs frequently
can over-edit if instructions are vague
may spend tokens/cost on irrelevant context
```

**Teaching demo**

Use the same repo task as chat assistants:

```text
"Add a leaderboard filter, update the tests, run the tests, and show the diff."
```

Compare:

```text
how it finds relevant files
how many files it edits
how it runs tests
how easy the diff is to review
```

---

### 5.3 Agentic IDEs / desktop agent workbenches

This is the best name for the “desktop tools” category.

**Examples**

```text
Cursor
Windsurf
VS Code Copilot agent mode
Zed agent panel
Claude Code Desktop / Web
Google Antigravity
Z.ai ZCode
Anthropic Cowork-style graphical agents
```

**Notes**

- Some tools in this category are full IDEs.
- Some are desktop or web workbenches.
- Some are graphical versions of terminal agents.
- Some are more “agent managers” than editors.

The category matters more than the exact list. The 2026 course should teach learners to ask:

```text
Does this tool see my repo?
Can it edit files?
Can it run commands?
Can it use the browser?
Can it show a diff?
Can it make a PR?
Can I control permissions?
Can I understand what context it used?
Can I control cost?
```

**Best for**

```text
interactive coding
UI changes
exploring a repo visually
reviewing diffs
running app and browser checks
working with project files and terminal together
```

**Weaknesses**

```text
editor lock-in
hidden context behavior
rate-limit/pricing surprises
too much autonomy if not reviewed
tool behavior changes quickly
```

---

### 5.4 Cloud / GitHub-native agents

**Examples**

```text
GitHub Copilot coding agent
Codex cloud-style workflows
Devin-like tools
Claude Code web/background sessions
```

**Best for**

```text
assigning issues
background PRs
repo maintenance
documentation updates
low-to-medium complexity tasks
```

**Weaknesses**

```text
asynchronous review burden
unclear ownership
governance and auditability
cost
CI and permission boundaries
```

This category should be mentioned in Module 1 but not necessarily used as a required lab.

---

### 5.5 Project bootstrappers

**Examples**

```text
Lovable
Bolt
Replit Agent
v0-style UI generators
```

**Best for**

```text
fast prototypes
landing pages
CRUD apps
UI mockups
demo apps
first draft of frontend
```

**Weaknesses**

```text
generated code may be messy
architecture may not match production needs
must migrate into a normal repo workflow
can hide complexity behind prompts
```

Module 2 should use this category practically.

---

## 6. Module 1 content flow

### Lesson 1.1 — The AI tool landscape

**Goal:** give students a map.

**Topics**

```text
chat assistants
terminal agents
agentic IDEs / desktop workbenches
cloud agents
bootstrappers
AI PR/review tools
security/audit/DevOps AI tools
```

**Exercise**

Students classify 10 tools into categories and say when they would use each.

---

### Lesson 1.2 — The same task in four tool styles

**Goal:** show how tool choice changes workflow.

**Task**

```text
Add a small feature to a simple repo:
- add a leaderboard filter
- update a UI label
- fix one failing test
- update README
```

Students try at least two approaches:

```text
chat assistant
terminal agent
agentic IDE
bootstrapper
```

**Deliverable**

```text
docs/tool-comparison.md
```

Template:

```markdown
# Tool comparison

## Task

## Tool 1

- What I asked
- What it did well
- What it got wrong
- How I verified it

## Tool 2

- What I asked
- What it did well
- What it got wrong
- How I verified it

## Recommendation

For this kind of task, I would use...
```

---

### Lesson 1.3 — The AI development loop

Teach a repeatable loop:

```text
spec
→ context
→ plan
→ edit
→ run
→ test
→ inspect diff
→ review
→ commit
```

Emphasize:

```text
do not start with "build the whole thing"
start with a small specification
ask for a plan
ask what files will change
make small commits
review the diff
run deterministic checks
```

---

### Lesson 1.4 — Context engineering

This should be one of the most important lessons.

**Files to introduce**

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

**Key idea**

Context engineering is not “write a better prompt.” It is:

```text
make the project understandable to agents
make conventions explicit
make commands discoverable
make constraints visible
make review criteria repeatable
```

---

### Lesson 1.5 — Human-in-the-loop review

**Topics**

```text
reviewing diffs
checking unrelated changes
detecting over-editing
checking tests
checking generated dependencies
checking auth and secrets
checking CI/deployment changes
knowing when to stop the agent
```

**Deliverable**

```text
docs/ai-usage-report.md
```

Template:

```markdown
# AI usage report

## What I delegated

## What I reviewed manually

## What I rejected

## What tests prove it works

## What I would not let the agent do automatically

## Cost / limits / friction

## What I learned
```

---

# Module 2 — Build and Ship an AI-Assisted Full-Stack App

## 7. Module 2 positioning

Module 2 is already strong and should remain the backbone of the practical course. It should take students from idea to deployed app.

The current Snake app structure is still a good choice because it is visual, interactive, and small enough to complete while still requiring frontend, backend, API, database, tests, Docker, deployment, and CI/CD.

---

## 8. Module 2 content flow

### Lesson 2.1 — Product spec and acceptance criteria

Before using a bootstrapper, students write:

```text
product-spec.md
user stories
acceptance criteria
non-goals
technical constraints
```

Example:

```markdown
# Product spec

## App

Snake Arena

## Users

- anonymous visitor
- registered player
- admin / maintainer

## Features

- play snake
- register/login
- leaderboard
- watch simulated games
- submit score

## Non-goals

- real-time multiplayer in this version
- payment
- social login

## Acceptance criteria

- user can play a local game
- user can submit score
- leaderboard shows top scores
- app works locally with Docker Compose
- backend tests pass
- frontend smoke test passes
```

---

### Lesson 2.2 — Frontend prototype

**Tools**

```text
Lovable
Bolt
Replit Agent
Cursor / Claude Code / Codex as fallback
```

**Goal**

Generate an initial frontend, then pull it into a normal repo workflow.

**Teaching point**

The prototype is not the final product. It is a first draft.

---

### Lesson 2.3 — OpenAPI contract

Students extract or write:

```text
openapi.yaml
```

Teach:

```text
API-first development
contract between frontend and backend
schema validation
generated clients/servers
how AI can hallucinate endpoints
```

---

### Lesson 2.4 — Backend implementation

**Options**

```text
FastAPI
Django
Node/Express
```

The default should probably remain FastAPI because it fits the current material.

**Topics**

```text
backend scaffolding
uv dependency management
OpenAPI-guided implementation
mock DB first
tests first for key endpoints
```

---

### Lesson 2.5 — Database support

**Topics**

```text
SQLite for local tests
Postgres for Docker/production
SQLAlchemy or Django ORM
migrations
integration tests
```

---

### Lesson 2.6 — Containerization

**Deliverables**

```text
Dockerfile
docker-compose.yml
.env.example
```

---

### Lesson 2.7 — Deployment

**Options**

```text
Render
Fly.io
Railway
Cloud Run
```

Keep the default simple.

---

### Lesson 2.8 — CI/CD

**Required**

```text
backend tests
frontend tests
integration tests if feasible
build check
deployment trigger
```

---

## 9. Module 2 deliverable

At the end of Module 2, each student should have:

```text
/product-spec.md
/AGENTS.md
/CLAUDE.md or equivalent
/frontend
/backend
/openapi.yaml
/docker-compose.yml
/tests
/.github/workflows
/docs/ai-usage-report.md
```

The app should be deployed and the repository should be reproducible.

---

# Module 3 — Coding Agent Capabilities: MCP, Skills, Plugins, and Custom Agents

## 10. Module 3 positioning

This module should incorporate the co-instructor’s suggestion, but keep the module generic:

> “Maybe we can convert Module 3 with a bit more of coding agent capabilities: MCP, skills, plugins, creating custom agents. I use Claude extensively, so the topics are aligned towards that.”

That is the right direction for examples and instructor experience, but the course should not become a Claude-specific module.

The old module should no longer be “MCP deep dive.” Instead:

> **Module 3 teaches how coding agents are extended, customized, constrained, and integrated into real developer workflows.**

MCP remains important, but it becomes one part of the larger capability stack.

---

## 11. Module 3 mental model

Every coding agent capability fits into one of these buckets:

```text
Instructions: What should the agent know and follow?
Context: What files, docs, schemas, and state can it see?
Tools: What can it do?
Permissions: What is it allowed to do automatically?
Workflows: What repeated procedures can be packaged?
Specialists: Which subagents handle specific tasks?
Distribution: How do teams share agent capabilities?
Custom agents: When do we build our own agent loop?
Audit: What did the agent do and why?
```

Concrete tools provide different implementations of these concepts. Examples can include:

```text
project instructions        AGENTS.md, CLAUDE.md, repo rules, editor instructions
tool/context protocols      MCP, built-in tools, extension APIs
reusable workflows          skills, commands, prompts, recipes, rules
hooks and guardrails        lifecycle automation, command checks, formatting, logging
specialized agents          subagents, specialist agents, reviewer agents
extension packaging         plugins, extensions, shared config packs
custom agent loops          SDKs, scripts, CI jobs, internal apps
```

---

## 12. Module 3 lesson flow

## Lesson 3.1 — How coding agents work

### Goal

Teach the agent loop.

### Concepts

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

### Lab

Use the Module 2 app. Ask a coding agent to:

```text
understand the repo
summarize architecture
find test commands
identify app entry points
propose one small feature
make a plan
implement it
run tests
show the diff
```

### Deliverables

```text
docs/agent-workflow-notes.md
AGENTS.md or equivalent project instructions
```

---

## Lesson 3.2 — Context engineering for coding agents

### Goal

Move beyond generic prompting and create project-level context.

### Files to add

```text
CLAUDE.md
AGENTS.md
docs/architecture.md
docs/testing.md
docs/agent-rules.md
docs/security-notes.md
```

### Example project instructions

```markdown
# Project context

This is a full-stack Snake app with a React frontend, FastAPI backend, PostgreSQL in production, and SQLite for tests.

# Development rules

- Use uv for Python dependency management.
- Use npm for frontend dependencies.
- Always run backend tests before changing API behavior.
- Do not modify CI/CD without asking.
- Do not introduce new dependencies unless justified.
- Prefer small, reviewable diffs.

# Testing

- Backend: uv run pytest
- Frontend: npm test
- Integration: docker compose up --build

# API contract

- The source of truth is openapi.yaml.
- If backend routes change, update openapi.yaml.
- If frontend API calls change, check openapi.yaml.

# Review checklist

- Is the OpenAPI contract still valid?
- Are errors handled?
- Are tests updated?
- Are there unrelated changes?
- Did the change affect auth, secrets, CI, or deployment?
```

### Teaching point

`AGENTS.md`, `CLAUDE.md`, editor rules, or equivalent project instructions should contain durable project facts and rules. Repeated procedures should later become reusable workflows such as skills, commands, prompts, rules, or recipes.

---

## Lesson 3.3 — MCP as one integration capability

### Goal

Teach MCP as a tool/context protocol, not the entire module.

### Concepts

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

### App-specific MCP server idea

Build an MCP server for the Module 2 app.

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

### Deliverables

```text
mcp-server/
  server.py
  README.md
.mcp.json
docs/mcp-tools.md
```

### Teaching point

MCP should expose useful capabilities with safe boundaries. It should not become “give the agent access to everything.”

---

## Lesson 3.4 — Reusable workflows: skills, commands, rules, and recipes

### Goal

Teach when repeated instructions should become a reusable capability.

### When to create one

Create a reusable workflow when you repeatedly paste the same:

```text
checklist
review procedure
debugging procedure
deployment procedure
project-specific convention
multi-step workflow
```

### Good course workflows

```text
/review-api-change
/debug-ci-failure
/add-backend-endpoint
/add-frontend-component
/prepare-pr
/check-generated-code
/deploy-staging
```

### Example workflow

Path:

```text
agent-capabilities/review-api-change/README.md
```

Content:

```markdown
---
name: review-api-change
description: Review backend or frontend changes that may affect the OpenAPI contract.
---

# API Change Review

When reviewing an API change:

1. Check whether `openapi.yaml` needs to change.
2. Check whether frontend API calls still match the backend.
3. Check whether backend tests cover the changed endpoint.
4. Check whether error responses are documented.
5. Check whether the database schema is affected.
6. Produce a concise report with:
   - contract changes
   - required tests
   - compatibility risks
   - suggested fixes
```

### Deliverables

```text
agent-capabilities/review-api-change/
agent-capabilities/debug-ci-failure/
docs/reusable-workflows.md
```

---

## Lesson 3.5 — Hooks for guardrails and automation

### Goal

Show that agent workflows can be controlled and automated.

### Hook use cases

```text
auto-format after edits
run ruff after Python edits
run prettier after frontend edits
block dangerous shell commands
block editing .github/workflows without confirmation
log every Bash command
notify when a long task finishes
run tests before commit
```

### Example hook idea

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/agent-hooks/check_bash_command.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/agent-hooks/format_changed_file.py"
          }
        ]
      }
    ]
  }
}
```

### Deliverables

```text
.claude/settings.json
scripts/agent-hooks/
docs/hooks.md
```

### Teaching point

Hooks turn “please be careful” into repeatable guardrails.

---

## Lesson 3.6 — Subagents for specialized tasks

### Goal

Teach specialized agents with their own context and permissions.

### Why subagents matter

They are useful when a side task would pollute the main context with logs, search results, or file contents.

### Course subagents

```text
api-contract-reviewer
debugger
browser-tester
security-reviewer
database-query-validator
release-note-writer
```

### Example subagent

Path:

```text
agent-capabilities/subagents/api-contract-reviewer.md
```

Content:

```markdown
---
name: api-contract-reviewer
description: Reviews changes that may affect the OpenAPI contract.
tools: Read, Grep, Glob
model: sonnet
---

You are an API contract reviewer.

Check:
- whether backend routes match openapi.yaml
- whether frontend clients match openapi.yaml
- whether tests cover success and error responses
- whether any breaking change is introduced

Do not edit files. Return a concise report with:
- changed endpoints
- compatibility risks
- missing tests
- required fixes
```

### Deliverables

```text
agent-capabilities/subagents/api-contract-reviewer.md
agent-capabilities/subagents/debugger.md
agent-capabilities/subagents/browser-tester.md
docs/subagents.md
```

### Teaching point

Subagents are a permission and context management tool, not just a “cool multi-agent feature.”

---

## Lesson 3.7 — Plugins for packaging reusable capabilities

### Goal

Teach when standalone `.claude/` config should become a shareable plugin.

### Standalone config vs plugin

```text
Use .claude/ for:
- one project
- personal workflows
- experiments
- short local skill names

Use plugins for:
- team sharing
- versioned releases
- cross-project reuse
- community distribution
- namespaced skills
```

### Example plugin layout

```text
plugins/ai-devtools-plugin/
  .claude-plugin/
    plugin.json
  skills/
    review-api-change/
      SKILL.md
    debug-ci-failure/
      SKILL.md
  agents/
    api-contract-reviewer.md
  hooks/
    guardrails.json
  README.md
```

### Example `plugin.json`

```json
{
  "name": "ai-devtools",
  "description": "Reusable AI Dev Tools Zoomcamp agent capabilities",
  "version": "0.1.0",
  "author": {
    "name": "DataTalks.Club"
  }
}
```

### Deliverables

```text
plugins/ai-devtools-plugin/
docs/plugin-usage.md
```

---

## Lesson 3.8 — Creating custom agents with SDKs

### Goal

Teach when to build a custom agent instead of using an interactive coding agent.

### When to use a custom agent

```text
CI/CD integration
custom internal app
scheduled automation
team-specific workflow
controlled tool access
structured output
repeatable pipeline
```

### Custom agent sketch

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

TASK = """
Review the current repository for changes that affect the API contract.
Return:
- files inspected
- endpoints affected
- tests needed
- risks
Do not edit files.
"""

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob", "Bash"],
    )

    async for message in query(prompt=TASK, options=options):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

### Deliverables

```text
custom-agent/
  agent.py
  README.md
docs/custom-agent-design.md
```

### Teaching point

Custom agents are for workflows that need programmatic control, structured outputs, and repeatability.

---

## 13. Module 3 final assignment: Agent Extension Pack

Students extend their Module 2 app with an agent extension pack.

### Required files

```text
AGENTS.md or equivalent project instructions

agent-capabilities/
  review-api-change/
  debug-ci-failure/
  subagents/
    api-contract-reviewer.md
    debugger.md

agent-hooks/

mcp-server/
  server.py
  README.md

plugins/
  ai-devtools-agent-pack/
    capabilities/
    subagents/
    README.md

custom-agent/
  agent.py
  README.md

docs/
  agent-extension-pack.md
  permissions.md
  demo.md
```

### Minimum requirements

```text
1 project instructions file
1 reusable workflow/skill/command
1 specialized subagent
1 MCP tool/server
1 hook or guardrail
1 small custom agent OR plugin/extension package
1 permission/security note
```

### Demo script

Students should record or write a demo showing:

```text
1. The agent reads the project instructions.
2. The agent invokes a reusable workflow.
3. A subagent reviews an API change.
4. The agent calls an MCP tool.
5. A hook prevents or logs a risky action.
6. The student reviews the final diff.
```

### Rubric

| Criterion | Excellent | Good | Needs work |
|---|---|---|---|
| Project context | Clear, complete, useful | Mostly useful | Generic or missing |
| Reusable workflow | Reusable and focused | Works but broad | Just a prompt dump |
| Subagent | Has clear role and permissions | Role defined | No permission thinking |
| MCP | Useful app-specific tool | Toy tool works | Not connected to app |
| Hook | Real guardrail or automation | Simple hook | Not demonstrated |
| Custom agent/plugin | Runs and documented | Partial | Missing |
| Permissions | Explicit and thoughtful | Basic | Not considered |

---

# Module 4 — Open-Source AI Tools for Security, Audit, and DevOps

## 14. Module 4 positioning

Module 4 should be focused and constrained:

```text
Only open-source AI tools.
Only security, audit, and DevOps.
No general coding agents.
No LLM application evals.
No AI test-generation focus.
```

This means the following tools are **not Module 4 tools**, even though they are useful elsewhere:

```text
Cline
goose
OpenCode
Aider
Codex CLI
Claude Code
Gemini CLI
OpenHands
SWE-agent
mini-SWE-agent
CoverUp
DeepEval
promptfoo
LangSmith
Braintrust
```

They belong in earlier modules or different courses.

---

## 15. Module 4 core tool stack

### Required stack

```text
PR-Agent
Semgrep MCP Server
Snyk Agent Scan
K8sGPT
LiteLLM
Ollama
```

### Optional / instructor-demo stack

```text
HolmesGPT
Stakpak
garak
MCPSafetyScanner
Agent Audit / future agent security scanners
```

---

## 16. Module 4 tool table

| Tool | Category | Why it belongs in Module 4 | Required? |
|---|---|---|---|
| PR-Agent | AI PR audit | Reviews PRs, summarizes changes, suggests improvements, updates changelog | Yes |
| Semgrep MCP | AI-accessible security scanning | Lets an AI assistant call deterministic Semgrep scans instead of guessing | Yes |
| Snyk Agent Scan | Agent/MCP/skill security audit | Scans MCP servers, tools, prompts, resources, and skills for agent-specific risks | Yes |
| K8sGPT | AI Kubernetes diagnostics | Explains Kubernetes cluster issues and can expose MCP integration | Yes |
| LiteLLM | AI gateway/governance | Centralizes model access, virtual keys, spend tracking, routing, guardrails | Yes |
| Ollama | Local model runner | Enables local/private model labs for security and ops data | Yes |
| HolmesGPT | AI SRE investigation | Investigates production incidents using logs, metrics, traces, alerts, runbooks | Optional / demo |
| Stakpak | DevOps AI agent | Autonomous DevOps agent; interesting but more advanced | Optional / mention |

---

## 17. Tool notes

### 17.1 PR-Agent

Use for:

```text
AI PR descriptions
AI PR review
suggested improvements
questions about diff
changelog updates
risk hints
```

Why it is useful:

```text
it sits at the PR boundary
it is easy to demo
it produces concrete review artifacts
it can run as GitHub Action or CLI
it can be customized
```

Suggested course commands:

```text
/describe
/review
/improve
/ask
/update_changelog
```

Suggested files:

```text
.github/workflows/pr-agent.yml
.pr_agent.toml
docs/pr-audit-checklist.md
```

---

### 17.2 Semgrep MCP Server

Use for:

```text
security scans through MCP
custom Semgrep rules
AI-assisted explanation of findings
deterministic security evidence
```

Important teaching point:

> The AI should not hallucinate security findings. It should call a real scanner and explain the results.

Useful tools exposed by Semgrep MCP include:

```text
security_check
semgrep_scan
semgrep_scan_with_custom_rule
get_abstract_syntax_tree
```

Suggested files:

```text
.vscode/mcp.json
.cursor/mcp.json
security/custom-rule.yml
security/semgrep-findings.md
```

---

### 17.3 Snyk Agent Scan

Important naming note:

> The older `mcp-scan` repository URL now redirects to **Snyk Agent Scan**. In the course, use the current name: **Snyk Agent Scan**. It still covers the same category we wanted from mcp-scan: scanning agent components, MCP servers, tools, prompts, resources, and skills.

Use for:

```text
agent component inventory
MCP server security review
skills security review
prompt injection detection
tool poisoning detection
toxic flow detection
hardcoded secret / credential handling checks in skills
```

Important safety note:

```text
Scanning MCP configs can execute the commands defined in those configs.
Run untrusted scans in a sandbox.
Review commands before approving them.
Use non-interactive flags only in trusted CI environments.
```

Suggested files:

```text
security/agent-scan-report.json
security/agent-scan-notes.md
security/mcp-threat-model.md
security/tool-permissions.md
```

---

### 17.4 K8sGPT

Use for:

```text
Kubernetes issue diagnosis
pod/deployment/service/ingress analysis
plain-English explanations
JSON reports
anonymized analysis
MCP integration with compatible clients
```

Good beginner lab failures:

```text
wrong image tag
missing environment variable
bad service selector
failing readiness probe
insufficient resources
crash loop
bad ingress target
```

Suggested commands:

```bash
k8sgpt auth add
k8sgpt analyze --explain
k8sgpt analyze --explain --with-doc
k8sgpt analyze --explain --filter=Pod --namespace=default
k8sgpt analyze --explain --output=json --anonymize
k8sgpt serve --mcp --mcp-http
```

Suggested files:

```text
ops/k8s-broken-deployment.yaml
ops/k8sgpt-report.json
ops/k8sgpt-diagnosis.md
```

---

### 17.5 HolmesGPT

Use for:

```text
incident investigation
alert triage
root-cause hypothesis
log/metric/trace correlation
runbook-aware investigation
SRE assistant demos
```

Why it is optional:

```text
it is powerful
it may require more setup
it benefits from observability data
it may be better as an instructor demo first
```

Suggested course use:

```text
prepared alert/log bundle
small Kubernetes incident
Prometheus/Loki demo if available
incident summary exercise
```

Suggested files:

```text
ops/alert-example.json
ops/holmes-investigation.md
ops/incident-summary.md
ops/follow-up-actions.md
```

---

### 17.6 LiteLLM

Use for:

```text
central model gateway
virtual keys
routing between providers
spend tracking
guardrails
logging
OpenAI-compatible API for tools
MCP gateway patterns
```

Why it belongs:

Module 4 should not only teach the AI security/audit tools; it should also teach how to control model access for those tools.

Suggested architecture:

```text
PR-Agent        -> LiteLLM -> hosted model
K8sGPT          -> LiteLLM or Ollama
HolmesGPT       -> LiteLLM
Semgrep MCP     -> scanner first, model only for explanation
Snyk Agent Scan -> scanner first, no broad model access needed
```

Suggested files:

```text
ops/litellm-config.yaml
docs/model-routing.md
docs/ai-tool-policy.md
```

---

### 17.7 Ollama

Use for:

```text
local model runs
privacy-sensitive demos
offline-ish labs
model fallback
local experiments with K8sGPT or other tools
```

Suggested commands:

```bash
ollama run qwen
ollama run deepseek-coder
ollama run gemma
```

Exact model names should be checked at recording time.

---

## 18. Module 4 content flow

## Lesson 4.1 — Production AI risk model

### Goal

Give learners a mental model before tools.

### Topics

```text
AI-generated code risk
agent tool risk
MCP server risk
skill/plugin supply-chain risk
CI/CD risk
Kubernetes/operations risk
model gateway/data exposure risk
```

### Main message

```text
AI can help audit and operate software, but it must be grounded in evidence:
- diffs
- scanner results
- cluster state
- logs
- metrics
- traces
- policies
```

### Deliverable

```text
security/ai-production-risk-model.md
```

Template:

```markdown
# AI production risk model

## What can AI tools read?

## What can AI tools change?

## What secrets or sensitive data could be exposed?

## Which tools are read-only?

## Which tools can write?

## Which actions require human approval?

## What logs or audit trails exist?
```

---

## Lesson 4.2 — AI PR audit with PR-Agent

### Goal

Teach AI-assisted review at the pull request boundary.

### Setup

```yaml
# .github/workflows/pr-agent.yml
name: PR Agent

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  pr_agent_job:
    runs-on: ubuntu-latest
    steps:
      - name: PR Agent action step
        uses: the-pr-agent/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

For the course, the model provider can go through LiteLLM instead of directly to a hosted provider.

### Security-focused PR-Agent configuration

```toml
[pr_reviewer]
extra_instructions = """
Focus on security, auditability, and operational risk.

Check for:
- missing auth or authorization checks
- unsafe user input handling
- secrets or tokens in code
- suspicious dependency changes
- Dockerfile or deployment risks
- broad GitHub Actions permissions
- unsafe use of pull_request_target
- changes to CI/CD without clear rationale
- missing tests for security-sensitive behavior
- unrelated changes
"""
```

### Lab

Students create a PR that changes the Module 2 app.

Run PR-Agent to:

```text
describe the PR
review the PR
suggest improvements
ask a question about a risky file
update changelog
```

### Deliverables

```text
.github/workflows/pr-agent.yml
.pr_agent.toml
docs/pr-agent-output.md
docs/pr-audit-checklist.md
```

### Teaching point

> AI PR review is not approval. It is an audit assistant.

---

## Lesson 4.3 — AI-accessible security scanning with Semgrep MCP

### Goal

Show how an AI assistant can use a deterministic security scanner.

### Setup example

```json
{
  "mcpServers": {
    "semgrep": {
      "command": "uvx",
      "args": ["semgrep-mcp"],
      "env": {
        "SEMGREP_APP_TOKEN": "<optional-token>"
      }
    }
  }
}
```

### Lab

1. Add an intentionally vulnerable pattern to the app.
2. Ask an MCP-compatible assistant to run Semgrep MCP.
3. Review the finding.
4. Ask the assistant to explain the finding.
5. Fix the issue.
6. Re-run the scan.
7. Record the remediation.

### Good toy vulnerabilities

```text
hardcoded fake API key
unsafe string interpolation into SQL-like query
missing authorization check
unsafe redirect
unsafe shell command construction
```

### Example custom rule skeleton

```yaml
rules:
  - id: python-dangerous-subprocess-shell-true
    message: Avoid shell=True with user-controlled input.
    severity: WARNING
    languages: [python]
    pattern: subprocess.run(..., shell=True, ...)
```

### Deliverables

```text
security/semgrep-findings.md
security/custom-rule.yml
security/remediation-notes.md
```

### Teaching point

> The LLM explains and orchestrates; Semgrep provides the evidence.

---

## Lesson 4.4 — Agent, MCP, and skill security scanning with Snyk Agent Scan

### Goal

Audit the agent extension pack from Module 3.

### Setup

```bash
uvx snyk-agent-scan@latest
```

Scan a specific MCP configuration:

```bash
uvx snyk-agent-scan@latest ~/.vscode/mcp.json
```

Scan project reusable workflows or tool-specific skill directories:

```bash
uvx snyk-agent-scan@latest agent-capabilities
```

### Lab

1. Use the Module 3 project instructions, reusable workflows, subagents, hooks, and MCP server.
2. Run Agent Scan.
3. Review detected risks.
4. Fix one issue in a skill or tool description.
5. Re-scan.
6. Write a permission table.

### Example permission table

| Tool / skill | Reads | Writes | Network | Secrets | Human approval required |
|---|---|---|---|---|---|
| Semgrep MCP | source code | no | optional | token optional | no |
| app MCP server: get_leaderboard | app DB | no | local app | no | no |
| app MCP server: create_bug_report | issue tracker | yes | yes | token | yes |
| deploy skill | repo + cloud config | yes | yes | cloud token | yes |

### Deliverables

```text
security/agent-scan-report.json
security/agent-scan-notes.md
security/tool-permissions.md
security/mcp-threat-model.md
```

### Teaching point

> Agent extensions are a supply chain. Skills, MCP servers, plugins, and tool descriptions deserve review.

---

## Lesson 4.5 — Kubernetes diagnostics with K8sGPT

### Goal

Introduce AI-assisted DevOps diagnosis without turning the course into a Kubernetes course.

### Suggested environment

```text
kind
k3d
minikube
```

### Lab scenario

Deploy a toy version of the Module 2 app to a local cluster, then intentionally break it.

Broken examples:

```yaml
# wrong image
image: snake-backend:does-not-exist

# bad selector
selector:
  app: backend-wrong

# missing env var
env:
  - name: DATABASE_URL
    value: ""
```

### Commands

```bash
k8sgpt auth add
k8sgpt analyze --explain
k8sgpt analyze --explain --filter=Pod --namespace=default
k8sgpt analyze --explain --output=json --anonymize
```

### Deliverables

```text
ops/k8s-broken-deployment.yaml
ops/k8sgpt-report.json
ops/k8sgpt-diagnosis.md
```

### Diagnosis template

```markdown
# K8sGPT diagnosis

## Incident

## Symptoms

## K8sGPT findings

## Evidence from kubectl

## Root cause

## Fix

## Prevention

## What AI got right

## What needed human verification
```

### Teaching point

> K8sGPT should be grounded in cluster state. Learners must verify with `kubectl`.

---

## Lesson 4.6 — Incident investigation with HolmesGPT

### Goal

Show AI as an SRE investigation assistant.

### Status

This can be optional or instructor-led for the first cohort.

### Lab option A: prepared data bundle

Give students:

```text
alert.json
pod-describe.txt
app.log
prometheus-snapshot.txt
runbook.md
```

Use HolmesGPT or an instructor demo to investigate.

### Lab option B: live mini-stack

Use:

```text
local Kubernetes
Prometheus
Loki
sample app
one triggered alert
```

This is more realistic but heavier.

### Deliverables

```text
ops/holmes-investigation.md
ops/incident-summary.md
ops/follow-up-actions.md
```

### Incident summary template

```markdown
# Incident summary

## What happened

## Impact

## Timeline

## Signals reviewed

- Alerts
- Logs
- Metrics
- Kubernetes events
- Recent deployments

## Root-cause hypothesis

## Confirmed root cause

## Fix

## Follow-up actions

## What HolmesGPT helped with

## What humans verified
```

### Teaching point

> AI can correlate and summarize operational evidence, but humans confirm root cause and own remediation.

---

## Lesson 4.7 — AI tool governance with LiteLLM and Ollama

### Goal

Teach how to control how AI tools access models and sensitive data.

### Topics

```text
open-source tool vs hosted model
local model vs hosted model
virtual keys
tool-specific keys
budget limits
model routing
audit logs
prompt/data retention
redaction
local model fallback
```

### Example LiteLLM config

```yaml
model_list:
  - model_name: fast-default
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: os.environ/OPENAI_API_KEY

  - model_name: local-qwen
    litellm_params:
      model: ollama/qwen
      api_base: http://localhost:11434

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

### Suggested policy

```markdown
# AI tool policy

## Allowed tools

- PR-Agent for PR audit
- Semgrep MCP for security scanning
- Snyk Agent Scan for agent/MCP/skill scanning
- K8sGPT for local/dev cluster diagnosis
- HolmesGPT for instructor demo or approved environments

## Model routing

- PR summaries may use hosted models.
- Security scans must not send secrets.
- Logs must be anonymized before hosted model use.
- Local model is preferred for sensitive operational data.

## Approval rules

- AI tools may comment on PRs.
- AI tools may not merge PRs.
- AI tools may not deploy to production.
- AI tools may not rotate secrets.
- Any tool with write access requires human approval.
```

### Deliverables

```text
ops/litellm-config.yaml
docs/ai-tool-policy.md
docs/model-routing.md
docs/data-handling.md
```

### Teaching point

> “Open-source AI tool” does not automatically mean “private.” The model, gateway, logs, and data flow matter.

---

## 19. Module 4 final assignment: AI Security/Audit/DevOps Report

Students apply Module 4 to their Module 2/3 project.

### Required deliverables

```text
security/
  ai-production-risk-model.md
  semgrep-findings.md
  agent-scan-report.json
  agent-scan-notes.md
  tool-permissions.md
  mcp-threat-model.md

ops/
  k8sgpt-report.json
  k8sgpt-diagnosis.md
  litellm-config.yaml

docs/
  pr-agent-output.md
  pr-audit-checklist.md
  ai-tool-policy.md
  data-handling.md
```

### Optional deliverables

```text
ops/
  holmes-investigation.md
  incident-summary.md
  follow-up-actions.md
```

### Capstone narrative

The final report should answer:

```text
What did we audit?
Which AI tools were used?
Which findings were real?
Which findings were false positives or not relevant?
What was fixed?
What remains risky?
Which tools have read/write access?
Which model provider sees which data?
Which actions require human approval?
```

### Module 4 rubric

| Criterion | Excellent | Good | Needs work |
|---|---|---|---|
| PR audit | PR-Agent configured, output reviewed, security-focused notes | Basic PR-Agent run | No review artifacts |
| Semgrep MCP | Scan run, finding explained, custom rule or remediation included | Scan run | No deterministic evidence |
| Agent Scan | MCP/skills scanned, risks interpreted, permissions fixed | Scan run | No agent security thinking |
| K8sGPT | Broken deployment diagnosed and verified with kubectl | Diagnosis run | No verification |
| Governance | Clear policy, model routing, data handling, approval rules | Basic policy | Missing |
| Final report | Explains evidence and decisions | Lists outputs | Hard to follow |

---

# 20. What belongs where

## Module 1

```text
ChatGPT
Claude
Gemini
Cursor
Windsurf
VS Code Copilot
Claude Code
Codex CLI
Gemini CLI
Aider
Cline
goose
OpenCode
Lovable
Bolt
Replit
Zed
Antigravity
ZCode
Cowork-style tools
```

Purpose: compare categories and choose the right tool.

## Module 2

```text
Lovable / Bolt / Replit for prototype
Claude Code / Codex / Cursor for implementation
OpenAPI
FastAPI / Django
Docker
GitHub Actions
Render / Fly / Railway
```

Purpose: build and ship an app.

## Module 3

```text
Claude Code
CLAUDE.md
AGENTS.md
MCP
skills
hooks
subagents
plugins
Agent SDK
custom MCP server
custom agent
```

Purpose: extend and customize coding agents.

## Module 4

```text
PR-Agent
Semgrep MCP
Snyk Agent Scan
K8sGPT
LiteLLM
Ollama
HolmesGPT optional
Stakpak optional
```

Purpose: security, audit, DevOps, governance.

---

# 21. Suggested README syllabus block

```markdown
## Syllabus

### Module 1: AI-Native Developer Workflow

Compare modern AI developer tools: chat assistants, terminal coding agents, agentic IDEs, desktop workbenches, cloud agents, and project bootstrappers. Learn when to use ChatGPT/Claude/Gemini-style chat, Claude Code/Codex/Gemini CLI-style terminal agents, Cursor/Windsurf/Zed/Antigravity-style IDEs, and Lovable/Bolt/Replit-style bootstrappers.

You will also learn context engineering with `AGENTS.md`, `CLAUDE.md`, repository instructions, product specs, architecture notes, testing guidelines, and security checklists.

Outcome: configure a repository for AI-assisted development and complete one small feature using a disciplined AI workflow.

### Module 2: Build and Ship an AI-Assisted Full-Stack App

Build an end-to-end application with AI assistance: product spec, frontend prototype, OpenAPI contract, FastAPI or Django backend, database, tests, Docker, deployment, and CI/CD.

Outcome: a deployed full-stack app with tests, Docker setup, OpenAPI contract, and a reproducible development workflow.

### Module 3: Coding Agent Capabilities: MCP, Skills, Plugins, and Custom Agents

Learn how modern coding agents are extended and customized. MCP is covered as one important capability, alongside project instructions, reusable workflows/skills, hooks, specialized subagents, plugins/extensions, and custom agents. Examples can use specific tools, but the concepts should transfer across modern agentic coding tools.

Outcome: create an agent extension pack for your app, including project instructions, a custom skill, a specialized subagent, a hook, an MCP tool/server, and either a small plugin or custom agent.

### Module 4: Open-Source AI Tools for Security, Audit, and DevOps

Learn how to use open-source AI tools around the production workflow. This module focuses on AI pull request audit, AI-accessible security scanning, agent/MCP/skill security scanning, Kubernetes diagnostics, incident investigation, and AI tool governance.

Outcome: harden and audit your final project using PR-Agent, Semgrep MCP, Snyk Agent Scan, K8sGPT, LiteLLM, Ollama, and optionally HolmesGPT.
```

---

# 22. Suggested repository structure

```text
ai-dev-tools-zoomcamp/
  README.md

  01-ai-native-workflow/
    README.md
    labs/
    examples/
    homework.md

  02-build-and-ship/
    README.md
    snake-app/
    examples/
    homework.md

  03-coding-agent-capabilities/
    README.md
    agent-capabilities/
      reusable-workflows/
      subagents/
      hooks/
      plugins/
    mcp-server/
    custom-agent/
    homework.md

  04-ai-security-audit-devops/
    README.md
    pr-agent/
    semgrep-mcp/
    agent-scan/
    k8sgpt/
    holmesgpt/
    litellm-ollama/
    homework.md

  project/
    README.md
    rubric.md
```

---

# 23. Suggested recording order

## First pass

1. Module 1 overview and tool comparison
2. Module 2 app build
3. Module 3 agent capabilities overview
4. Module 3 skills + subagents
5. Module 3 MCP + custom agent
6. Module 4 PR-Agent
7. Module 4 Semgrep MCP + Agent Scan
8. Module 4 K8sGPT
9. Module 4 LiteLLM/Ollama governance
10. Module 4 optional HolmesGPT demo

## Why this order

This order gets learners to a working app before they need to understand deeper agent customization and production tools.

---

# 24. Instructor ownership suggestion

## Alex / main course flow

```text
Module 1 framing
Module 2 full-stack app
overall project and cohort structure
```

## Co-instructor with coding agent expertise

```text
Module 3 coding agent capabilities
reusable workflows / skills / commands
hooks and guardrails
specialized subagents
plugins and extensions
MCP
custom agents
```

## Security/DevOps contributor or research time

```text
Module 4 tool selection
PR-Agent
Semgrep MCP
Snyk Agent Scan
K8sGPT
LiteLLM/Ollama
HolmesGPT demo
```

---

# 25. Reply draft to co-instructor

```text
Hey, this sounds great and aligns well with the 2026 direction.

I’m thinking we move Module 3 away from being only an MCP deep dive and make it about coding agent capabilities more broadly: how agents get context, how they use tools, how we extend them with MCP, skills, hooks, plugins, subagents, and how to build small custom agents.

Since you use Claude extensively, Claude Code can be one concrete demo environment. But we should explain the concepts in a way that transfers to other coding agents too, including Codex, OpenCode, Cursor, GitHub Copilot, Aider, and similar tools.

A possible outcome for the module is an “agent extension pack” for the app built in Module 2:
- project instructions such as AGENTS.md, CLAUDE.md, or equivalent
- one reusable workflow / skill / command
- one specialized subagent
- one hook
- one MCP tool/server
- one small plugin/extension package or custom agent
- a permissions/security note

That would make Module 3 much more useful than just MCP, and it gives students something concrete to add to their project repo.
```

---

# 26. Source notes checked for this proposal

These are not required reading for students, but they informed the proposal and should be useful for instructors.

## Claude / Module 3

- [Claude Code overview](https://code.claude.com/docs/en/overview) — Claude Code reads codebases, edits files, runs commands, integrates with tools, and is available in terminal, IDE, desktop app, and browser.
- [Claude Code MCP docs](https://code.claude.com/docs/en/mcp) — MCP connects Claude Code to external tools, data sources, databases, and APIs.
- [Claude Code skills docs](https://code.claude.com/docs/en/skills) — skills use `SKILL.md`, can be invoked with slash commands, and are useful for repeatable workflows.
- [Claude Code hooks docs](https://code.claude.com/docs/en/hooks) — hooks are shell commands, HTTP endpoints, or LLM prompts executed at lifecycle points.
- [Claude Code subagents docs](https://code.claude.com/docs/en/sub-agents) — subagents are specialized assistants with their own context, tools, and permissions.
- [Claude Code plugins docs](https://code.claude.com/docs/en/plugins) — plugins package skills, agents, hooks, and MCP servers for sharing.
- [Claude Agent SDK docs](https://code.claude.com/docs/en/agent-sdk) — Agent SDK supports custom agents in Python/TypeScript with Claude Code tools and agent loop.
- [Model Context Protocol architecture](https://modelcontextprotocol.io/docs/learn/architecture) — MCP client-server architecture, tools, resources, prompts, and transports.

## Module 4 tools

- [PR-Agent GitHub repository](https://github.com/The-PR-Agent/pr-agent) — open-source AI-powered PR review agent with `/describe`, `/review`, `/improve`, `/ask`, and changelog support.
- [Semgrep MCP Server](https://github.com/semgrep/mcp) — MCP server for using Semgrep to scan code for security vulnerabilities.
- [Snyk Agent Scan](https://github.com/snyk/agent-scan) — security scanner for AI agents, MCP servers, and agent skills. The older `invariantlabs-ai/mcp-scan` URL redirects here.
- [K8sGPT](https://github.com/k8sgpt-ai/k8sgpt) — Kubernetes diagnostics with AI explanations and MCP serve mode.
- [HolmesGPT](https://github.com/HolmesGPT/holmesgpt) — open-source SRE agent for investigating production incidents and root causes; CNCF sandbox project.
- [LiteLLM](https://github.com/BerriAI/litellm) — open-source AI gateway for many LLM providers with virtual keys, cost tracking, guardrails, routing, and logging.
- [Ollama](https://github.com/ollama/ollama) — local model runner with REST API.
- [Stakpak](https://github.com/stakpak/agent) — optional DevOps agent to mention or demo, not required.

## Tool landscape / Module 1 watchlist

- [Google Antigravity coverage](https://www.theverge.com/news/822833/google-antigravity-ide-coding-agent-gemini-3-pro) — agent-first coding tool with editor, terminal, browser, and artifact-style verification.
- [Z.ai ZCode coverage](https://www.businessinsider.com/z-ai-zcode-ai-coding-tool-chinese-startup-lower-cost-2026-7) — emerging Z.ai coding tool; treat as a watchlist item.
- [Claude Cowork coverage](https://www.techradar.com/pro/put-claude-to-work-claude-can-now-use-your-computer-autonomously-you-just-have-to-tell-it-what-to-do) — graphical/autonomous Claude work assistant; mention cautiously as a related workbench-style product, not a core coding tool.

---

# 27. Final recommendation

Proceed with the four-module structure.

The most important changes are:

```text
1. Rename Module 1 from vibe coding to AI-native developer workflow.
2. Keep Module 2 as the main end-to-end app build.
3. Convert Module 3 from MCP-only to coding agent capabilities:
   MCP + skills + hooks + subagents + plugins + custom agents.
4. Make Module 4 a focused open-source AI security/audit/DevOps module:
   PR-Agent + Semgrep MCP + Snyk Agent Scan + K8sGPT + LiteLLM + Ollama,
   with HolmesGPT as optional/instructor demo.
```

This gives the course a strong 2026 identity:

> **Build with AI, extend the agent, then audit and operate the result safely.**

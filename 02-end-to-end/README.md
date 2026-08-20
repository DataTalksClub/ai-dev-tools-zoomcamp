# Module 2 — Build and Ship an AI-Assisted Full-Stack App

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what we are preparing, but the final videos, exercises, homework, and requirements may change before the cohort starts.

## Overview

In this module, you build a working end-to-end application with AI assistance. The default project remains a small Snake Arena app because it is visual, interactive, and still requires the main parts of a real system:

- product spec
- frontend
- OpenAPI contract
- backend
- database
- tests

The goal is not to let an AI tool build everything unchecked. The goal is to practice a controlled workflow where AI helps you move faster and you verify each step.

The module ends with an app that runs on your machine: a frontend and a backend that talk to each other over a defined contract, with data persisted in SQLite. Everything needed to put it in front of other people — integration tests, containers, CI, deployment, and CI/CD — is [Module 3](../03-deployment/).

Reference app from the previous version:

- https://github.com/alexeygrigorev/snake-arena-online

[Recording: Build and Ship an AI-Assisted Full-Stack App](https://www.youtube.com/watch?v=x9dq5nBpDg8)

Module summary: The companion article builds a collaborative system-design interview app from
scratch. It moves from a frontend prototype with mocked calls to an OpenAPI
contract, a FastAPI backend, WebSocket collaboration, and SQLite persistence,
while testing each stage before moving on.

[Read the article: Build and Ship a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with)

## Lessons

### Lesson 2.1 — Product Spec and Acceptance Criteria

Before generating code, write a small product spec:

```text
product-spec.md
user stories
acceptance criteria
non-goals
technical constraints
```

Example app scope:

- play Snake
- register/login
- leaderboard
- watch simulated games
- submit score

Non-goals:

- real-time multiplayer
- payments
- social login

### Lesson 2.2 — Frontend Prototype

Use an AI tool to create a first frontend draft.

Possible tools:

- Lovable
- Bolt
- Replit Agent
- Cursor
- Claude Code
- Codex
- GitHub Copilot
- OpenCode

Teaching point: the prototype is not the final product. Pull it into a normal repo workflow, inspect the generated code, and make the app maintainable.

### Lesson 2.3 — OpenAPI Contract

Create or extract:

```text
openapi.yaml
```

Topics:

- API-first development
- contract between frontend and backend
- schema validation
- generated clients/servers
- how AI can hallucinate endpoints

### Lesson 2.4 — Backend Implementation

Default stack:

- FastAPI
- `uv`
- mock database first
- tests for key endpoints

Other valid options:

- Django
- Node/Express

Use the OpenAPI contract as the source of truth for backend behavior.

### Lesson 2.5 — Database Support

Replace the in-memory store with a real database so data survives a restart.

Topics:

- SQLite for local development
- SQLAlchemy or Django ORM
- configuring the connection through an environment variable
- staying database-agnostic so Postgres can be added later without a rewrite

Teaching point: tell the agent up front that another database will replace this one. Otherwise the first version quietly depends on SQLite-specific behavior.

### Lesson 2.6 — Tests

Cover the behavior described in the spec and the contract:

- unit tests for the key backend endpoints
- frontend tests
- what the tests would catch if an agent rewrote the code tomorrow

Integration tests against a production-like database come in [Module 3](../03-deployment/).

## Module Deliverables

At the end of Module 2, your repo should include:

```text
product-spec.md
AGENTS.md or equivalent
frontend/
backend/
openapi.yaml
tests/
docs/ai-usage-report.md
```

The app should run locally from the README, persist data in SQLite, and pass its own tests.

## Previous Cohort Materials

The previous version of this module is archived here:

- [2025 archived Module 2](../cohorts/2025/02-end-to-end/)
- [2026 homework](../cohorts/2026/02-end-to-end/homework.md)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

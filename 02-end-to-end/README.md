# Module 2 — Build and Ship an AI-Assisted Full-Stack App

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what we are preparing, but the final videos, exercises, homework, and requirements may change before the cohort starts.

## Overview

In this module, you build an end-to-end application with AI assistance. The default project remains a small Snake Arena app because it is visual, interactive, and still requires the main parts of a real system:

- product spec
- frontend
- OpenAPI contract
- backend
- database
- tests
- Docker
- deployment
- CI/CD

The goal is not to let an AI tool build everything unchecked. The goal is to practice a controlled workflow where AI helps you move faster and you verify each step.

Reference app from the previous version:

- https://github.com/alexeygrigorev/snake-arena-online

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

Topics:

- SQLite for local tests
- Postgres for Docker/production
- SQLAlchemy or Django ORM
- migrations
- integration tests

### Lesson 2.6 — Containerization

Deliverables:

```text
Dockerfile
docker-compose.yml
.env.example
```

### Lesson 2.7 — Deployment

Suggested platforms:

- Render
- Fly.io
- Railway
- Cloud Run

Keep the default deployment path simple and reproducible.

### Lesson 2.8 — CI/CD

Required checks:

- backend tests
- frontend tests
- integration tests if feasible
- build check
- deployment trigger

## Module Deliverables

At the end of Module 2, your repo should include:

```text
product-spec.md
AGENTS.md or equivalent
frontend/
backend/
openapi.yaml
docker-compose.yml
tests/
.github/workflows/
docs/ai-usage-report.md
```

The app should be deployed, tested, and reproducible from the README.

## Previous Cohort Materials

The previous version of this module is archived here:

- [2025 archived Module 2](../cohorts/2025/02-end-to-end/)
- [2026 homework](../cohorts/2026/02-end-to-end/homework.md)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

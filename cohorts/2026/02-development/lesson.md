---
video_url: https://www.youtube.com/watch?v=x9dq5nBpDg8
---
# Build and Ship an AI-Assisted Full-Stack App

## Overview

In this module, you build a working end-to-end application with AI assistance. The default project remains a small Snake Arena app because it is visual, interactive, and still requires the main parts of a real system:

- product spec
- frontend
- OpenAPI contract
- backend
- database
- tests

The goal is not to let an AI tool build everything unchecked. The goal is to practice a controlled workflow where AI helps you move faster and you verify each step.

The module ends with an app that runs on your machine: a frontend and a backend that talk to each other over a defined contract, with data persisted in SQLite. Everything needed to put it in front of other people — integration tests, containers, CI, deployment, and CI/CD — is [Module 3](../03-deployment/lesson.md).

You will:

- Write a small product spec with user stories, acceptance criteria, and non-goals before generating any code
- Draft a frontend prototype with an AI tool (Lovable, Bolt, Cursor, Claude Code, Codex, ...), then pull it into a normal repo workflow and make it maintainable
- Define an OpenAPI contract as the source of truth between frontend and backend
- Implement a FastAPI backend against the contract, starting with a mock database and tests for the key endpoints
- Swap the mock store for SQLite, keeping the app database-agnostic so Postgres can replace it later without a rewrite
- Add unit and frontend tests that cover the behavior described in the spec and the contract

Reference app:

- https://github.com/alexeygrigorev/interview-canvas-share

Module summary: The companion article builds a collaborative system-design interview app from
scratch. It moves from a frontend prototype with mocked calls to an OpenAPI
contract, a FastAPI backend, WebSocket collaboration, and SQLite persistence,
while testing each stage before moving on.

[Read the article: Build and Ship a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with)

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

## Homework

- [Homework](homework.md)

## Previous Cohort Materials

The previous version of this module is archived here:

- [2025 archived Module 2](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/tree/main/cohorts/2025/02-end-to-end)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

# Module 3 — Test, Containerize, and Deploy an AI-Assisted App

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what we are preparing, but the final videos, exercises, homework, and requirements may change before the cohort starts.

## Overview

Module 2 ends with an application that runs on your machine. This module takes it the rest of the way: proven by tests that exercise the real stack, packaged in containers, checked automatically on every pull request, and deployed so other people can use it.

The path:

```text
integration tests
containerization
continuous integration
deployment
continuous delivery
```

Each step is something AI tools are good at drafting and bad at owning. A generated `Dockerfile` that builds is not the same as one that builds the right thing, and a green pipeline that skips the tests is worse than no pipeline. The workflow stays the same as in earlier modules: let the agent produce the first version, then read it, run it, and break it on purpose to see whether it actually catches anything.

Continue with the app you built in Module 2.

[Recording: Test, Containerize, and Deploy an AI-Assisted App](https://www.youtube.com/watch?v=gxt5ZDVnBMM)

Module summary: The companion article takes the local application to a public deployment. It
adds integration and end-to-end tests, packages the frontend and backend in a
container, switches from SQLite to Postgres with Docker Compose, deploys to
AWS, and automates delivery with GitHub Actions.

[Read the article: Deploy a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/deploy-a-full-stack-app-with-ai-coding)

## Lessons

### Lesson 3.1 — Integration Tests

Goal: test the app the way it is deployed, not the way it is unit-tested.

Module 2 covered unit tests for individual endpoints against local SQLite. Integration tests cover the seams:

```text
API request through to a real database
migrations applied to an empty database
auth flow end to end
frontend calling the backend
error and failure paths
```

Topics:

- test database setup and teardown
- fixtures and seed data
- transactional vs. recreated test databases
- testing against the OpenAPI contract
- what belongs in a unit test and what needs integration
- keeping the suite fast enough to run on every push

Teaching point: ask the agent for the tests, then break the code on purpose. A test suite that stays green when you delete a validation rule is not testing anything.

Deliverables:

```text
tests/integration/
docs/testing.md
```

### Lesson 3.2 — Containerization

Goal: package the app so it runs the same way everywhere.

Deliverables:

```text
Dockerfile
docker-compose.yml
.dockerignore
.env.example
```

Topics:

- multi-stage builds: build the frontend with Node, serve the static files from the backend image
- base image choice and image size
- build-time vs. runtime configuration
- secrets and environment variables that must not be baked into the image
- swapping SQLite for Postgres as a Compose service
- database migrations
- running the integration tests against the containerized stack

Module 2 kept the app database-agnostic behind an ORM and an environment variable. This is where that pays off: the same code runs on SQLite locally and Postgres in a container.

Teaching point: AI tools produce plausible `Dockerfile`s quickly. Check what the generated image actually contains, which user it runs as, and whether the frontend build really produced the files the backend expects to serve.

### Lesson 3.3 — Setting Up CI

Goal: make the checks run automatically on every change, before deployment enters the picture.

Required checks:

```text
linting and formatting
backend unit tests
frontend tests
integration tests
container build
```

Topics:

- workflow triggers on push and pull request
- service containers for the test database
- caching dependencies
- required status checks and branch protection
- reading a failing pipeline log and feeding it back to the agent

Deliverables:

```text
.github/workflows/ci.yml
```

Teaching point: CI is where the review checklist becomes automatic. Anything you keep asking an agent to remember belongs here instead.

### Lesson 3.4 — Deployment

Goal: get the app running somewhere other people can reach.

Suggested platforms:

- Render
- Fly.io
- Railway
- Cloud Run

Topics:

- managed database provisioning
- environment variables and secret storage
- running migrations on deploy
- health checks
- logs and rollback
- the difference between a deploy that succeeded and an app that works

Deliverables:

```text
deployment configuration for your platform
docs/deployment.md
a public URL
```

Keep the default deployment path simple and reproducible. Someone should be able to follow your README and get the same result.

### Lesson 3.5 — CI/CD

Goal: connect the pipeline to the deployment so merging is what ships.

Topics:

- deploy on merge to the main branch
- gating deployment behind the test job
- staging vs. production environments
- migrations in an automated deploy
- smoke test after deploy
- how to roll back

Deliverables:

```text
.github/workflows/deploy.yml
docs/release-process.md
```

Teaching point: CI/CD ships a bad release as efficiently as a good one. The pipeline is only as trustworthy as the checks in front of it, which is why the tests came first.

## Module Deliverables

At the end of Module 3, your repo should include:

```text
tests/integration/
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
.github/workflows/deploy.yml
docs/testing.md
docs/deployment.md
docs/release-process.md
```

The app should be deployed at a public URL, rebuilt and redeployed automatically when you merge to the main branch, and reproducible locally from the README.

## Previous Cohort Materials

Related material from the previous cohort:

- [2025 archived CI/CD and DevOps module](../cohorts/2025/05-cicd-devops/)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

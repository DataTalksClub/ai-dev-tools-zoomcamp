---
video_url: https://www.youtube.com/watch?v=gxt5ZDVnBMM
---
# Test, Containerize, and Deploy an AI-Assisted App

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

Module summary: The companion article takes the local application to a public deployment. It
adds integration and end-to-end tests, packages the frontend and backend in a
container, switches from SQLite to Postgres with Docker Compose, deploys to
AWS, and automates delivery with GitHub Actions.

[Read the article: Deploy a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/deploy-a-full-stack-app-with-ai-coding)

You will:

- Write integration tests that hit a real database, cover migrations, auth, and the frontend-to-backend flow, and are fast enough to run on every push
- Containerize the app with a multi-stage Dockerfile and Docker Compose, swapping SQLite for Postgres
- Set up GitHub Actions CI to run linting, unit tests, integration tests, and the container build on every pull request
- Deploy the app to a public URL on a platform like Render, Fly.io, Railway, or Cloud Run, with a managed database and migrations running on deploy
- Wire up CI/CD so merging to main is gated on the tests and automatically builds, migrates, and redeploys
- Add staging vs. production environments, a post-deploy smoke test, and a documented rollback path

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

## Homework

- [Homework](homework.md) — questions coming

## Previous Cohort Materials

Related material from the previous cohort:

- [2025 archived CI/CD and DevOps module](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/tree/main/cohorts/2025/05-cicd-devops)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

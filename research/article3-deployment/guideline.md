# Guideline

Status: approved

## Reader and promised transformation

The reader finished Article 2 with the interview-canvas application running
locally. Article 3 takes that exact app to a repeatable production-shaped setup:
tested across its real seams, packaged once, backed by Postgres, deployed through
infrastructure as code, and shipped through CI/CD. [HUMAN]

## Thesis and non-goals

The central claim is that AI-assisted deployment should use the same incremental
method as AI-assisted development: ask for one bounded artifact, run it, inspect
the failure, and only then add the next layer.
[INFERENCE article-2-end-to-end,full-stack-workshop-deployment]

This is not a generic cloud comparison, a complete AWS reference, or a claim
that generated deployment files are trustworthy without verification. It should
not return to the workshop's Snake Royale example. [HUMAN]

## Narrative order

1. Open as the third article in the series and recap the Article 2 handoff:
   React, FastAPI, WebSockets, SQLAlchemy, and local SQLite.
   [FACT article-2-end-to-end]
2. Explain the deployment path in one short overview: one image, Postgres,
   Compose, integration tests, AWS, and CI/CD.
   [INFERENCE article-2-end-to-end,full-stack-workshop-deployment]
3. Start the technical walkthrough with containerization. Package frontend and
   backend in one multi-stage image. Preserve the existing
   prompt where possible, but make the validation specific: `npm run build`
   produces `dist/client`, FastAPI serves those files, `/docs` works, and the
   WebSocket path works through port 8000. [FACT interview-canvas-repository]
4. Run the image first with SQLite and a named `/data` volume. Use
   `SDIP_DATABASE_URL`, `interview-canvas`, and `interview-canvas-data` in all
   examples. [FACT interview-canvas-repository]
5. Add a Postgres driver and use `postgresql+psycopg://...`. Explain that the
   SQLAlchemy boundary from Article 2 makes this a small application change, but
   still requires tests. [INFERENCE article-2-end-to-end,full-stack-workshop-deployment]
6. Add `compose.yaml` with `app` and `postgres`, a named Postgres volume, a
   database health check, `depends_on: condition: service_healthy`, and service
   name `postgres` in the database URL. [FACT full-stack-workshop-deployment]
7. Add full-flow integration tests against the containerized stack. Cover the
   application's defining behavior: an interviewer creates a session, a
   candidate joins in another client, a canvas change crosses the WebSocket
   room, and persisted state survives an app restart. Include the
   deliberate-break test: remove or bypass an important behavior and verify the
   suite fails. [INFERENCE interview-canvas-repository]
8. Present AWS as the demonstrated path, with a short managed-host detour. Ask
   the assistant for CloudFormation that provisions managed PostgreSQL, secrets,
   one VM for the app image, HTTPS, WebSocket support, health checks, logs, and a
   public URL. Do not include time-sensitive cost estimates.
   [FACT full-stack-workshop-deployment; INFERENCE interview-canvas-repository]
9. Require the reader to test the public URL with two browser sessions, not just
    trust a successful stack deployment. Verify signup, joining, realtime canvas
    changes, persistence, health checks, and logs. [INFERENCE article-2-end-to-end]
10. Add a GitHub Actions pipeline: frontend and backend tests in parallel,
    integration tests next, deploy only from `main`, smoke-test after deploy, and
    use GitHub OIDC for AWS. [FACT full-stack-workshop-deployment]
11. Remove the temporary admin access key once OIDC works and show how to delete
    the CloudFormation stack so it stops costing money.
    [FACT full-stack-workshop-deployment]
12. End with the boundary between deployment and operations. The next article
    will cover CI/CD maturity, observability, and responding when a deployed app
    fails. [INFERENCE article-2-end-to-end]

## Prompt and command policy

- Keep Article 2's pattern: a short explanation, a copyable prompt, then the
  concrete checks that prove the result. [HUMAN]
- Show commands readers need to validate the result. Avoid pasting large
  generated CloudFormation or workflow files; the linked workshop holds the
  exhaustive walkthrough. [PROPOSAL]
- Use the repository's exact identifiers: `SDIP_DATABASE_URL`, port 8000,
  `dist/client`, and `make test`. [FACT interview-canvas-repository]
- Later sections describe desired generated artifacts because the current repo
  stops at the Dockerfile. Do not write “the assistant creates” as a verified
  fact when the file is absent; write “ask it to create” and explain what to
  inspect. [FACT interview-canvas-repository]

## Voice and structure

- Match Article 2: direct first-person teaching voice, short paragraphs,
  practical prompts, and candid notes about failed first attempts. [HUMAN]
- Prefer concrete checks over broad claims: open two windows, restart the
  container, inspect logs, run migrations against an empty database, and break a
  test on purpose. [INFERENCE article-2-end-to-end,full-stack-workshop-deployment]
- Keep headings descriptive and sentence case. Avoid marketing language,
  excessive warnings, and a catalog of alternatives. [PROPOSAL]

## Counterarguments and tensions

- A managed platform is faster than AWS for a proof of concept. Acknowledge it,
  but retain AWS because it is the workshop's demonstrated infrastructure-as-code
  path and exposes the moving pieces readers need to understand.
  [FACT full-stack-workshop-deployment; PROPOSAL]
- Running Postgres in Compose is easier than managed Postgres, but it does not
  give production backups or failover. Use Compose locally and managed Postgres
  in the cloud. [FACT full-stack-workshop-deployment]
- A green CI run does not prove the application works. Keep a post-deploy smoke
  test and a manual two-browser check in the narrative. [INFERENCE
  article-2-end-to-end,full-stack-workshop-deployment]

## Approved editorial choices

1. Keep AWS/CloudFormation as the main cloud path, with managed platforms as a
   brief shortcut.
2. Skip database migrations in Article 3. Record them as follow-up work rather
   than expanding the deployment walkthrough.
3. Do not claim a live interview-canvas deployment or link to absent deployment
   files.
4. Keep generated configuration concise and emphasize prompts plus validation
   checks; link readers to the full workshop for every step.
5. Start the technical walkthrough with containerization, followed by Postgres,
   Compose, integration tests, deployment, and CI/CD.

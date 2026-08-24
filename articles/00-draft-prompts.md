DRAFT — exact prompts copied verbatim from articles 1, 2, 3, and 4 (Retroloop
for the spec step; Interview Canvas / system-design-interview app for the
rest), PLUS a few newly-written "choose the tool" prompts inserted wherever
a downstream copied prompt hardcodes a specific technology (marked NEW,
never mixed into a copied block). Staged for merge into
00-from-zero-to-production.md.

Nothing inside a copied ```text block is paraphrased. Mid-sentence line
wraps (an artifact of the source articles' line width) have been joined so
prompts read as normal paragraphs on Substack; sentence/directive boundaries
are kept as separate lines exactly where the source had them. Source
citations were dropped from headings to keep them clean for merge — see git
history of this file, or the source articles directly, if you need to trace
a prompt back to its exact line numbers. Non-prompt reference blocks (file
trees, raw file contents) were dropped — only actual instructions given to
an agent are listed. `##` sections match the article's top-level structure;
`###` items are numbered continuously across the whole file.

## Build (from Article 2, spec step from Article 1)

### 1. Specification

Article 2's spec step is done via ChatGPT dictation with no discrete prompt
block (just prose: "For creating the specification, I always use ChatGPT in
dictation mode."). Article 1 has an actual verbatim prompt for this step, so
that's what's copied here:

```text
I want to build a tool for weekly feedback for projects.

Help me set the scope for this project precisely. I want to brainstorm with you and understand how the tool should work. Give me options.

Ask me one question at a time and keep your output short.
```
ADJUST: "I want to build a tool for weekly feedback for projects." -> Study
Relay's one-line pitch. Rest is generic as-is.

### 2. Frontend first, mocked

```text
Create a system design interview application.

[Paste the ChatGPT-generated specification here.]

Centralize every backend call in one services layer, and create a mock implementation of it so the whole app runs without a real backend.

Add tests.
```
ADJUST: "system design interview application" -> Study Relay's description.

### 3. OpenAPI contract

```text
Read the frontend's API client in frontend/

Create openapi.yaml at the repository root.

Specify the backend this frontend expects: every endpoint, method, path, request body, response body, and which endpoints need authentication.
```
ADJUST: nothing app-specific, generic as-is.

### 4. Choose the backend stack

```text
Propose two backend stacks for this application, with the tradeoffs for each. Recommend one and wait for my approval before writing code.
```

### 5. Backend

```text
Build a FastAPI backend in backend/ that implements the openapi.yaml spec.
Use an in-memory store and seed it with data so the frontend has something to show.
Add authentication with hashed passwords and bearer tokens for the endpoints that need it.
Split the code into modules - routers, models, store, auth
Write tests
```
ADJUST: "FastAPI" -> whatever the previous prompt's approved stack is. Keep
FastAPI only if we want a concrete illustrative example rather than a
placeholder.

### 6. Makefile

```text
Create a Makefile so I can easily run it.
```
ADJUST: nothing app-specific, generic as-is.

### 7. Connect frontend and backend

```text
Switch the frontend to use the real backend client.
```
ADJUST: nothing app-specific, generic as-is.

### 8. Database

```text
Replace the in-memory store with a database. Use SQLite and SQLAlchemy
Use an environment variable to configure which DB the server should connect to
Make it database-agnostic - later we will add support for other databases (e.g. postgres)
```
ADJUST: "SQLite and SQLAlchemy" -> whatever the approved backend stack from
item 4 uses. Keep as illustrative example or genericize to "an ORM".

## Deploy (from Article 3)

### 9. Dockerfile

```text
Create a Dockerfile that builds the frontend with Node, then builds a Python image with the backend and the frontend static files.

Backend should serve the frontend.
```
ADJUST: "Node"/"Python" -> whatever frontend/backend stacks were approved.

### 10. Postgres

```text
Add Postgres support to the backend.
```
ADJUST: nothing app-specific, generic as-is.

### 11. Docker Compose

```text
Create docker-compose.yaml with two services: Postgres and the app.
```
ADJUST: nothing app-specific, generic as-is.

### 12. Integration tests

```text
Create integration tests that run against docker-compose.yaml.
What scenarios should we test?
```
ADJUST: nothing app-specific, generic as-is.

### 13. End-to-end test

```text
Add an end-to-end test that runs against docker-compose.yaml.

Use Playwright to:

1. Log in as the interviewer (session 1).
2. Create an interview session.
3. Share the join link.
4. Join from a separate client as the candidate (session 2).
5. Change the canvas as the candidate (session 2).
6. Verify that the interviewer sees the change (session 1).

Put the tests in the e2e/ folder in the repository root.
```
ADJUST: steps 1-6 are entirely interview-canvas-specific (interviewer,
candidate, canvas) — needs a full rewrite to Study Relay's two-sided flow
(host lists a group, a student requests to join, host approves, both
confirm kickoff). "Playwright" is also a specific tool choice — either keep
as the example's pick or genericize to "a browser-automation tool."

### 14. Choose the deployment and CI/CD approach

```text
Propose two ways to deploy and continuously deliver this application, comparing cost, complexity, and portability. Recommend one and wait for my approval before creating any infrastructure.
```

### 15. Deploy to AWS

```text
Deploy this application to AWS. Use AWS CloudFormation.
```
ADJUST: not generic — names AWS and CloudFormation specifically. Now that
item 14 makes the choice explicit, reword to "Deploy this application using
the approved plan" or keep AWS/CloudFormation as the example's concrete
outcome.

### 16. CI/CD pipeline

```text
Create a CI/CD pipeline that:

- runs backend and frontend tests in parallel
- builds the Docker Compose stack and runs integration and end-to-end tests against it
- deploys to AWS using a GitHub OIDC role
- validates that the deploy is successful by checking the health endpoint
```
ADJUST: "AWS"/GitHub OIDC assume the same concrete choice as item 15 — keep
consistent with whatever that prompt lands on, or genericize to "our cloud
provider".

## Operate (from Article 4)

### 17. Second environment

```text
Create a second, independent copy of our infrastructure. We will use the copy as production, and the existing infrastructure as a dev environment.
```
ADJUST: nothing app-specific, generic as-is.

### 18. Manual promotion workflow

```text
Create a manual GitHub Actions workflow that promotes the dev version to production.
```
ADJUST: "GitHub Actions" assumes the CI/CD tool chosen back in item 14 —
keep consistent or genericize to "a manual promotion workflow using our CI
system".

### 19. Split build/deploy, tag images

```text
Currently we build the image during the deploy stage.

Split it into two stages:

- Build: build the image and push it to a container registry (ECR)
- Deploy: pull the image from the registry and serve it

The manual prod promotion CI/CD workflow pulls the currently deployed dev image to prod.

Tag each image using the YYYYMMDD-HHMMSS-shortsha pattern (e.g. "20260818-163457-83242da")
```
ADJUST: "ECR" assumes AWS from item 14 — keep consistent or genericize to
"a container registry".

### 20. Instrument with OpenTelemetry

```text
Instrument the backend with OpenTelemetry.

Include in the telemetry:

- service name
- environment
- deployed version
```
ADJUST: nothing app-specific, generic as-is — OpenTelemetry itself is a
vendor-neutral standard, not a specific product, so no selection prompt
needed here.

### 21. Choose the observability backend

```text
Propose two options for storing and viewing this telemetry — metrics, logs, and traces. Recommend one and wait for my approval.
```

### 22. OTel Collector stack

```text
Add an OpenTelemetry Collector.

Create "observability/" directory with Docker Compose for:

- OpenTelemetry Collector
- Prometheus
- Loki
- Tempo
- Grafana

Keep this as a separate Compose project from the application stack.
```
ADJUST: Prometheus/Loki/Tempo/Grafana -> whatever item 21 approves. Keep as
illustrative example or genericize to "the approved observability stack".

### 23. Application metrics

```text
Track these application metrics:

- interview rooms created
- active interview participants
- canvas elements created
- failures in component creation

Include the environment and deployed version.
```
ADJUST: all four metrics are interview-canvas-specific — rewrite to Study
Relay metrics (e.g. groups created, join requests, kickoff confirmations,
relay registrations, or whatever we settle on).

### 24. Grafana panel

```text
Add a Grafana panel with these metrics.
Make it possible to filter by environment and deployed version
```
ADJUST: "Grafana" assumes item 21's outcome — keep consistent or genericize
to "a dashboard panel".

### 25. Deploy observability stack

```text
Deploy the observability stack. It should be separate from the application stack.
Connect both development and production to it.
```
ADJUST: nothing app-specific, generic as-is.

### 26. Alert

```text
Add an actionable alert for repeated canvas component-creation failures.

Use a threshold and duration that represent real user impact. Include the service, environment, deployed version, owner, and dashboard URL in the alert.
```
ADJUST: "canvas component-creation failures" -> Study Relay equivalent
(e.g. failed join requests or kickoff confirmations).

### 27. On-call worker

```text
Add an on-call-engineer/ directory with a script that polls the observability alert API every minute.

When an alert fires, pass the alert details to a headless coding agent.
```
ADJUST: nothing app-specific, generic as-is.

### 28. On-call agent system prompt

```text
You are the on-call engineer for this repository. An alert just fired.

Investigate the root cause. Read the code and reproduce the failure.
If you find a real bug, make the smallest correction, run the backend tests, and commit the fix with a clear message.
If the alert is a false positive, explain why and do not change the code.
```
ADJUST: nothing app-specific, generic as-is.

### 29. Introduce a bug

```text
Introduce a realistic bug in canvas component creation.

For some requests, creating a component should fail even though the existing tests pass. Keep the failure reproducible so we can test that the bug causes an alert and the on-call response.
```
ADJUST: "canvas component creation" -> Study Relay equivalent (e.g. kickoff
confirmation).

### 30. Clean up

```text
Delete the CloudFormation stacks.
```
ADJUST: not generic — assumes CloudFormation from item 14's outcome. Reword
to something tool-agnostic like "Delete the infrastructure we created for
this exercise" or keep CloudFormation as the example's concrete choice.

## What's Next (no source in articles 2-4 — newly written, same terse style)

### 31. Managed runtime

```text
Evaluate managed runtimes for this container and recommend the simplest one that fits our scaling and budget needs.
```

### 32. Backups and restore

```text
Add scheduled database backups. Restore the latest one into a fresh environment and confirm the data matches.
```

### 33. Reduce public exposure

```text
Put the database and observability stack on a private network. Only the application should be publicly reachable.
```

### 34. Load testing

```text
Load test the busiest endpoint and report throughput, latency, and error rate as concurrency increases.
```

### 35. Progressive delivery

```text
Add canary deployment: route a small percentage of traffic to the new version and roll back automatically on errors.
```

### 36. Recurring assurance review

```text
Set up a monthly agent review of dependencies, unused cloud resources, and open security findings.
```

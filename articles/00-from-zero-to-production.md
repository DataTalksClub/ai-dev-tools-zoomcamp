# From Zero to Production with AI Coding Agents

This is a bonus article in the series based on
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club. Across the series we build an
application with AI coding agents end to end:

- [Build and Ship a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with) builds it
- [Deploy a Full-Stack App with AI Coding Assistants](https://aishippingblog.com/p/deploy-a-full-stack-app-with-ai-coding) deploys it
- [DevOps and Observability for an AI-Built App](https://aishippingblog.com/p/devops-and-observability-for-an-ai) makes it operable

## Intro

This article gives you the whole thing as one ready-to-copy prompt set. When you're working on your own project, whether it's a course project or something of your own, follow these steps in order and you'll end up with an application that works end to end. The steps are ordered by complexity on purpose: stop at any point and you still have something that works, then add the next layer only when you actually need it.

It comes in three parts, matching the three articles above:

- Build
- Deploy
- Operate

That's also how you should think about building your own application, step by step. Not every project needs to reach the Operate stage. A weekend project or a course submission is often done once it's built and deployed, and that's fine too.

Each step gives one goal and one prompt, not a tour of every generated file. The prompts stay tool-agnostic: no assumed language, framework, database, host, CI product, or observability vendor. Where a real choice is needed, the walkthrough asks the agent to propose options and waits for your approval rather than assuming one.

One example carries the whole walkthrough end to end: Study Relay.

A student starts a study group for one leg of a course: a module, a cohort, a few weeks. Other students request to join, and the host approves people up to capacity. Everyone confirms the group actually kicked off. When the leg ends, the host can hand the group's notes and momentum to a new host for the next cohort, who registers their leg as a continuation of the last one, a relay, not a one-off.

## Build

Build follows a deliberate sequence. Write the specification before touching a coding agent, so the idea is explicit rather than assumed. Build the frontend first, behind a mocked backend, to test the idea cheaply. Once the spec is validated against a clickable UI, define the OpenAPI contract, then implement the backend against it. Persistence comes last, once the whole flow is already working.

With frontend, backend, and a database talking to each other locally, the application is ready to leave your machine.

### 1. Specification

If you give a coding agent a vague idea, it fills in the gaps with its own assumptions. Better to brainstorm scope with a reasoning model first, one question at a time so it stays a dialogue rather than a wall of text, then save the result to a file the coding agent can read later.

```text
I want to build a tool for weekly feedback for projects.

Help me set the scope for this project precisely. I want to brainstorm with you and understand how the tool should work. Give me options.

Ask me one question at a time and keep your output short.
```

With scope decided, hand the idea to a coding agent to make it real.

### 2. Frontend first, mocked

We build the frontend before the backend so we can test the idea and the spec while the cost of changing either is still low. The key is centralizing every backend call in one services layer: the mock sits there, and when we swap in a real client later, it's one change in one place. A tool like Lovable, v0, or Bolt can generate a whole frontend from a single prompt, or use a coding agent directly.

```text
Create a system design interview application.

[Paste the ChatGPT-generated specification here.]

Centralize every backend call in one services layer, and create a mock implementation of it so the whole app runs without a real backend.

Add tests.
```

Once the frontend is real and clickable, move it into the project structure the rest of the build will use.

### 3. OpenAPI contract

The OpenAPI contract is the explicit agreement between frontend and backend: every endpoint, request body, response body, and auth rule. Skipping it is possible, but then the backend has to infer its own behavior from the frontend code, and that's a worse target. Reading the frontend's own mocked client to generate the spec means the contract reflects what the UI actually calls, not a guess.

```text
Read the frontend's API client in frontend/

Create openapi.yaml at the repository root.

Specify the backend this frontend expects: every endpoint, method, path, request body, response body, and which endpoints need authentication.
```

With the contract defined, the backend has a precise target to build against. But first, we need to decide what it's built with.

### 4. Choose the backend stack

The coding agent can propose stacks, but we make the call, informed by real tradeoffs. Naming the framework explicitly, rather than letting the agent default to whatever it knows best, keeps the decision intentional.

```text
Propose two backend stacks for this application, with the tradeoffs for each. Recommend one and wait for my approval before writing code.
```

With a stack approved, implement the backend against the contract.

### 5. Backend

Start with an in-memory store so we can verify the frontend-backend connection before persistence is even in the picture. Authentication and authorization belong in this step, not bolted on later. Split routing, models, storage, and auth into separate modules from the start.

```text
Build a FastAPI backend in backend/ that implements the openapi.yaml spec.
Use an in-memory store and seed it with data so the frontend has something to show.
Add authentication with hashed passwords and bearer tokens for the endpoints that need it.
Split the code into modules - routers, models, store, auth
Write tests
```

A Makefile makes the running commands easy to remember and repeat.

### 6. Makefile

Remembering the right run command for every service adds friction that's easy to automate away.

```text
Create a Makefile so I can easily run it.
```

With the backend running, connect it to the frontend that's been running on mocks.

### 7. Connect frontend and backend

Because every backend call was already centralized in one services layer, switching from mock to real is a single, low-risk change.

```text
Switch the frontend to use the real backend client.
```

The app now works end-to-end, but a restart still erases everything. That's next.

### 8. Database

Data has to survive a restart, so we replace the in-memory store with something durable. SQLite is a good first stop: no separate server to run, all state in a single file. Using an ORM and staying database-agnostic sets up a low-friction switch to Postgres later.

```text
Replace the in-memory store with a database. Use SQLite and SQLAlchemy
Use an environment variable to configure which DB the server should connect to
Make it database-agnostic - later we will add support for other databases (e.g. postgres)
```

The application works locally end-to-end. Making it survive contact with the real world is next.

## Deploy

Local success and production success are different problems. Real networking, real databases, and real infrastructure introduce failure modes that a local run never hits. The goal here is one container image, not two: a compiled frontend is just static files the backend can serve directly, so it doesn't need its own container. SQLite was right for development; Postgres is the production-grade swap the ORM already prepared for. Deployment only earns real trust once it's exercised by automated tests and repeated through CI, not run once by hand.

Deployed and tested, the application still needs someone watching it. That's where the operate stage picks up.

### 9. Dockerfile

In development, the frontend runs as its own watched process. In production it's just static files, so it doesn't need its own container. A two-stage build compiles the frontend, then copies only the built files into the backend image.

```text
Create a Dockerfile that builds the frontend with Node, then builds a Python image with the backend and the frontend static files.

Backend should serve the frontend.
```

Build and run the image, then verify the real two-user flow works inside the container.

### 10. Postgres

SQLite didn't need a database server, which kept local development simple. Production needs Postgres's durability and concurrency. Because the backend already used an ORM without SQLite-specific features, the switch is a small, contained change.

```text
Add Postgres support to the backend.
```

Running Postgres by hand works for one command, but the app needs every service defined together.

### 11. Docker Compose

One file that starts the app and its database together beats juggling separate `docker run` commands. A health check makes sure the app waits for Postgres to actually be ready before it starts.

```text
Create docker-compose.yaml with two services: Postgres and the app.
```

With the full stack running together, it's time to test it as a whole, not just its parts.

### 12. Integration tests

The backend may already have tests from earlier steps. If it doesn't, this is the point to add ones that exercise it against a real database.

```text
Create integration tests that run against docker-compose.yaml.
What scenarios should we test?
```

Integration tests catch backend and database problems. An end-to-end test catches problems in the full user flow.

### 13. End-to-end test

Containerizing and switching to Postgres are both changes that can silently break the real user flow. Test that flow directly, running against the same stack that will actually ship.

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

With the whole stack tested, the application is ready to leave our machine for good. But the target platform is still an open question.

### 14. Choose the deployment and CI/CD approach

The cloud provider and CI product are a decision, not a default. Ask for tradeoffs before creating any infrastructure.

```text
Propose two ways to deploy and continuously deliver this application, comparing cost, complexity, and portability. Recommend one and wait for my approval before creating any infrastructure.
```

With a platform approved, deploy the tested artifact to it.

### 15. Deploy to AWS

A temporary admin-level identity is fine for a first deploy, as long as every step is watched closely. A managed database service is a safer choice than colocating the database on the same instance as the app, once you move past a proof of concept.

```text
Deploy this application to AWS. Use AWS CloudFormation.
```

One successful manual deploy is not a repeatable process. CI/CD is what makes it one.

### 16. CI/CD pipeline

Continuous integration catches breakage on every push. Continuous deployment is what turns a passing check into a live release. A short-lived role assumed through OIDC replaces the standing admin credentials used for the first manual deploy.

```text
Create a CI/CD pipeline that:

- runs backend and frontend tests in parallel
- builds the Docker Compose stack and runs integration and end-to-end tests against it
- deploys to AWS using a GitHub OIDC role
- validates that the deploy is successful by checking the health endpoint
```

The application deploys itself now. Keeping it running safely in front of real users is the next problem.

## Operate

Two environments replace one. Development absorbs risk before production does, and we explicitly promote a passing build rather than pushing every commit straight to users. Building the image once and reusing that artifact in production removes an entire class of "worked in dev, broke in prod" problems. Metrics, logs, and traces turn "something broke" into "here's exactly what broke and why." An agent can investigate and propose a fix; a human decides whether it ships.

Rehearsing a real failure, end to end, is the only way to know whether this loop actually works.

### 17. Second environment

Reusing the existing infrastructure-as-code for a second copy means most of the setup transfers directly.

```text
Create a second, independent copy of our infrastructure. We will use the copy as production, and the existing infrastructure as a dev environment.
```

With two environments, CI/CD needs to know the difference between shipping to one and promoting to the other.

### 18. Manual promotion workflow

Development still deploys automatically on every push. Production only moves when a person explicitly approves it.

```text
Create a manual GitHub Actions workflow that promotes the dev version to production.
```

Before that promotion can be trusted, building and deploying need to stop happening as one combined step.

### 19. Split build/deploy, tag images

Building during deploy means a failed build can still trigger a broken deploy, and promoting to production rebuilds the image instead of reusing what was already tested in dev. Tagging every image with a timestamp and commit SHA makes "this exact build" an unambiguous, promotable artifact.

```text
Currently we build the image during the deploy stage.

Split it into two stages:

- Build: build the image and push it to a container registry (ECR)
- Deploy: pull the image from the registry and serve it

The manual prod promotion CI/CD workflow pulls the currently deployed dev image to prod.

Tag each image using the YYYYMMDD-HHMMSS-shortsha pattern (e.g. "20260818-163457-83242da")
```

With a reliable release process in place, the next problem is knowing when something inside it breaks.

### 20. Instrument with OpenTelemetry

Basic infrastructure metrics like CPU and memory hint that something's wrong, but they don't explain what happened inside a request. OpenTelemetry is a vendor-neutral standard, so instrumenting against it doesn't lock us into a specific observability backend.

```text
Instrument the backend with OpenTelemetry.

Include in the telemetry:

- service name
- environment
- deployed version
```

Telemetry is only useful once it's actually collected and stored somewhere we can look at it.

### 21. Choose the observability backend

Where telemetry ends up, which metrics store, log store, trace store, and dashboard, is a real decision with many valid answers, worth asking about explicitly.

```text
Propose two options for storing and viewing this telemetry — metrics, logs, and traces. Recommend one and wait for my approval.
```

With a backend approved, wire up the collector and the dashboards that use it.

### 22. OTel Collector stack

An OpenTelemetry Collector sits between the app and storage, so the app doesn't need to know where telemetry ultimately lands. Running the observability stack as its own Compose project keeps it decoupled from the application stack.

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

Raw telemetry only becomes useful once it's turned into metrics worth looking at.

### 23. Application metrics

Generic infrastructure metrics don't tell you if the product itself is working. Track what users are actually doing instead. Tagging every metric with environment and version is what makes a regression visible by release.

```text
Track these application metrics:

- interview rooms created
- active interview participants
- canvas elements created
- failures in component creation

Include the environment and deployed version.
```

Metrics only help if there's somewhere to actually see them.

### 24. Grafana panel

A dashboard that can't be filtered by environment and version can't answer "did the last release cause this."

```text
Add a Grafana panel with these metrics.
Make it possible to filter by environment and deployed version
```

The dashboard works locally. Now the observability stack itself needs to be deployed.

### 25. Deploy observability stack

Observability infrastructure gets deployed like anything else: separately from the app, but reachable by both environments.

```text
Deploy the observability stack. It should be separate from the application stack.
Connect both development and production to it.
```

Dashboards need a human watching them. Alerts don't.

### 26. Alert

A metric can silently degrade for hours if nobody's watching the dashboard. An alert is what forces attention. A threshold tuned for real user impact, with an owner and a dashboard link attached, is what makes an alert actionable rather than noise.

```text
Add an actionable alert for repeated canvas component-creation failures.

Use a threshold and duration that represent real user impact. Include the service, environment, deployed version, owner, and dashboard URL in the alert.
```

Once an alert can fire, something has to actually respond to it.

### 27. On-call worker

Polling the alert API and handing the details to a headless coding agent is the entire on-call loop in miniature.

```text
Add an on-call-engineer/ directory with a script that polls the observability alert API every minute.

When an alert fires, pass the alert details to a headless coding agent.
```

What that agent is allowed to do with an alert needs to be spelled out explicitly.

### 28. On-call agent system prompt

The agent should investigate first, reproduce the failure, and only patch if the fix is small, tested, and committed to an isolated branch. It never deploys directly. A false positive gets explained, not "fixed" by changing code that wasn't actually broken.

```text
You are the on-call engineer for this repository. An alert just fired.

Investigate the root cause. Read the code and reproduce the failure.
If you find a real bug, make the smallest correction, run the backend tests, and commit the fix with a clear message.
If the alert is a false positive, explain why and do not change the code.
```

The only way to know this actually works is to break something on purpose.

### 29. Introduce a bug

We need a bug that's reproducible but still passes the existing test suite. That's exactly the kind of regression this whole loop exists to catch.

```text
Introduce a realistic bug in canvas component creation.

For some requests, creating a component should fail even though the existing tests pass. Keep the failure reproducible so we can test that the bug causes an alert and the on-call response.
```

After the on-call agent proves it can wake up and respond, the exercise and its temporary resources should be cleaned up.

### 30. Clean up

Resources created for learning cost money if left running. Tear them down as deliberately as they were created.

```text
Delete the CloudFormation stacks.
```

That's the credible minimum loop. Real products keep going from here.

## Going Further

None of the topics below are covered in the walkthrough above. They're what's still missing once the minimum loop works. A single hand-deployed instance and a hand-run backup are both fine for learning, but neither holds up under real usage or a real incident. Each prompt builds on a decision already made earlier in the walkthrough: the platform, the database, the deployment pipeline. None start from scratch.

These prompts are what it takes to make the loop production-grade, not just working.

### 31. Managed runtime

A hand-run container is fine for learning. A managed platform handles restarts, placement, and scaling without anyone watching it.

```text
Evaluate managed runtimes for this container and recommend the simplest one that fits our scaling and budget needs.
```

The runtime can scale the app, but the data still needs a plan for disaster.

### 32. Backups and restore

A backup nobody has restored is a guess, not a safety net.

```text
Add scheduled database backups. Restore the latest one into a fresh environment and confirm the data matches.
```

Even a perfectly backed-up app is only as safe as the network it's exposed on.

### 33. Reduce public exposure

The database and observability stack don't need to be reachable from the public internet. Only the application does.

```text
Put the database and observability stack on a private network. Only the application should be publicly reachable.
```

A safely exposed app still needs to prove it holds up under real load.

### 34. Load testing

Correctness under one user says nothing about correctness under a thousand. Measure it before real traffic finds the limit.

```text
Load test the busiest endpoint and report throughput, latency, and error rate as concurrency increases.
```

Once we know where the limits are, releases can start rolling out more carefully too.

### 35. Progressive delivery

Promoting a build to 100% of users at once means a bad release affects everyone at once. A canary limits the blast radius.

```text
Add canary deployment: route a small percentage of traffic to the new version and roll back automatically on errors.
```

None of this replaces vigilance. It has to be revisited on a schedule, not set up once and forgotten.

### 36. Recurring assurance review

Dependencies, unused resources, and open findings all drift over time. A one-time audit doesn't stay true.

```text
Set up a monthly agent review of dependencies, unused cloud resources, and open security findings.
```


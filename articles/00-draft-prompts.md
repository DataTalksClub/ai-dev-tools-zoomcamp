DRAFT — exact prompts copied verbatim from articles 1, 2, 3, and 4 (Retroloop
for the spec step; Interview Canvas / system-design-interview app for the
rest), PLUS a few newly-written "choose the tool" prompts inserted wherever
a downstream copied prompt hardcodes a specific technology. Staged for merge
into 00-from-zero-to-production.md — Sonnet 4.6 will turn this into full
article prose next.

Nothing inside a copied ```text block is paraphrased. Mid-sentence line
wraps (an artifact of the source articles' line width) have been joined so
prompts read as normal paragraphs on Substack; sentence/directive boundaries
are kept as separate lines exactly where the source had them. Non-prompt
reference blocks (file trees, raw file contents) were dropped — only actual
instructions given to an agent are listed.

Structure: each `##` and `###` section has 2-4 bullet points before its
content (grounded in what the source article actually said, not invented)
and a one-line transition at the end leading into what's next. `###` items
are numbered continuously across the whole file.

## Build (from Article 2, spec step from Article 1)

- A specification turns a vague idea into decisions before any code exists.
- Build the visible workflow first, behind a mocked backend, to test the idea cheaply before investing in a server.
- Define the contract (OpenAPI) explicitly so the backend has a precise target instead of inferring behavior from frontend code.
- Only add real persistence once frontend and backend are already talking to each other through the contract.

With frontend, backend, and a database talking to each other locally, the application is ready to leave your machine.

### 1. Specification

Article 2's spec step is done via ChatGPT dictation with no discrete prompt
block (just prose: "For creating the specification, I always use ChatGPT in
dictation mode."). Article 1 has an actual verbatim prompt for this step, so
that's what's copied here.

- A vague idea gets filled in with the agent's own assumptions if you don't specify it first.
- Brainstorm scope conversationally before touching a coding agent — one question at a time keeps it a dialogue, not a wall of text.
- Save the result to a file the coding agent can read later.

```text
I want to build a tool for weekly feedback for projects.

Help me set the scope for this project precisely. I want to brainstorm with you and understand how the tool should work. Give me options.

Ask me one question at a time and keep your output short.
```
ADJUST: "I want to build a tool for weekly feedback for projects." -> Study
Relay's one-line pitch. Rest is generic as-is.

With scope decided, hand the idea to a coding agent to make it real.

### 2. Frontend first, mocked

- Test the idea and the specification before building the rest of the application.
- Centralizing every backend call in one services layer means the mock becomes the single integration point later.
- A tool like Lovable, v0, or Bolt (or a coding agent directly) can generate a whole frontend from one prompt.

```text
Create a system design interview application.

[Paste the ChatGPT-generated specification here.]

Centralize every backend call in one services layer, and create a mock implementation of it so the whole app runs without a real backend.

Add tests.
```
ADJUST: "system design interview application" -> Study Relay's description.

Once the frontend is real and clickable, move it into the project structure the rest of the build will use.

### 3. OpenAPI contract

- The contract is the explicit agreement between frontend and backend: every endpoint, request, response, and auth rule.
- Skipping this step is possible, but it costs a clear picture of what the backend actually needs to do.
- Reading the frontend's own mocked client to generate the contract means it reflects what the UI actually calls, not a guess.

```text
Read the frontend's API client in frontend/

Create openapi.yaml at the repository root.

Specify the backend this frontend expects: every endpoint, method, path, request body, response body, and which endpoints need authentication.
```
ADJUST: nothing app-specific, generic as-is.

With the contract defined, the backend has a precise target to build against — but only after deciding what it's built with.

### 4. Choose the backend stack

- The coding agent can propose stacks, but you make the call, informed by real tradeoffs.
- Naming the framework up front, rather than letting the agent default to whatever it knows best, keeps this walkthrough tool-agnostic.

```text
Propose two backend stacks for this application, with the tradeoffs for each. Recommend one and wait for my approval before writing code.
```

With a stack approved, implement the backend against the contract.

### 5. Backend

- Start with an in-memory store so the frontend-backend connection can be verified before persistence is a factor.
- Authentication and authorization belong in this step, not bolted on later.
- Split routing, models, storage, and auth into separate modules from the start.

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

A Makefile makes the running commands easy to remember and repeat.

### 6. Makefile

- Remembering the right run command for every service adds friction that's easy to automate away.

```text
Create a Makefile so I can easily run it.
```
ADJUST: nothing app-specific, generic as-is.

With the backend running, connect it to the frontend that's been running on mocks.

### 7. Connect frontend and backend

- Because every backend call was already centralized in one services layer, switching from mock to real is a single, low-risk change.

```text
Switch the frontend to use the real backend client.
```
ADJUST: nothing app-specific, generic as-is.

The app now works end-to-end, but a restart still erases everything — that's next.

### 8. Database

- Data must survive a restart, so replace the in-memory store with something durable.
- SQLite is a good first stop: no separate server to run, all state in a single file.
- Using an ORM and staying database-agnostic sets up a low-friction switch to Postgres later.

```text
Replace the in-memory store with a database. Use SQLite and SQLAlchemy
Use an environment variable to configure which DB the server should connect to
Make it database-agnostic - later we will add support for other databases (e.g. postgres)
```
ADJUST: "SQLite and SQLAlchemy" -> whatever the approved backend stack from
item 4 uses. Keep as illustrative example or genericize to "an ORM".

The application works locally end-to-end. Making it survive contact with the real world — deployment — is next.

## Deploy (from Article 3)

- Local success and production success are different problems: real networking, real databases, and real infrastructure introduce new failure modes.
- One container image, not two — a compiled frontend is static files the backend can serve directly.
- SQLite was right for development; Postgres is the production-grade swap the ORM already prepared for.
- Deployment only earns trust once it's exercised by real tests and repeated through CI, not run once by hand.

Deployed and tested, the application still needs someone watching it — that's where the operate stage picks up.

### 9. Dockerfile

- In development, the frontend runs as its own watched process; in production it's just static files, so it doesn't need its own container.
- A two-stage build compiles the frontend, then copies only the built files into the backend image.

```text
Create a Dockerfile that builds the frontend with Node, then builds a Python image with the backend and the frontend static files.

Backend should serve the frontend.
```
ADJUST: "Node"/"Python" -> whatever frontend/backend stacks were approved.

Build and run the image, then verify the real two-user flow works inside the container.

### 10. Postgres

- SQLite didn't need a database server, which made local development simple; production needs Postgres's durability and concurrency guarantees.
- Because the backend already used an ORM without SQLite-specific features, the switch is a small, contained change.

```text
Add Postgres support to the backend.
```
ADJUST: nothing app-specific, generic as-is.

Running Postgres by hand works for one command, but the app needs every service defined together.

### 11. Docker Compose

- One file that starts the app and its database together beats juggling separate `docker run` commands.
- A health check makes sure the app waits for Postgres to actually be ready before it starts.

```text
Create docker-compose.yaml with two services: Postgres and the app.
```
ADJUST: nothing app-specific, generic as-is.

With the full stack running together, it's time to test it as a whole, not just its parts.

### 12. Integration tests

- The backend may already have some tests from earlier steps; if it doesn't, this is the point to add ones that exercise it against a real database.

```text
Create integration tests that run against docker-compose.yaml.
What scenarios should we test?
```
ADJUST: nothing app-specific, generic as-is.

Integration tests catch backend/database problems; an end-to-end test catches problems in the full user flow.

### 13. End-to-end test

- Containerizing and switching to Postgres are both changes that can silently break the real user flow — test that flow directly.
- Running against docker-compose.yaml means the test exercises the same stack that will actually ship.

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

With the whole stack tested, the application is ready to leave your machine for good — but the target platform is still an open question.

### 14. Choose the deployment and CI/CD approach

- The cloud provider and CI product are a decision, not a default — ask for tradeoffs before creating any infrastructure.

```text
Propose two ways to deploy and continuously deliver this application, comparing cost, complexity, and portability. Recommend one and wait for my approval before creating any infrastructure.
```

With a platform approved, deploy the tested artifact to it.

### 15. Deploy to AWS

- A temporary admin-level identity is fine for the first deploy, as long as every step is watched closely.
- A managed database service is a safer choice than colocating the database on the same instance as the app, once you move past a proof of concept.

```text
Deploy this application to AWS. Use AWS CloudFormation.
```
ADJUST: not generic — names AWS and CloudFormation specifically. Now that
item 14 makes the choice explicit, reword to "Deploy this application using
the approved plan" or keep AWS/CloudFormation as the example's concrete
outcome.

One successful manual deploy is not a repeatable process — CI/CD is what makes it one.

### 16. CI/CD pipeline

- Continuous integration catches breakage on every push; continuous deployment is what turns a passing check into a live release.
- A short-lived role assumed through OIDC replaces the standing admin credentials used for the first manual deploy.

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

The application deploys itself now. Keeping it running safely in front of real users is the next problem.

## Operate (from Article 4)

- Deploying every push straight to what users see is fine early on, but real users need a buffer: a development environment that absorbs risk before production does.
- Building the image once and promoting that same artifact to production removes an entire class of "worked in dev, broke in prod" bugs.
- Telemetry — metrics, logs, traces — is what turns "something broke" into "here's exactly what broke and why."
- An agent can investigate and even fix incidents, but only a human decides what reaches production.

Rehearsing a real failure, end to end, is the only way to know whether this loop actually works.

### 17. Second environment

- Reusing the existing infrastructure-as-code for a second copy means most of the setup transfers directly.

```text
Create a second, independent copy of our infrastructure. We will use the copy as production, and the existing infrastructure as a dev environment.
```
ADJUST: nothing app-specific, generic as-is.

With two environments, CI/CD needs to know the difference between shipping to one and promoting to the other.

### 18. Manual promotion workflow

- Development still deploys automatically on every push; production only moves when a person explicitly approves it.

```text
Create a manual GitHub Actions workflow that promotes the dev version to production.
```
ADJUST: "GitHub Actions" assumes the CI/CD tool chosen back in item 14 —
keep consistent or genericize to "a manual promotion workflow using our CI
system".

Before that promotion can be trusted, building and deploying need to stop happening as one combined step.

### 19. Split build/deploy, tag images

- Building during deploy means a failed build can still trigger a broken deploy, and promoting to prod rebuilds instead of reusing what was already tested in dev.
- Tagging every image with a timestamp and commit SHA makes "this exact build" an unambiguous, promotable thing.

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

With a reliable release process in place, the next problem is knowing when something inside it breaks.

### 20. Instrument with OpenTelemetry

- Basic infrastructure metrics (CPU, memory, requests per second) hint that something's wrong but don't explain what happened inside a request.
- OpenTelemetry is a vendor-neutral standard, so instrumenting against it doesn't lock in a specific observability backend.

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

Telemetry is only useful once it's actually collected and stored somewhere you can look at it.

### 21. Choose the observability backend

- Where telemetry ends up — which metrics store, log store, trace store, dashboard — is a real decision with many valid answers, worth asking about explicitly.

```text
Propose two options for storing and viewing this telemetry — metrics, logs, and traces. Recommend one and wait for my approval.
```

With a backend approved, wire up the collector and the dashboards that use it.

### 22. OTel Collector stack

- An OpenTelemetry Collector sits between the app and storage, so the app doesn't need to know where telemetry ultimately lands.
- Running the observability stack as its own Compose project keeps it decoupled from the application stack.

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

Raw telemetry only becomes useful once it's turned into metrics worth looking at.

### 23. Application metrics

- Generic infrastructure metrics don't tell you if the product itself is working — track what users are actually doing instead.
- Tagging every metric with environment and version is what makes a regression visible by release.

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

Metrics only help if there's somewhere to actually see them.

### 24. Grafana panel

- A dashboard that can't be filtered by environment and version can't answer "did the last release cause this."

```text
Add a Grafana panel with these metrics.
Make it possible to filter by environment and deployed version
```
ADJUST: "Grafana" assumes item 21's outcome — keep consistent or genericize
to "a dashboard panel".

The dashboard works locally — now the observability stack itself needs to be deployed.

### 25. Deploy observability stack

- Observability infrastructure gets deployed like anything else: separately from the app, but reachable by both environments.

```text
Deploy the observability stack. It should be separate from the application stack.
Connect both development and production to it.
```
ADJUST: nothing app-specific, generic as-is.

Dashboards need a human watching them; alerts don't.

### 26. Alert

- A metric can silently degrade for hours if nobody's watching the dashboard — an alert is what forces attention.
- A threshold tuned for low traffic and an owner/dashboard link attached to the alert are what make it actionable instead of noise.

```text
Add an actionable alert for repeated canvas component-creation failures.

Use a threshold and duration that represent real user impact. Include the service, environment, deployed version, owner, and dashboard URL in the alert.
```
ADJUST: "canvas component-creation failures" -> Study Relay equivalent
(e.g. failed join requests or kickoff confirmations).

Once an alert can fire, something has to actually respond to it.

### 27. On-call worker

- Polling the alert API and handing the details to a headless coding agent is the entire on-call loop in miniature.

```text
Add an on-call-engineer/ directory with a script that polls the observability alert API every minute.

When an alert fires, pass the alert details to a headless coding agent.
```
ADJUST: nothing app-specific, generic as-is.

What that agent is allowed to do with an alert needs to be spelled out explicitly.

### 28. On-call agent system prompt

- Investigate first, reproduce the failure, and only patch if the fix is small, tested, and committed to an isolated branch — never deployed directly.
- A false positive should be explained, not "fixed" by changing code that wasn't actually broken.

```text
You are the on-call engineer for this repository. An alert just fired.

Investigate the root cause. Read the code and reproduce the failure.
If you find a real bug, make the smallest correction, run the backend tests, and commit the fix with a clear message.
If the alert is a false positive, explain why and do not change the code.
```
ADJUST: nothing app-specific, generic as-is.

The only way to know this actually works is to break something on purpose.

### 29. Introduce a bug

- A bug that's reproducible but still passes the existing test suite is exactly the kind of regression this whole loop exists to catch.

```text
Introduce a realistic bug in canvas component creation.

For some requests, creating a component should fail even though the existing tests pass. Keep the failure reproducible so we can test that the bug causes an alert and the on-call response.
```
ADJUST: "canvas component creation" -> Study Relay equivalent (e.g. kickoff
confirmation).

After the on-call agent proves it can wake up and respond, the exercise — and its temporary resources — should be cleaned up.

### 30. Clean up

- Resources created for learning cost money if left running — tear them down as deliberately as they were created.

```text
Delete the CloudFormation stacks.
```
ADJUST: not generic — assumes CloudFormation from item 14's outcome. Reword
to something tool-agnostic like "Delete the infrastructure we created for
this exercise" or keep CloudFormation as the example's concrete choice.

That's the credible minimum loop. Real products keep going from here.

## What's Next (no source in articles 2-4 — newly written, same terse style)

- A single hand-deployed instance and a hand-run backup are both fine for learning, but neither holds up under real usage or a real incident.
- Each of these extends a decision already made earlier in the walkthrough — the platform, the database, the deployment pipeline — rather than starting something new.

None of these are required to call the loop complete — they're where to go once it is.

### 31. Managed runtime

- A hand-run container is fine for learning; a managed platform is what handles restarts, placement, and scaling without you watching it.

```text
Evaluate managed runtimes for this container and recommend the simplest one that fits our scaling and budget needs.
```

The runtime can scale the app, but the data still needs a plan for disaster.

### 32. Backups and restore

- A backup nobody has restored is a guess, not a safety net.

```text
Add scheduled database backups. Restore the latest one into a fresh environment and confirm the data matches.
```

Even a perfectly backed-up app is only as safe as the network it's exposed on.

### 33. Reduce public exposure

- The database and observability stack don't need to be reachable from the public internet — only the application does.

```text
Put the database and observability stack on a private network. Only the application should be publicly reachable.
```

A safely exposed app still needs to prove it holds up under real load.

### 34. Load testing

- Correctness under one user says nothing about correctness under a thousand — measure it before real traffic finds the limit.

```text
Load test the busiest endpoint and report throughput, latency, and error rate as concurrency increases.
```

Once you know where the limits are, releases can start rolling out more carefully too.

### 35. Progressive delivery

- Promoting a build to 100% of users at once means a bad release affects everyone at once — a canary limits the blast radius.

```text
Add canary deployment: route a small percentage of traffic to the new version and roll back automatically on errors.
```

None of this replaces vigilance — it has to be revisited on a schedule, not set up once and forgotten.

### 36. Recurring assurance review

- Dependencies, unused resources, and open findings all drift over time — a one-time audit doesn't stay true.

```text
Set up a monthly agent review of dependencies, unused cloud resources, and open security findings.
```

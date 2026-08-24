# From Zero to Production with AI Coding Agents

This is the introductory article in a series based on
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp),
the free course we run at DataTalks.Club.

THESIS: this article compresses the whole course arc — build, deploy, operate —
into one path. Not a full walkthrough of every generated file; one goal and one
focused prompt per step. Prompts are tool-agnostic (no assumed language,
framework, database, host, CI, observability vendor, model provider) — put
preferences in project instructions, or ask the agent to propose a stack and
approve it first. Points ahead to the deeper articles later in the series for
each stage.

## The Example: Study Relay

I needed an example app that would exercise every stage below without turning
into a tutorial about the app itself. A few candidates came up along the way:
a GPU time-share ledger for a lab, a homework-review swap for a course, a
dry-run feedback exchange for conference speakers. Any of them would have
worked. I went with **Study Relay**, because organizing a study group is a
problem most of this newsletter's readers have tried and abandoned at least
once.

A student starts a study group for one leg of a course — a module, a cohort,
a few weeks. Other students request to join, and the host approves people up
to capacity. Everyone confirms the group actually kicked off. When the leg
ends, the host can hand the group's notes and momentum to a new host for the
next cohort, who registers their leg as a continuation of the last one — a
relay, not a one-off.

It's a small idea, but it forces the same hard parts as a "real" product:
accounts and roles, state that moves through defined transitions, data that
has to survive a restart, two people racing for the same open seat, uploaded
content that needs moderation, and eventually a production incident someone
has to actually diagnose.

## The Target

THESIS: a public URL is not the finish line. By the end:

- a person can complete the main workflow over the network;
- important behavior is covered by automated checks;
- one immutable artifact moves through environments;
- development and production are separated;
- failures produce correlated evidence;
- an alert represents sustained user impact;
- rollback and restore paths have been practiced;
- secrets, data, infrastructure, and agent permissions are bounded.

Run every result yourself — an agent claiming success is not verification.

## 1. Write the Specification

THESIS: a spec turns enthusiasm into decisions; capture actors, journeys,
state rules, privacy, failure cases, and acceptance criteria before asking
for implementation.

```text
You are an experienced product manager. Help me specify a small web
application called Study Relay.

Product intent:
Students organize study groups around one leg of a course. A host lists a
group with its topic, schedule, and seat capacity. Other students request to
join, the host approves members up to capacity, and everyone confirms the
group's kickoff session happened. When a leg ends, the host can hand it off:
a new host registers their group as a continuation of the previous leg,
carrying forward a short handoff note. Members can add session notes and
photos. Moderators can hide abusive content.

Produce docs/spec.md with:

- goals, non-goals, personas, and permissions;
- the three most important end-to-end journeys;
- entities and relationships, including group listings, join requests,
  kickoff confirmations, group profiles, relay links between legs, session
  notes, photos, and moderation reports;
- group and join-request states with allowed transitions;
- rules preventing two students from filling the same last open seat;
- privacy, retention, moderation, accessibility, and abuse-prevention rules;
- launch acceptance criteria written so QA can test them without guessing.

Ask up to five clarifying questions first. Do not implement anything.
```

## 2. Create the Working Agreement

THESIS: give the agent durable context before generating a lot of code —
require small diffs, tests, and honest uncertainty up front.

```text
Create AGENTS.md at the repository root.

Tell future coding agents how to work here:

- read docs/spec.md before changing product behavior;
- keep diffs small and reviewable;
- run formatting, linting, type checks, and tests when they exist;
- discover missing commands from project files instead of inventing them;
- never commit secrets, credentials, private addresses, or environment values;
- summarize what changed, how it was verified, and what remains uncertain;
- stop before destructive actions, dependency additions, infrastructure
  changes, or work outside the stated task.

Also create docs/decisions.md for concise architecture decisions and
docs/runbook.md for local development, verification, deployment, operations,
and teardown.
```

## 3. Choose the Stack Deliberately

THESIS: the agent can recommend a stack, but you own the choice — ask for
options and tradeoffs instead of letting the first scaffold decide.

```text
Read docs/spec.md and AGENTS.md.

Propose two suitable technology stacks. For each option explain:

- why it fits Study Relay;
- local developer experience;
- deployment portability;
- testing strategy;
- operational and security considerations;
- expected maintenance burden.

Recommend one option, identify its main risks, and wait for my approval.
Do not create files yet.
```

## 4. Prototype Behind Fake Services

THESIS: build the visible workflow before the server; every network call sits
behind one boundary so mocks swap out cleanly later.

```text
Create the smallest usable client application for the approved specification.

Implement these flows:

1. A student signs in and lists a study group with a topic, schedule, and
   seat capacity.
2. Another student browses open groups and requests to join one.
3. The host sees requests and approves members up to capacity.
4. Members confirm the kickoff session happened.
5. When a leg ends, a new host registers their group as a continuation of the
   previous one, carrying forward a handoff note.
6. Everyone sees the relevant status without being able to edit someone
   else's confirmation.

Centralize every server call behind one application service layer. Implement
that layer with deterministic mock data so the whole experience runs without
a server.

Add behavioral tests for navigation, form validation, permission boundaries,
invalid state changes, and the main success path. Update docs/runbook.md with
exact commands to install, run, and verify the prototype.
```

THESIS: walk through both roles yourself; a wrong flow is cheaper to fix in
the spec now than in the integrated system later.

## 5. Define the Integration Contract

THESIS: the contract is the client/service agreement — operations, fields,
errors, auth, side effects — so the backend has a precise target instead of
inferring behavior from screens.

```text
Read the centralized client service layer and docs/spec.md.

Create a machine-readable API contract at the repository root using a widely
supported contract format appropriate to the chosen stack.

Describe every operation needed by the implemented prototype:

- route or procedure identifier;
- request and response fields;
- validation limits and normalized error responses;
- authentication and role requirements;
- state transition performed;
- pagination, filtering, and concurrency controls where needed.

Do not implement the service yet. Add a check that fails when the client
service layer and contract disagree.
```

## 6. Implement the Service with Temporary State

THESIS: connect the real halves while persistence is still simple, so
contract mismatches stay isolated from database problems.

```text
Implement a backend service that satisfies the approved contract.

Requirements:

- follow AGENTS.md and reuse the approved stack;
- put all storage behind a repository or store interface;
- implement the first store in memory with deterministic seed data;
- enforce authentication, ownership, moderator permissions, validation, and
  allowed state transitions;
- return the errors defined by the contract;
- split routing, application logic, contracts, authentication, storage, and
  configuration into clear modules;
- switch the client from the mock adapter to the transport-backed adapter;
- preserve the mock adapter for story-level development and tests;
- add unit and integration tests for successful paths, unauthorized actions,
  invalid submissions, forbidden transitions, and double kickoff confirmation;
- document commands to run each side and all tests.
```

THESIS: test the journey in two isolated sessions — host and joining student
— then try an invalid action and one outside that actor's permission.

## 7. Add Durable State Carefully

THESIS: a restart must not erase groups, requests, or relay links; keep
storage details out of business rules so production can differ from dev.

```text
Replace the in-memory store with durable storage.

Requirements:

- keep application logic independent of the specific database product;
- configure connections only through environment variables;
- provide safe local defaults and explicit configuration for hosted
  environments;
- use versioned migrations with safe up behavior and meaningful down behavior
  where practical;
- prevent destructive migrations from running against production by accident;
- wrap seat approval and related state changes in a transaction;
- guarantee that two concurrent approvals cannot both fill the last open seat;
- prove records survive a process restart;
- add tests for migrations, restart survival, transactions, and concurrent
  join attempts;
- list required variables without putting real secret values in the
  repository.
```

THESIS: create a few records, restart the service, confirm they're still there.

## 8. Prove the Whole System Locally

THESIS: make verification boring before deployment — the last cheap place to
catch contract drift, race conditions, bad config, missing migrations.

```text
Create automated checks that prove the complete system works locally.

Include:

- unit tests for domain rules;
- contract tests for the client-service agreement;
- integration tests for service and storage;
- one end-to-end test for listing a group, requesting to join, approving,
  confirming kickoff, and registering the next leg;
- tests for concurrent join attempts;
- checks for formatting, linting, types, and known vulnerabilities where the
  stack provides reasonable options.

Make every check runnable through documented commands. Add one local
verification command that tells me whether the project is ready to commit.
Update docs/runbook.md with setup, run, test, troubleshooting, and cleanup
steps.
```

THESIS: run the verification command yourself and review the diff before
committing.

## 9. Package What You Tested

THESIS: production gets repeatable once you release the exact artifact you
tested, not a rebuild from whatever's installed on some machine.

```text
Prepare the application for deployment as a reproducible release artifact.

Requirements:

- choose packaging appropriate to the approved stack, such as a portable
  container image or another immutable executable package;
- separate build dependencies from runtime dependencies;
- exclude development files and secrets;
- run as an unprivileged identity where the runtime supports it;
- expose readiness and liveness health checks;
- read environment-specific configuration from the environment;
- print a stable release identifier containing the UTC date/time and source
  revision;
- serve the built client from the application process unless there is a
  documented reason to deploy them separately;
- add a check that builds the artifact, starts it, waits for health,
  exercises one critical workflow, stops it cleanly, and prints its logs on
  failure;
- document local build, run, smoke-test, and cleanup commands.
```

THESIS: verify the packaged artifact, not the development servers.

## 10. Deploy to a Non-Production Environment

THESIS: the first hosted environment is not production — it's where you learn
whether networking, config, domains, TLS, storage, startup, health checks
actually work.

```text
Prepare deployment to a non-production environment.

Before changing infrastructure:

1. list required resources and configuration;
2. propose the least-privilege deployment identity;
3. identify billable, persistent, public, and sensitive resources;
4. show the planned steps, estimated blast radius, and teardown path;
5. wait for my approval.

Then encode the approved deployment as reviewed infrastructure/configuration.

Configure:

- non-production secrets through the platform's supported mechanism;
- durable storage for the datastore and uploaded photos;
- HTTPS for externally accessible traffic;
- health checks and restart behavior;
- access to logs and metrics;
- labels identifying project, environment, owner, and purpose.

Finish by deploying the current artifact and completing the join-and-approve
journey against the deployed URL. Record every resource and its removal path
in docs/runbook.md.
```

THESIS: use the narrowest credentials that allow the deployment; watch
irreversible actions closely.

## 11. Add Continuous Integration

THESIS: CI protects the main branch — every proposed change gets built and
checked before a human merges it.

```text
Set up continuous integration using this repository's supported automation
system.

On pull requests:

- install dependencies reproducibly;
- discover and run formatting, linting, type, unit, contract, integration,
  and end-to-end checks;
- build the release artifact;
- scan dependencies and configuration for high-severity issues where
  practical;
- upload logs, test results, and artifacts needed to debug a failure;
- fail on incomplete runs, skipped required checks, or untrusted
  configuration changes.

Use minimum credentials. CI should not deploy unless I explicitly add that in
a separate controlled step. Document every variable and secret without
exposing values.
```

THESIS: open a PR with a harmless change, then break a check on purpose and
confirm the pipeline catches it.

## 12. Deploy Development Automatically

THESIS: once CI is trustworthy, merging can deploy to development
automatically — keep it observable and reversible.

```text
Extend delivery so a merge to the main branch:

1. runs the pull-request checks;
2. builds and publishes exactly one uniquely tagged immutable artifact;
3. deploys that tagged artifact to development;
4. applies migrations according to their safety classification;
5. waits for readiness and liveness checks;
6. runs a smoke test for the main workflow;
7. records artifact identifier, digest, source revision, deployment time,
   workflow link, migration status, smoke-test result, and previous good
   artifact;
8. preserves a tested rollback path.

Use short-lived least-privilege deployment credentials. Do not deploy
directly to production. Make failed deployments visibly fail while leaving
the previous healthy release running.
```

THESIS: push a harmless change and watch it all the way to a verified
development URL.

## 13. Separate Production Promotion

THESIS: development can receive every merged change; production should
receive only a release someone chose to promote.

```text
Create an independent production environment using the same deployment
mechanics, but separate configuration, credentials, datastore, object
storage, domains, logs, metrics, backups, and data.

Automatic deployment goes only to development. Add a manual production
promotion flow that requires a person to:

- choose an already-published artifact;
- see its digest, source revision, tests, migration status, changelog, and
  deployment time;
- confirm the release intentionally;
- promote that exact artifact without rebuilding it;
- apply preflight checks for migrations, configuration, health, rollback
  target, and monitoring;
- run health checks and a production-safe smoke test;
- roll back automatically on failed startup, health, or smoke test where the
  platform supports it;
- record who promoted what, when, why, and whether recovery was verified.

Show me the approval and rollback paths before enabling promotion.
```

THESIS: promote once, test the real workflow, and practice finding and
deploying the previous artifact before you actually need it during an
incident.

## 14. Instrument the Application

THESIS: a process starting successfully is not the same as users succeeding
— metrics show trends, traces show request paths, structured logs preserve
detail the other two flatten out.

```text
Instrument Study Relay using the standard telemetry approach for the
approved stack.

Collect structured logs, metrics, distributed traces, and health signals for:

- group creation, publication, expiration, and closing;
- join requests, approvals, rejections, cancellations, and expiry;
- kickoff confirmations and stalled confirmations;
- relay registrations linking a new leg to the one before it;
- note and photo uploads;
- moderation actions;
- authentication and authorization failures;
- storage, queue, notification, and dependency failures;
- request count, error count, latency, saturation, and active instances.

Attach stable service name, environment, release version, request
identifier, actor role, and anonymized entity identifiers where appropriate.
Never log passwords, tokens, private contact details, photo contents, or
unnecessary free text. Export telemetry through configurable endpoints and
protocols, and document how to inspect each signal in development.
```

THESIS: generate one successful and one failed request, then correlate them
across metric, trace, and log.

## 15. Store Telemetry and Build One Useful View

THESIS: instrumentation doesn't help if the evidence disappears with the
process — send it somewhere you can filter by environment and release.

```text
Configure collection and storage for logs, metrics, and traces.

Requirements:

- keep application instrumentation decoupled from the observability backend;
- route telemetry through the configured exporter or collector;
- secure transport and authenticated team access;
- retain enough history to compare before and after a release;
- redact or minimize sensitive fields before storage;
- document retention, cardinality, sampling, and cost controls.

Then create one operational dashboard with panels for:

- availability and error indicators by environment/release;
- latency percentiles for critical operations;
- groups created, filled, kicked off, and closed;
- join conflicts and invalid transitions;
- kickoff-confirmation rate and age;
- photo, storage, notification, and moderation failures;
- current release version.

Generate healthy and failing traffic. Confirm that a metric anomaly can lead
to a matching trace and log from the same environment, release, and time
window.
```

## 16. Alert on User Impact

THESIS: dashboards support investigation; alerts demand action. Start with
few alerts, each one a symptom someone would actually handle.

```text
Add actionable alerts for conditions representing real user impact.

Start with:

- critical workflow unavailable;
- elevated failed joins or kickoff confirmations over a meaningful interval;
- repeated invalid group or relay transitions;
- storage or upload failures;
- repeated authorization-bypass attempts.

For each alert define threshold, duration adjusted for low traffic, severity,
owner, service, environment, release labels, direct links to dashboards,
runbook, initial investigation steps, rollback guidance, escalation contact,
and expected false-positive behavior.

Suppress duplicates while acknowledged. Test every alert safely and confirm
normal traffic doesn't fire it.
```

THESIS: if nobody would know what to do when it fires, it's noise, not
alerting.

## 17. Add a Bounded Agent First Responder

THESIS: an agent can gather evidence and prepare a fix fast, but confidence
isn't authority — separate investigation from permission to change
production.

```text
Create an incident-response worker that polls the configured alert source.

When an alert fires:

1. validate and deduplicate the event;
2. collect a bounded evidence packet containing the alert, affected
   operation, environment, release, recent deployments, relevant metrics,
   traces, sanitized logs, configuration changes, health results, dashboard
   link, and prior similar incidents;
3. invoke a headless coding-agent session with the packet and the responder
   prompt below;
4. restrict the agent to read-only access to code, telemetry, and runbooks,
   plus write access only to an isolated branch and incident record;
5. save transcript, findings, proposed patch, test results, policy decision,
   actions taken, and escalation decision.

Responder prompt:

You are the first responder for Study Relay. An alert fired.

Investigate the root cause from the supplied evidence packet. Form testable
hypotheses, reproduce the failure locally where possible, and distinguish bad
code, bad configuration, bad migration, dependency failure, capacity
exhaustion, and malicious activity.

If you find a safe code correction, make the smallest change, add a
regression test, run the required checks, and commit it to an isolated
branch. Do not deploy or modify production.

If mitigation is needed, classify it as investigate, mitigate, rollback, or
escalate. Explain the evidence, impact, confidence, immediate human action,
proposed reversible runbook, verification query, and missing information.

Never expose secrets, delete evidence, disable alerts to hide failure, rotate
credentials, modify infrastructure, delete data, auto-merge patches, or
certify its own fix. Route novel, destructive, security-sensitive,
privacy-sensitive, or ambiguous actions to a human.
```

THESIS: prompts shape reasoning; sandboxes, credentials, budgets, timeouts,
and external policy are what actually enforce limits.

## 18. Rehearse Failure Before Reality Chooses the Test

THESIS: the operational loop is unproven until you deliberately break the
application and recover it.

```text
Run a game-day exercise in development.

Introduce a realistic temporary bug that causes some join or kickoff
confirmations to fail while existing unit tests still pass. Deploy it to
development.

Verify:

- the dashboard shows increased user-visible failures;
- the alert fires after the intended duration;
- the responder receives useful, sanitized evidence;
- it produces either a tested isolated patch or a clear escalation;
- external policy allows only the intended reversible action, if any;
- rollback restores the previous known-good artifact;
- health checks and the original metric query prove recovery;
- the incident record explains the timeline without exposing secrets.

Then repeat with conflicting or incomplete evidence and confirm the responder
escalates instead of guessing. Remove the injected bug and all temporary
resources when the exercise ends.
```

THESIS: fix weaknesses in alerting, evidence, permissions, policy, or
rollback — not just the bug you injected.

## 19. Audit Before Calling It Done

THESIS: review the system as an operator and as an adversary would — look
for overexposed resources, excessive privileges, untested backups, weak
input handling, undocumented manual steps.

```text
Perform a production-readiness and security audit of this repository and its
running environments.

Review:

- authentication, session handling, authorization, and abuse prevention;
- input validation, file uploads, output handling, and injection risks;
- secret storage, rotation, and accidental history exposure;
- dependency, base-artifact, and configuration vulnerabilities;
- network exposure of applications, databases, object storage, telemetry, and
  administrative tools;
- deployment, responder, moderator, and operator permissions and blast
  radius;
- backup schedule, isolation, encryption, retention, and restore testing;
- release metadata, rollback path, and incident-response evidence;
- data retention, deletion, export, and moderation obligations;
- billable resources, ownership, budget alerts, and cleanup paths.

Classify findings as blocker, high, medium, low, or observation. For each
one, cite the evidence, explain the risk and abuse or failure path, propose
the smallest remediation, and define how to verify it.

Implement blockers only after I approve the plan. Do not weaken functionality
or remove visibility to make the report look better.
```

## What Comes Next

THESIS: this is a credible minimum production loop — specify, prototype,
formalize the contract, implement, persist, package, test, deploy, promote,
observe, alert, investigate, rehearse, audit. Real products deepen that loop.

### Run on a Managed Runtime

THESIS: a single hand-deployed instance is fine for learning; production
benefits from a platform that manages restarts, placement, scaling, rollout.

```text
Evaluate managed compute options for the immutable artifact. Compare managed
application platforms, managed container/runtime services, and container
orchestration. Recommend the simplest option that meets availability,
scaling, private networking, secret handling, logging, rollback, regional,
and budget requirements. Encode the deployment and document how to migrate
away from it.
```

### Harden Data Operations

THESIS: data loss shows up at the worst possible moment; backups only count
if restore is tested.

```text
Move durable state to an appropriate managed service if needed. Add
scheduled backups, independent copies, retention rules, encryption,
integrity checks, access controls, restore permissions, and a recovery
objective.

Restore a recent backup into an isolated environment, run migrations and
smoke tests, compare critical counts, verify photos and relay links, record
recovery duration, and document how to revoke compromised data access.
```

### Reduce Public Exposure

THESIS: public should mean exactly the intended surface, nothing more.

```text
Harden network and identity boundaries.

Keep databases, object stores, queues, telemetry backends, responders, and
administrative interfaces private where possible. Require least-privileged
authenticated access, separate human/deployment/application/responder
identities, rotate credentials, restrict egress, and document ingress,
break-glass access, audit trails, and periodic access review.
```

### Scale with Evidence

THESIS: correctness under one study group is different from correctness
under a thousand.

```text
Add capacity planning.

Identify the busiest journeys and expensive queries. Create realistic load
profiles for browsing, group creation, join races, kickoff confirmation,
photo upload, moderation, and relay-link lookup. Measure throughput,
latency, errors, connection-pool behavior, storage growth, queue depth, and
saturation.

Then propose the smallest scaling, caching, indexing, timeout, retry,
backpressure, load-balancing, or autoscaling changes. Include failure modes,
capacity thresholds, and cost implications. Never run destructive load tests
against production data.
```

### Make Releases Progressive

THESIS: once the basic promotion path works, reduce the number of users
exposed to a bad release.

```text
Add progressive delivery where the platform supports it: health-gated
rollout, canary or percentage release, feature flags for risky behavior,
comparison against the current version, automatic halt on regression, and
one-command rollback. Preserve a deliberate manual promotion and rollback
path.
```

### Repeat Assurance

THESIS: security, operations, and agent capabilities drift; reviews should
recur, not happen once.

```text
Create scheduled assurance reviews for dependencies, artifacts, secrets,
identities, network exposure, backup restores, alert usefulness, telemetry
cost, unresolved findings, disaster-recovery drills, and every automation or
coding-agent capability. Record what each automated actor can read, write,
execute, spend, deploy, and approve. Require dated owners, deadlines,
evidence links, human disposition, and periodic removal of unused access.
```

THESIS: humans stay responsible for choosing the product, reviewing
contracts, approving production promotion, validating findings, and deciding
what the system may do without asking.

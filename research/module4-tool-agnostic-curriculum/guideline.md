# Guideline: initial Module 4 outline for discussion

Status: proposed outline; not approved for article writing or implementation

## Working title

**Module 4 — Operating AI-Built Software: Observability, Agent Response, and Security Audits** [PROPOSAL]

Alternative: **From Deployment to Operations: Observability, First-Line Agents, and Security Audits** [PROPOSAL]

The title should describe the system learners build and operate. Individual products belong inside implementation sections, not in the module title. [HUMAN]

## Reader and promised transformation

The reader has completed Module 2: a React frontend and FastAPI backend, Postgres, containers, public deployment, and CI/CD. [FACT current-module-4,syllabus-proposal] Module 4 takes that same application beyond “deployed” into “operable.” [HUMAN]

The reader should finish with a system that:

- emits useful metrics, logs, and traces through OpenTelemetry;
- shows application health and request behavior in Grafana;
- raises a small number of actionable alerts;
- gives a sandboxed coding agent the first opportunity to collect evidence and diagnose an incident;
- permits only narrow, pre-approved automatic remediation and otherwise escalates with a human-ready incident packet;
- runs repeatable change-level and scheduled security audits with deterministic checks and independent frontier-model review;
- preserves an audit trail across deployment, alert, diagnosis, action, verification, escalation, and security findings. [INFERENCE observability-pipeline,alerting-sre,safe-remediation,agent-security-review]

## Core claim

Deployment is not the end of the development loop. A production system must tell us when users are affected, provide evidence about why, constrain what automation may change, and preserve enough history for a human to verify every important decision. [INFERENCE alerting-sre,nist-incident-response,safe-remediation]

The module has three pillars:

```text
observe the system
respond safely to incidents
audit the code and the response system
```

## Running system

```text
Module 2 application and CI/CD
              |
      OpenTelemetry signals
              |
     OpenTelemetry Collector
      /        |        \
Prometheus    Loki      Tempo
 metrics      logs      traces
      \        |        /
             Grafana
       dashboards + alerts
                  |
         first-line agent
       /                  \
safe runbook          human escalation
       |               + evidence packet
verify recovery

Scheduled/PR security audit runs alongside this operational path.
```

[INFERENCE observability-pipeline] The collector is the stable, vendor-neutral boundary. Prometheus, Loki, Tempo, and Grafana are the concrete teaching backends, not the concepts themselves.

## Initial article/module outline

### Opening — We deployed the app; now we have to operate it

Continue directly from Module 2. The Snake Royale application is public and deploys through CI/CD, but we cannot yet answer basic operational questions:

- Is it working for users?
- Which requests are failing or slow?
- Did the last deployment cause the problem?
- What evidence should an agent inspect?
- What may the agent fix without waking a human?
- How do we know the fix actually worked?
- How do we regularly audit the code and the automation itself? [HUMAN] [PROPOSAL]

Introduce the end-to-end architecture and state that the module will deliberately break the application twice: one known, safely recoverable incident and one ambiguous incident that must be escalated.

### 4.1 — Instrument the Module 2 application with OpenTelemetry

Concepts:

- Instrumentation, collection, storage, and visualization are separate layers.
- Metrics show trends and alert conditions; logs record events; traces show a request crossing components.
- Consistent resource attributes identify service, version, environment, and instance.
- Trace IDs connect a slow or failed request to its logs.
- Telemetry can contain sensitive data, so collection, redaction, retention, authentication, and cardinality are security/cost concerns. [FACT observability-pipeline]

Core implementation scope:

- Instrument FastAPI requests, outbound/database operations where feasible, and custom game/business operations.
- Export traces and metrics through OTLP to an upstream OpenTelemetry Collector.
- Keep application logs structured on stdout and inject trace/service context so the collector can route and correlate them.
- Add deployment version/commit as a resource attribute or annotation.
- Treat React/browser tracing as an optional extension because current OpenTelemetry browser instrumentation remains experimental. [FACT observability-pipeline]

Deliverables:

```text
observability/
  collector.yaml
  compose.yaml
  README.md
docs/
  telemetry-data-flow.md
```

Teaching point: instrument once against an open protocol; choose or replace backends later.

### 4.2 — Turn telemetry into dashboards and actionable alerts

Concepts:

- Start with traffic, errors, latency, and saturation/health—the golden signals.
- Alert on sustained user-visible symptoms rather than every internal cause.
- A page/incident must imply an action; dashboards keep the diagnostic detail.
- Group, deduplicate, silence, and inhibit related alerts.
- Monitor the monitoring path with an external health check. [FACT alerting-sre]

Minimum dashboard:

- request rate;
- error rate by endpoint/status family;
- p50/p95 latency;
- current service version and recent deployment marker;
- representative traces and correlated logs;
- one saturation/health measure appropriate to the app.

Minimum alerts:

1. Public application/health endpoint unavailable for a sustained period.
2. Elevated user-visible 5xx/error rate.
3. Elevated p95 request latency.
4. Optional saturation alert.
5. Metamonitoring alert when telemetry or alert delivery stops. [INFERENCE alerting-sre]

Every alert includes severity, affected service, start time, user symptom, dashboard/trace link, recent deployment, and a runbook reference.

Deliverables:

```text
observability/
  dashboards/
  alerts.yaml
  alert-tests/
runbooks/
  availability.md
  error-rate.md
  latency.md
```

Teaching point: an alert without context, ownership, and a possible action is noise.

### 4.3 — Make a coding agent the first line of support

When an alert fires, an incident orchestrator starts Codex, Claude Code, or another compatible terminal agent in a constrained environment. The agent receives the alert, system map, read-only observability commands, deployment history, and relevant runbook. [HUMAN]

The response loop:

```text
alert
→ enrich with telemetry and recent changes
→ state observed facts
→ form and test hypotheses
→ choose safe runbook or escalate
→ execute only if policy permits
→ verify recovery
→ record the incident
```

The agent initially has read-only access. It can query metrics/logs/traces, inspect configuration and git history, and run health/diagnostic commands. [INFERENCE safe-remediation,alerting-sre]

First prepared incident: deploy a version that causes a clear error-rate regression. The evidence identifies the recent deployment; a versioned, pre-approved rollback is available; the agent invokes it and verifies the health/error-rate postcondition. [PROPOSAL]

Second prepared incident: create an ambiguous database/latency failure with incomplete or competing evidence. The agent must stop and escalate rather than guess. [PROPOSAL]

Deliverables:

```text
incident-response/
  responder-task.md
  evidence-schema.json
  incident-record.schema.json
  incidents/
```

Teaching point: the agent’s first value is fast, consistent evidence collection—not unrestricted production mutation.

### 4.4 — Decide what the agent may fix and when humans take over

Use action levels:

| Level | Capability | Policy |
| --- | --- | --- |
| 0 | Enrich alert with evidence | Automatic |
| 1 | Read-only diagnosis and recommendation | Automatic within limits |
| 2 | Execute a tested, reversible runbook | Policy-gated |
| 3 | Create a code patch/PR and run CI | Isolated branch; no auto-merge |
| 4 | Destructive, broad, secret/data, or novel production action | Human approval |

Automatic remediation requires all of:

- known failure signature;
- pre-approved and versioned runbook;
- idempotent or reversible action;
- bounded blast radius;
- no unresolved security, privacy, data-integrity, or authorization concern;
- deterministic recovery check;
- strict retry, time, command, and cost limits;
- full action logging. [INFERENCE safe-remediation]

Escalation is mandatory for unknown/ambiguous causes, high or growing impact, sensitive data/security involvement, missing telemetry or recovery test, novel/destructive actions, repeated failure, or exhausted budgets. [INFERENCE safe-remediation,alerting-sre]

The escalation packet contains facts, hypotheses, evidence links, recent changes, actions attempted, current state, remaining risk, and the recommended next human action.

Deliverables:

```text
incident-response/
  autonomy-policy.yaml
  escalation-policy.md
  runbook-allowlist.yaml
  audit.jsonl
```

Teaching point: confidence is not authorization. Policy, reversibility, blast radius, and verification determine autonomy.

### 4.5 — Run recurring AI-assisted security audits

Security review has three cadences:

1. **Every change:** tests and deterministic security checks plus a focused agent review of the diff.
2. **Scheduled or release audit:** a deeper full-repository review using two independent model families.
3. **Human review:** high-severity, disputed, business-logic, data/IAM, and audit-system findings. [INFERENCE owasp-secure-code-review,agent-security-review]

Current model examples:

- OpenAI `gpt-5.6-sol` with `max` reasoning for a quality-first review. [FACT current-audit-models]
- Anthropic `claude-fable-5` as an independent reviewer, subject to classifier refusal and 30-day retention policy. [FACT current-audit-models]
- ChatGPT for interactive, human-guided investigation of selected findings. If ChatGPT uses GPT-5.6, it is another surface over the same family, not a third independent vote. [INFERENCE current-audit-models]

The two automated reviewers receive the same versioned audit brief and repository snapshot but do not see each other’s output. Findings must include code/config evidence, impact/abuse path, uncertainty, validation method, and remediation. Agreement raises priority but is not proof. [INFERENCE agent-security-review,owasp-secure-code-review]

Deterministic scanners/tests and a human validate findings. Agents may create patch branches and regression tests, but they do not directly merge a security fix or declare their own finding resolved without independent evidence. [FACT agent-security-review] [INFERENCE owasp-secure-code-review]

Rotating audit themes:

- authentication and authorization;
- injection, unsafe commands, and file access;
- secrets and sensitive data in code/logs/telemetry;
- dependencies, containers, CI/CD, and infrastructure;
- business logic, abuse cases, race conditions, and resource limits;
- agent instructions, tools, permissions, and prompt-injection paths.

Deliverables:

```text
security-audit/
  audit-brief.md
  findings.schema.json
  baselines/
  runs/
  accepted-findings.md
```

Teaching point: multiple fluent reviewers do not replace evidence. Models propose findings; repeatable checks and humans decide.

### 4.6 — Audit the whole operating system

Tie the three pillars together. Given a code commit or incident ID, the learner should be able to reconstruct:

- who or what initiated the change/action;
- which commit and deployment were active;
- which alert fired and why;
- which telemetry and commands the agent inspected;
- which policy authorized or blocked an action;
- whether recovery was independently verified;
- whether a human was notified or approved;
- which security findings remain open. [INFERENCE nist-ai-rmf,nist-incident-response]

Final deliverable: an **Operations and Security Audit Report** containing the observability data flow, dashboards/alerts, one automatically recovered incident, one escalated incident, one recurring security audit, remediation evidence, and residual risks.

## What we should mention but not teach deeply

The article should end with a production-maturity map, clearly separating the core module from important extensions:

- formal SLIs, SLOs, error budgets, and multi-window burn-rate alerts;
- frontend real-user monitoring and synthetic browser checks;
- infrastructure/database/host monitoring and capacity planning;
- continuous profiling and eBPF-based observability;
- sampling, telemetry retention, PII redaction, tenant isolation, and observability cost control;
- progressive/canary deployments, feature flags, and automatic rollback;
- load, stress, chaos, and disaster-recovery testing;
- backups and tested restore procedures;
- on-call rotations, status communication, incident command, and blameless postmortems;
- SBOMs, provenance/signing, secret scanning, dependency/container/IaC scanning, penetration testing, and coordinated disclosure;
- model/provider evaluation, prompt/version regression tests, and audit false-positive/false-negative measurement;
- high availability for the observability and incident-response systems themselves. [INFERENCE nist-ssdf,nist-incident-response,alerting-sre,observability-pipeline]

These are not unimportant. They are excluded because implementing them would obscure the module’s main loop.

## Explicit non-goals

- Do not teach Grafana, Prometheus, Loki, or Tempo as isolated product tours.
- Do not build a general autonomous SRE agent.
- Do not give a coding agent unrestricted cloud or production credentials.
- Do not claim automatic root-cause certainty from telemetry correlation.
- Do not auto-merge model-generated security fixes.
- Do not send proprietary source or sensitive telemetry to a model without an explicit provider/retention policy.
- Do not make Kubernetes a prerequisite; the Module 2 Docker/AWS deployment is sufficient.

## Feasibility boundary for the implementation pass

The later implementation should demonstrate the complete control flow locally or in a safe staging environment. It does not need to build a production-grade incident platform. A small alert webhook/orchestrator may invoke Codex or Claude Code in headless mode, preserve structured outputs, call allowlisted scripts, and generate escalation artifacts. [PROPOSAL]

“Implement ourselves” means building this orchestration, policy, evidence, and audit layer around standard telemetry and CLI interfaces—not recreating Prometheus, a tracing backend, a security scanner, or a model API. [INFERENCE observability-pipeline,nist-ssdf]

## Decisions needed before approval

1. Is the working title and three-pillar story correct?
2. Should browser/frontend tracing be optional, or must both frontend and backend be instrumented in the core lab despite the browser SDK’s experimental status?
3. Are the two incident scenarios right: one safe rollback and one mandatory escalation?
4. Should recurring audits use both model families in the required exercise, or show one required reviewer plus an optional independent second reviewer to control cost and account requirements?
5. Is six sections realistic for the module duration, or should Sections 4.3 and 4.4 be one lesson?

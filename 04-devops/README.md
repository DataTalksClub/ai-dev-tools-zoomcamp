# Module 4 — DevOps and Observability for AI-Built Apps

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what we are preparing, but the final videos, exercises, homework, and requirements may change before the cohort starts.

## Overview

Module 3 ends with an app that deploys automatically when tests pass. That gets it online. It does not tell you whether it still works.

If an important endpoint starts returning `500`, you need to know that users are affected, find the failed requests, connect them to the deployment that caused them, and decide what to do. CI/CD ships a bad release as efficiently as a good one.

This module builds the loop that closes that gap:

```text
change
→ observe user impact
→ alert with context
→ investigate from evidence
→ authorize a bounded response or escalate
→ verify recovery
→ audit the code and the response trail
```

We also put an agent inside that loop as the first line of support. It collects the same evidence you would collect, compares it with recent changes, and proposes an action. What it does not get is general production credentials. A model supplies confidence; code outside the model enforces permission.

The concrete stack is OpenTelemetry into Prometheus, Loki, and Tempo, with Grafana on top, and a responder that runs Codex or Claude Code in headless mode. Those products are replaceable. The boundaries between evidence, reasoning, permission, and verification are the part worth learning.

Prerequisite: the deployed app from [Module 3](../03-deployment/).

The long-form version of this module is the series article [DevOps and Observability for an AI-Built App](../articles/04-devops.md).

## Lessons

### Lesson 4.1 — The Operational Gap

Goal: find out what you cannot answer about your own deployed app.

Break the app with a deliberately bad deployment, then try to answer:

```text
Are users seeing errors?
Which operation is failing?
Can I open one representative failed request?
Which log belongs to that request?
Which deployment served it?
```

Most first-time answers come from SSH and raw console logs. That is the gap the rest of the module closes.

Teaching point: a dashboard full of CPU graphs that cannot answer those five questions is not observability. Start from the incident you care about, not from the tool.

### Lesson 4.2 — Instrument One Request End to End

Goal: make the app produce evidence you can follow.

Each kind of evidence answers a different question:

- a metric tells you the error rate on score submission increased
- a trace shows the path of one failed request through the backend and the database
- a log records the exception and the values you deliberately chose to keep

Topics:

- OpenTelemetry SDK setup for the backend
- resource attributes: service name, environment, deployed git commit
- structured JSON logs with the trace ID injected
- one custom counter for the operation you care about
- what must never be recorded: passwords, tokens, request bodies, user names
- why browser instrumentation is a later step, not the first one

Instrument one important operation first, not the whole app.

Deliverables:

```text
backend instrumentation for one endpoint
a test proving instrumentation did not change the response
```

Teaching point: telemetry is also data you are storing and paying for. Decide what you keep before you turn it on.

### Lesson 4.3 — The Telemetry Pipeline

Goal: put a stable boundary between the app and wherever the data ends up.

The app sends OTLP to an OpenTelemetry Collector. The collector exports to the backends:

```text
Prometheus   metrics
Loki         logs
Tempo        traces
Grafana      reads all three
```

Topics:

- why the app should not export directly to each backend
- batching and retries outside the request path
- pivoting from a metric exemplar to a trace, and from a trace to its logs
- keeping high-cardinality values such as trace IDs out of log labels
- running the stack with Docker Compose

Deliverables:

```text
observability/
  collector.yaml
  compose.yaml
  dashboard.json
```

Teaching point: give the assistant the architecture and let it write the configuration. Asking a model to choose your observability stack produces a plausible answer to a question you should decide yourself.

### Lesson 4.4 — One Alert Worth Waking Up For

Goal: create a single alert that represents user impact and carries enough context to act.

An alert needs both conditions:

- enough requests failed to affect users
- the failure lasted long enough that one blip does not start an incident

The payload needs:

```text
affected service and environment
severity and owner
user-visible symptom
start time
dashboard link
active deployment version
runbook path
```

Topics:

- symptoms page, causes go on the dashboard
- thresholds need duration
- what Alertmanager adds in a larger setup: grouping, deduplication, silencing, inhibition
- alert fatigue, rotting rule packs, and alerts nobody can act on
- testing an alert expression

Deliverables:

```text
observability/alerts.yaml
a test for the alert expression
a note on why this is an alert and not a dashboard-only metric
```

Teaching point: do not import a large alert pack. One alert you trust beats forty you have learned to ignore.

### Lesson 4.5 — Evidence Before the Agent

Goal: collect a bounded, repeatable evidence packet before any model is involved.

The alert fires a webhook at a small responder. The responder runs allowlisted, read-only queries and writes a fixed directory:

```text
incidents/<timestamp>/
  alert.json
  health.json
  metrics.json
  traces.json
  logs.jsonl
  deployment.json
  recent-commits.txt
```

Topics:

- read-only credentials, not a scoped-sounding prompt
- known queries instead of model-invented commands against a live system
- why the webhook carries a symptom and links, never a prompt or a command
- an append-only incident record

Deliverables:

```text
incident-response/collect-evidence.sh
incident-response/evidence.schema.json
```

Teaching point: the model does not get to decide what to look at. It starts from the same packet every time, which is also what makes the incident reconstructable later.

### Lesson 4.6 — The Agent as First Responder

Goal: invoke a headless coding agent as a read-only investigator with structured output.

The adapter contract stays vendor-neutral:

```text
input:  versioned task + evidence directory + output schema
output: observed facts, hypotheses, proposed action, uncertainty
limits: working directory, read-only tools, timeout, command budget, network scope
```

The task asks for facts tied to evidence files, up to three ordered hypotheses, checks that would distinguish them, one proposed action or `ESCALATE`, and what remains unknown.

Concrete adapters:

- `codex exec` with a read-only sandbox and an output schema
- `claude -p` in plan mode with file-reading tools only and a JSON schema

Topics:

- forcing structured output and validating it
- timeouts and budgets
- what a schema catches and what it does not
- keeping the adapter stable while the CLI flags change

Deliverables:

```text
incident-response/responder-task.md
incident-response/response.schema.json
incident-response/run-agent.sh
```

Teaching point: a schema catches a missing field. It does not make the diagnosis true.

### Lesson 4.7 — Confidence Is Not Permission

Goal: put authorization outside the model.

The proposed action goes to an allowlist:

```yaml
actions:
  rollback_last_release:
    required_signature: error_rate_after_deployment
    command: runbooks/rollback.sh
    verify: runbooks/verify-recovery.sh
    max_attempts: 1
    timeout_seconds: 300
```

An action may run automatically only when all of these hold:

- the evidence matches a known failure signature
- the runbook was approved and versioned before the incident
- the action affects one bounded target
- it is reversible or safe to repeat
- no security, authorization, sensitive-data, or data-integrity question is open
- an independent check can confirm recovery
- the time and attempt budget is not exhausted

Autonomy levels:

| Level | What happens | Policy |
| --- | --- | --- |
| 0 | Alert enrichment | Automatic |
| 1 | Read-only investigation and recommendation | Automatic within limits |
| 2 | Tested, reversible, versioned runbook | Allowlisted signature only |
| 3 | Patch or PR in isolation | Human reviews, never auto-merge |
| 4 | Novel, destructive, broad, or security-related action | Human required |

Everything else escalates, with a report that states user impact, facts and their evidence, the active deployment, hypotheses already checked, what was attempted, current state, what is unknown, and the safest next action for a person.

Lab: run the same incident twice. First with evidence matching the known post-deployment signature, so the rollback runs and recovery is verified. Then remove the deployment match or add a data-integrity signal, and watch the same agent be forced to escalate.

Deliverables:

```text
incident-response/autonomy-policy.yaml
incident-response/runbooks/rollback.sh
incident-response/runbooks/verify-recovery.sh
incident-response/incidents/
```

Teaching point: the model did not get less intelligent in the second run. You changed what the policy authorized.

### Lesson 4.8 — Recurring Security Audits

Goal: find weaknesses before they become incidents, without trusting a model opinion on its own.

Three layers:

1. a deterministic scanner finds known patterns and dependency issues
2. a model reviews context, authorization, abuse paths, and business logic
3. a person validates the evidence and decides what to fix

Give the model the scanner output as evidence, not as a verdict. Require every finding to include file and line evidence, the concrete abuse path, impact and uncertainty, how a person can reproduce or disprove it, and a proposed fix with a regression test.

Topics:

- running Semgrep and keeping machine-readable output
- Semgrep MCP as one way to expose the scanner to an agent
- PR-Agent and built-in review features at the pull-request boundary
- when a second independent model family is worth it, and when it is the same family behind a different interface
- provider data handling: what source code goes where, and under which retention terms

Deliverables:

```text
security-audit/audit-brief.md
security-audit/semgrep.json
security-audit/findings.schema.json
security-audit/runs/
```

Teaching point: agreement between two models raises the priority of a finding. It does not prove it. A reproduction, a scanner result, a test, or an informed human review decides.

### Lesson 4.9 — Audit the Agent Too

Goal: treat the responder itself as attack surface.

It now has instructions, CLI adapters, filesystem access, model credentials, and possibly MCP servers. Inventory them:

```text
Capability | Source | Read | Write | Network | Secrets | Approval
-----------|--------|------|-------|---------|---------|---------
metrics    | local  | yes  | no    | local   | no      | no
logs       | local  | yes  | no    | local   | no      | no
git        | system | yes  | no    | no      | no      | no
rollback   | repo   | no   | yes   | deploy  | scoped  | policy
```

For each capability, record where it came from, which version you trust, what input it processes, and which credential enforces its limits.

Topics:

- provenance of agent extensions as a supply chain
- Snyk Agent Scan for inventorying agents, skills, and MCP servers
- the scanner's own permissions and data path, since scanning an MCP config may start server commands

Deliverables:

```text
security-audit/capability-table.md
security-audit/agent-scan-notes.md
```

Teaching point: a sentence in the prompt that says "read only" is not the same as a read-only token.

This lesson is where [Module 5](../05-agent-capabilities/) starts. Every capability you add to a coding agent there belongs in a table like this one.

## Where the Other Tools Fit

Once the problems have names, the rest of the landscape places itself:

- **HolmesGPT** and **K8sGPT** collect operational evidence a model can explain. Same design as the responder, without making Kubernetes a prerequisite for this course.
- **PR-Agent** applies model review at the pull-request boundary.
- **Semgrep MCP** connects deterministic scanning to an agent.
- **Snyk Agent Scan** inventories the agent extension supply chain.
- **LiteLLM** adds a gateway for model routing, keys, budgets, and logs when many apps or providers need one policy.
- **Ollama** runs models locally when data placement requires it.
- **garak** tests LLM applications themselves, which is not what this app is.

A local model does not automatically make the workflow private: the host, network, prompt history, local logs, endpoint authentication, and model quality all still matter. A gateway centralizes model access policy, but it does not make a weak incident process reliable.

## Non-Goals

This module deliberately does not cover:

```text
SLOs, error budgets, and burn-rate alerts
synthetic monitoring, real-user monitoring, and profiling
sampling, retention, and observability cost control
canary and progressive delivery, feature flags, chaos testing
on-call ownership, incident command, blameless postmortems
SBOMs, build provenance, signing, penetration testing
```

They are excluded because they would obscure the main loop, not because they are unimportant. The article's closing section suggests the order to add them in, starting with an SLI and SLO for your most important user journey.

## Module Deliverable: Operations and Security Report

Apply the module to your own app:

```text
observability/
  collector.yaml
  compose.yaml
  dashboard.json
  alerts.yaml

incident-response/
  collect-evidence.sh
  responder-task.md
  response.schema.json
  autonomy-policy.yaml
  runbooks/rollback.sh
  runbooks/verify-recovery.sh
  incidents/

security-audit/
  audit-brief.md
  findings.schema.json
  capability-table.md
  runs/

docs/operations-and-security-report.md
```

Given one incident ID, the report should let a reader reconstruct:

- the deployed version and the user impact
- the alert and the evidence inspected
- the model and configuration used, and the action proposed
- the policy decision and the command actually executed
- the recovery verification, or the escalation packet
- any related security finding and the human disposition

The operating principle: the model may reason; the system must observe, authorize, verify, and remember.

## Previous Cohort Materials

Related material from the previous cohort:

- [2025 archived CI/CD and DevOps module](../cohorts/2025/05-cicd-devops/)

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

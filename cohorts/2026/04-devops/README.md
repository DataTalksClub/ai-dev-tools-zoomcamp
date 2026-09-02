# Module 4 — DevOps and Observability for AI-Built Apps

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

You will:

- Find what you can't answer about a broken deployment, and see why CPU graphs alone don't count as observability
- Instrument one endpoint end to end with OpenTelemetry — metrics, traces, and structured logs — without leaking secrets
- Wire a telemetry pipeline: an OpenTelemetry Collector feeding Prometheus, Loki, and Tempo, viewed together in Grafana
- Write one alert that represents real user impact and carries enough context in its payload to act on
- Collect a bounded, repeatable evidence packet with read-only, allowlisted queries before any model gets involved
- Run a headless coding agent (Codex or Claude Code) as a read-only first responder behind a vendor-neutral, structured-output adapter
- Gate any automated action behind an allowlist and autonomy levels, so a model's confidence never substitutes for permission
- Run recurring security audits that combine a deterministic scanner (Semgrep), model review, and human validation
- Treat the responder itself as attack surface: inventory its capabilities, credentials, and provenance (Snyk Agent Scan)

Prerequisite: the deployed app from [Module 3](../03-deployment/).

[Recording: DevOps and Observability for AI-Built Apps](https://www.youtube.com/watch?v=YkxLo_FRoQw)

Module summary: The companion article makes the deployed app more production-ready by
separating dev and prod, collecting logs, metrics, and traces, and alerting on
user impact. It then runs a small proof-of-concept agent as on-call responder:
given an alert, it investigates the root cause, reproduces the failure, and
commits a fix, without the allowlists, escalation, or recovery verification a
production setup would need — the module's own lessons add those guardrails
on top.

[Read the article: DevOps and Observability for an AI-Built App](https://aishippingblog.com/p/devops-and-observability-for-an-ai)

This module is where [Module 5](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/tree/main/05-agent-capabilities) starts. Every capability you add to a coding agent there belongs in the kind of capability table you build for the responder here.

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

- [2025 archived CI/CD and DevOps module](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/tree/main/cohorts/2025/05-cicd-devops)
- [2026 homework](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/04-devops/homework.md) — questions coming

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

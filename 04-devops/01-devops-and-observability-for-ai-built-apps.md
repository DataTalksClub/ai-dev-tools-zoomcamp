---
video_url: https://www.youtube.com/watch?v=YkxLo_FRoQw
prev_url: ../03-deployment/01-test-containerize-and-deploy-an-ai-assisted-app.md
---
# DevOps and Observability for AI-Built Apps

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

We also put an agent inside that loop as the first line of support. An alert starts it automatically. It inspects a saved evidence packet and the code, then proposes an action. What it does not get is general production credentials. A model supplies confidence; code outside the model enforces permission.

The concrete stack is OpenTelemetry into Prometheus, Loki, and Tempo, with Grafana on top, and a responder that runs Codex or Claude Code in headless mode. Those products are replaceable. The boundaries between evidence, reasoning, permission, and verification are the part worth learning.

You will:

- Find what you can't answer about a broken deployment, and see why CPU graphs alone don't count as observability
- Instrument one endpoint end to end with OpenTelemetry — metrics, traces, and structured logs — without leaking secrets
- Wire a telemetry pipeline: an OpenTelemetry Collector feeding Prometheus, Loki, and Tempo, viewed together in Grafana
- Write one alert that represents real user impact and triggers a local responder
- Collect a bounded, repeatable evidence packet with read-only, allowlisted queries before any model gets involved
- Run a headless coding agent (Codex or Claude Code) from the alert, with read-only access to deployed systems and an isolated worktree for a proposed fix
- Gate deployment behind allowlisted changes, a regression test, and passing CI; escalate when those checks fail
- Run recurring security audits that combine a deterministic scanner (Semgrep), model review, and human validation
- Treat the responder itself as attack surface: inventory its capabilities, credentials, and provenance (Snyk Agent Scan)

For the homework, use the standalone [Order Tracker starter](https://github.com/alexeygrigorev/order-tracker). You can also apply the exercise to the app you deployed in [Module 3](../03-deployment/01-test-containerize-and-deploy-an-ai-assisted-app.md).

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

Apply the module to Order Tracker or your own app:

```text
observability/
  collector.yaml
  compose.yaml
  dashboard.json
  alerts.yaml

incident-response/
  collect-evidence.sh
  test-incident.sh
  responder-task.md
  response.schema.json
  autonomy-policy.yaml
  runbooks/deploy-fix.sh
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

## Community Notes

Did you take notes? You can share them here.

- Add a link to your notes above this line

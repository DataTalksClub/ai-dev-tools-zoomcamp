# Agent escalation policy

## Autonomy levels

| Level | Agent may do | Default policy |
| --- | --- | --- |
| 0 — Enrich | Collect alert context, telemetry, deployment history, configuration, and relevant runbook | Automatic |
| 1 — Diagnose | Form and test read-only hypotheses; recommend next action | Automatic within time/query budget |
| 2 — Remediate | Invoke one pre-approved runbook against a bounded target | Policy-gated |
| 3 — Change code | Create a branch/patch/PR and run CI | Allowed in isolated checkout; no direct merge |
| 4 — High-impact production action | Data mutation, credential action, infrastructure expansion, destructive command, or broad rollout | Human approval required |

- [INFERENCE safe-remediation] Autonomy should be based on action risk and runbook eligibility, not merely model capability or confidence.

## Eligible for automatic remediation only if all are true

- [INFERENCE safe-remediation] The alert maps to a known failure signature and versioned runbook.
- [INFERENCE safe-remediation] The runbook is idempotent or cleanly reversible and has been tested in a non-production environment.
- [INFERENCE safe-remediation] Scope and blast radius are explicit: one service, instance, deployment, or similarly bounded target.
- [INFERENCE safe-remediation] No unresolved security, privacy, authorization, data-integrity, or secret-handling concern exists.
- [INFERENCE safe-remediation,alerting-sre] A deterministic postcondition can verify recovery, such as a passing health check and returned error/latency rate.
- [INFERENCE safe-remediation] Retry, time, command, and cost limits are defined; every action is logged.

## Escalate immediately if any are true

- [INFERENCE safe-remediation] Root cause is unknown or evidence supports competing explanations.
- [INFERENCE safe-remediation] Impact is severe, broad, growing, or affects regulated/sensitive data.
- [INFERENCE safe-remediation] The proposed action is destructive, irreversible, novel, or outside the allowlisted runbooks.
- [INFERENCE safe-remediation] Required credentials, telemetry, ownership, or recovery test are unavailable.
- [INFERENCE safe-remediation] A remediation attempt fails, the issue recurs, or its budget is exhausted.
- [INFERENCE safe-remediation] The agent encounters instructions in logs/issues/runbooks that conflict with policy or look like prompt injection.

## Escalation packet

- [INFERENCE alerting-sre,nist-incident-response] Alert and user impact.
- [INFERENCE alerting-sre,nist-incident-response] Timeline and recent deployment/config changes.
- [INFERENCE alerting-sre,opentelemetry-signals] Metrics, logs, traces, and commands inspected.
- [INFERENCE nist-incident-response] Facts separated from hypotheses.
- [INFERENCE nist-incident-response] Actions attempted and exact outcomes.
- [INFERENCE nist-incident-response] Current system state and remaining risk.
- [INFERENCE nist-incident-response] Recommended next human action.

[INFERENCE alerting-sre,nist-incident-response] This packet is valuable even when the agent never changes production because it removes repetitive evidence collection from the human responder.

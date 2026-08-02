# Synthesis

## Current thesis

- [HUMAN] Module 4 should extend the Module 2 application rather than survey security/DevOps tools.
- [INFERENCE observability-pipeline,alerting-sre,safe-remediation] The module’s durable story is: observe the deployed system, turn user-impact symptoms into actionable alerts, let a constrained agent perform first-line triage, permit only bounded runbook remediation, and escalate everything else with evidence.
- [INFERENCE owasp-secure-code-review,agent-security-review,current-audit-models] Recurring security audit is a parallel feedback loop: deterministic checks plus independent model review propose findings; reproducible evidence and humans determine validity and remediation.
- [INFERENCE nist-ai-rmf,nist-incident-response] One audit trail should connect code, deployment, telemetry, alert, agent actions, approval/escalation, recovery verification, and security findings.

## Recommended scope

1. Instrument FastAPI with stable OpenTelemetry traces and metrics; correlate structured stdout logs. Keep browser tracing optional because its current OpenTelemetry support is experimental. [FACT observability-pipeline]
2. Use an upstream OpenTelemetry Collector and a local/staging Prometheus–Loki–Tempo–Grafana stack to make the signals inspectable and replaceable. [INFERENCE observability-pipeline]
3. Build one dashboard around traffic, errors, latency, health/saturation, version, and correlated traces/logs. [FACT alerting-sre,observability-pipeline]
4. Create three core symptom alerts plus metamonitoring, with alert context and runbook links. [INFERENCE alerting-sre]
5. Demonstrate one known deployment regression that an agent may roll back and one ambiguous incident it must escalate. [INFERENCE safe-remediation]
6. Run one recurring audit workflow with deterministic evidence and two independent model families, then validate a known fixture and record false-positive disposition. [INFERENCE agent-security-review,current-audit-models]

## Autonomy conclusion

- [FACT safe-remediation] Safe automation practice emphasizes idempotence/reversibility, tested runbooks, scoped permissions, supervision, recovery checks, and containment.
- [INFERENCE safe-remediation] There is no meaningful universal “agent confidence” threshold for production action. Confidence can rank hypotheses; deterministic policy authorizes actions.
- [INFERENCE safe-remediation] The course’s eligibility rule should be conjunctive: known signature, allowlisted runbook, bounded target, reversible/idempotent action, no protected-data/security ambiguity, deterministic postcondition, and strict budgets.
- [INFERENCE safe-remediation] Code fixes belong on a branch/PR through CI; only narrow operational runbooks such as rollback to a known-good version should be eligible for automatic production-like execution.

## Model conclusion

- [FACT current-audit-models] The accurate OpenAI configuration is `gpt-5.6-sol` with `max` reasoning effort.
- [FACT current-audit-models] Claude Fable 5 is current and suitable for demanding reasoning, but classifiers and 30-day retention affect security-audit design.
- [INFERENCE current-audit-models] ChatGPT is best presented as the human-guided audit surface, while scheduled automation uses terminal agents or APIs. It should not be counted as an independent third reviewer when backed by the same GPT-5.6 family.
- [INFERENCE agent-security-review] Cross-model agreement improves prioritization but cannot substitute for a reproduction, deterministic check, regression test, or informed human review.

## Important exclusions

- [INFERENCE alerting-sre] Full SLO/error-budget programs, on-call organization, and incident command are beyond the core lab.
- [INFERENCE observability-pipeline] Browser RUM, profiling, and production-scale telemetry security/cost engineering are follow-on topics.
- [INFERENCE nist-incident-response,nist-ssdf] Disaster recovery, chaos/load testing, full software supply-chain security, penetration testing, and coordinated disclosure should be named on the maturity map but not implemented here.

## Remaining editorial choices

- [OPEN] Require or merely recommend the second model reviewer.
- [OPEN] Decide whether browser tracing is worth its experimental complexity.
- [OPEN] Confirm whether the safe rollback occurs in staging/local simulation or against the live Module 2 deployment.
- [OPEN] Confirm module duration and whether responder workflow plus escalation policy should be one lesson.

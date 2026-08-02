# Synthesis

## Current thesis

- [HUMAN] Module 4 should extend the Module 2 application rather than survey security/DevOps tools.
- [INFERENCE observability-pipeline,alerting-sre,safe-remediation] The module’s durable story is: observe the deployed system, turn user-impact symptoms into actionable alerts, let a constrained agent perform first-line triage, permit only bounded runbook remediation, and escalate everything else with evidence.
- [INFERENCE owasp-secure-code-review,agent-security-review,current-audit-models] Recurring security audit is a parallel feedback loop: deterministic checks plus independent model review propose findings; reproducible evidence and humans determine validity and remediation.
- [INFERENCE nist-ai-rmf,nist-incident-response] One audit trail should connect code, deployment, telemetry, alert, agent actions, approval/escalation, recovery verification, and security findings.

## Recommended scope

1. [HUMAN] Fit a complete core story into 90 minutes, with an optional 30-minute extension.
2. Instrument one important FastAPI request with stable OpenTelemetry traces and metrics; correlate structured stdout logs. Keep browser tracing optional because its current OpenTelemetry support is experimental. [FACT observability-pipeline]
3. Use a prepared Collector and Prometheus–Loki–Tempo–Grafana environment so learners spend time interpreting one request rather than installing infrastructure. [INFERENCE observability-pipeline,practitioner-observability]
4. Create one sustained user-impact alert with the context and runbook needed by a first responder. [INFERENCE alerting-sre,practitioner-observability]
5. Demonstrate one deployment regression. Permit an external policy to run a known rollback, then alter one fact to force escalation without building a second incident. [INFERENCE safe-remediation,practitioner-ai-operations]
6. Run one deterministic scanner plus one model reviewer in the live exercise, validate one finding, and describe the second independent model as the scheduled/deeper audit. [INFERENCE agent-security-review,current-audit-models,practitioner-ai-security]
7. Use the optional extension for an ambiguous escalation and a capability audit of the responder itself. [INFERENCE mcp-security,practitioner-ai-security]

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
- [INFERENCE problem-first-tool-landscape] K8sGPT, LiteLLM, Ollama, and garak do not solve a problem essential to the core Module 2 operating loop and should remain examples or extensions.

## Practitioner evidence

- [FACT practitioner-observability] Alert fatigue discussions emphasize user impact, actionability, runbooks, ownership, and pruning noisy rules; merely owning dashboards does not guarantee teams use them.
- [FACT practitioner-ai-operations] Operators describe useful evidence collection and summarization, but unreliable root-cause conclusions when system context is missing and strong hesitation around write access.
- [FACT practitioner-ai-security] Security practitioners disagree on model-review quality and report false positives/misses, reinforcing layered scanners, independent review, and human disposition.
- [FACT practitioner-model-infrastructure] Gateway and local-inference discussions expose real governance/data-placement concerns, but also additional identity, logging, endpoint, capacity, and maintenance problems.
- [INFERENCE practitioner-observability,practitioner-ai-operations,practitioner-ai-security] These anecdotes sharpen the workshop problems but do not establish industry prevalence or product efficacy.

## Remaining editorial choices

- [OPEN] Confirm the working title.
- [OPEN] Confirm the bad-deployment rollback as the prepared bounded remediation.
- [OPEN] Choose whether the optional 30 minutes prioritizes ambiguous escalation plus capability audit or a second independent model audit.
- [OPEN] Decide whether to ship two terminal-agent adapters or one reference adapter plus documented commands for the other.

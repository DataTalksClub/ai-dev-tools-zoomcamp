# Safe operations automation and human escalation guidance

Primary locators:

- [FACT safe-remediation] https://sre.google/sre-book/automation-at-google/
- [FACT safe-remediation] https://sre.google/sre-book/service-best-practices/
- [FACT safe-remediation] https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-economics/feedback.html
- [FACT safe-remediation] https://www.anthropic.com/engineering/how-we-contain-claude

Summary: Safe automation depends more on bounded capability, tested recovery, and action economics than on an agent's self-reported confidence.

- [FACT safe-remediation] Google SRE describes automation as a force multiplier rather than a panacea and emphasizes judicious application.
- [FACT safe-remediation] Common fixes become safer when they are idempotent, dependency-aware, peer reviewed, permission scoped, and repeatedly testable.
- [FACT safe-remediation] Production changes should be progressively rolled out, monitored, and rolled back before diagnosis when unexpected behavior occurs.
- [FACT safe-remediation] AWS recommends human involvement when the cost of failure exceeds the cost of human review.
- [FACT safe-remediation] Anthropic argues that repeated permission prompts create approval fatigue and that containment limits blast radius more reliably than probabilistic supervision alone.
- [INFERENCE safe-remediation] An incident is eligible for automatic remediation only when it matches a known condition with a pre-approved, reversible/idempotent runbook, bounded target, no protected-data or security ambiguity, and an independent success check.
- [INFERENCE safe-remediation,alerting-sre] Unknown cause, conflicting evidence, high/broad impact, data integrity or security implications, missing recovery check, failed retry, or exceeded time/action budget should force escalation.

Limitations: No universal confidence threshold exists. Eligibility should be deterministic policy plus evidence; model confidence may help rank hypotheses but should not authorize production mutation.

Related: [agent escalation policy](../concepts/agent-escalation-policy.md)

Accessed: 2026-08-02. Publication dates vary.

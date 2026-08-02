# Assessment model

- [INFERENCE nist-ssdf,current-module-4,syllabus-proposal] Grade demonstrated outcomes and evidence quality, not product installation.

## Proposed artifact set

```text
security/
  risk-and-trust-model.md
  change-assurance.md
  findings.json
  remediation.md
  capability-inventory.md

ops/
  evidence-bundle/
  investigation.md
  recovery-verification.md

governance/
  ai-usage-policy.md
  data-flow.md
  audit.jsonl

docs/
  hardening-report.md
```

## Proposed rubric dimensions

1. **Scope and risk:** important assets, trust boundaries, actors, data, privileges, and residual risks are explicit.
2. **Evidence quality:** findings and diagnoses cite reproducible evidence and separate observation from inference.
3. **Triage and judgment:** false positives, uncertainty, impact, priority, and decision rationale are recorded.
4. **Control design:** least privilege, untrusted-input handling, sandboxing, policy, and approval gates match risk.
5. **Remediation and verification:** at least one issue is fixed and independently rechecked; recovery criteria are demonstrated.
6. **Portability and auditability:** workflows have explicit inputs/outputs and can be rerun with another compliant CLI agent.

- [INFERENCE current-module-4] Named products may earn no rubric points by themselves; they matter only through the evidence or control they provide.

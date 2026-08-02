# Concept architecture

## One loop, six applications

- [INFERENCE current-module-4,syllabus-proposal,nist-ssdf] The common learning loop is:

```text
scope -> collect -> analyze -> propose -> approve -> act -> verify -> record
```

- [INFERENCE owasp-prompt-injection,mcp-security] Inputs may be incomplete, malicious, stale, or sensitive; privileges and destinations must be explicit before collection or action.
- [INFERENCE owasp-secure-code-review,opentelemetry-signals] Analysis may combine deterministic checks and probabilistic reasoning, but the resulting claim must point back to inspectable evidence.
- [INFERENCE nist-ai-rmf,nist-incident-response] Approval, action ownership, validation criteria, residual risk, and learning must be recorded.

## Six concept areas

1. **Trust and risk boundaries** — assets, actors, data, dependencies, privileges, trust zones, failure modes, approval levels, and residual risk.
2. **Change assurance** — intent-aware, risk-based review of code/config/dependency/infrastructure changes.
3. **Security evidence pipelines** — reproducible checks, structured findings, triage, remediation, and rerun.
4. **Agent and toolchain security** — provenance and permissions for instructions, tools, skills, hooks, plugins, servers, commands, and models.
5. **Operational investigation** — signals, timeline, changes, hypotheses, discriminating tests, recovery validation, and prevention.
6. **AI usage governance** — policy for identities, data classes, providers/models, secrets, cost, retention, audit, and human oversight.

## Cross-cutting distinctions

- [INFERENCE current-module-4,tool-repositories] **Observation vs explanation:** a scanner result, log line, metric, trace, diff, or command output is evidence; an LLM summary is an interpretation.
- [INFERENCE mcp-security,nist-ai-rmf] **Advisory vs action:** reading and proposing differ from editing, commenting, merging, deploying, deleting, or changing production state.
- [INFERENCE current-module-4,tool-repositories] **Capability vs product:** “review a change” is a capability; PR-Agent is one implementation.
- [INFERENCE owasp-prompt-injection,mcp-security] **Control vs instruction:** a request in a prompt is guidance; sandboxing, permissions, policy checks, and approval gates are enforceable controls.
- [INFERENCE owasp-secure-code-review] **Finding vs decision:** a detected pattern is not automatically exploitable, relevant, accepted, or fixed.
- [INFERENCE current-module-4,tool-repositories] **Local vs private:** local/open-source execution does not alone settle which dependencies, model endpoints, logs, or telemetry receive data.

Related: [portable execution model](portable-execution-model.md), [assessment model](assessment-model.md)

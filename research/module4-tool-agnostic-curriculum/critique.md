# Critique

## Reflection

- The revised outline has one end-to-end operational story and fits a 90-minute core on paper: 10 + 20 + 15 + 25 + 17 + 3 minutes.
- Product names no longer determine the sequence. Every original tool is mapped to a problem, a durable pattern, a DIY demonstration, and a core/extension/exclusion decision.
- The live observability work answers an incident question. It does not equate installed dashboards with useful observability.
- One carefully designed 5xx alert replaces the earlier multi-alert build. This matches both primary alerting guidance and practitioner reports about alert fatigue.
- The first-line agent is portable across Codex, Claude, or another headless CLI through a small adapter contract.
- Authorization is enforced outside the model by credentials, sandboxing, an exact runbook allowlist, and deterministic verification. The outline does not mistake a prompt or confidence score for a security boundary.
- One prepared incident demonstrates both branches by changing the policy/evidence conditions. This preserves the lesson about escalation without spending time constructing a second system failure.
- The live security audit requires one deterministic scan and one model reviewer. A second model family remains the recommended scheduled audit, avoiding a two-account prerequisite in the 90-minute session.
- Reddit/social material is explicitly labeled anecdotal and promotional risk is recorded. Primary sources remain authoritative for architecture and controls.
- Current model identities are verified: `gpt-5.6-sol` plus `max` effort, Claude Fable 5 with retention/refusal considerations, and ChatGPT as a surface rather than an independent vote when backed by the same family.

## Feasibility risks

- Twenty minutes is enough to inspect and modify focused instrumentation, not to build and debug the full observability stack. Starter configuration and downloaded images must be prepared.
- Twenty-five minutes for the responder requires a small, deterministic orchestrator and prepared evidence adapters. A generic autonomous agent platform would exceed the time box.
- A live cloud rollback introduces credential, cost, latency, and safety variance. The default implementation should use local or staging deployment semantics while preserving the same policy boundary.
- Security scanner installation and two model calls can be slow. Cache dependencies and provide fixture output as a fallback.
- The final three-minute audit-trail reconstruction needs a prebuilt incident record view or concise command, not a new reporting exercise.

## Subjective decisions

- [INFERENCE current-module-4] Use an action-led series title: “Operate an AI-Built App with Observability, Agents, and Security Audits”.
- [INFERENCE safe-remediation] Use the bad-deployment rollback as the prepared safe action.
- [INFERENCE safe-remediation,mcp-security] Use ambiguous escalation plus a capability audit for the optional extension.
- [INFERENCE current-audit-models] Present one portable adapter contract with concrete Codex and Claude headless commands.
- [HUMAN] The user's instruction to finish the research and create the write-up approves the writing pass.

## Accepted risks

- [HUMAN] The article explains a concrete DIY design but does not claim that the full observability and response stack has been implemented in this repository.
- [HUMAN] Product and model details are current as of August 2026 and may need a pre-publication refresh.

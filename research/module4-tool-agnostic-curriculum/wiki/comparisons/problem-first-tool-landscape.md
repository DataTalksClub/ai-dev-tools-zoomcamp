# Problem-first tool landscape

This comparison translates the original tool list into durable learning goals. Product names are examples after the concept, never the organizing structure. [HUMAN]

| Tool or stack | Problem it exposes | Durable solution pattern | Quick DIY demonstration | Core decision |
| --- | --- | --- | --- | --- |
| OpenTelemetry + Collector | Application evidence is inconsistent and coupled to one backend | Standard signal semantics, stable resource identity, correlation, and a collection boundary | Instrument one FastAPI request and export OTLP through a collector | Core implementation |
| Prometheus + Alertmanager | Teams either miss user-impacting failures or drown in noisy conditions | Symptom-based thresholds, duration, routing, grouping, ownership, and runbook context | One 5xx regression rule delivered as a structured webhook | Core implementation |
| Grafana + Loki + Tempo | Metrics, logs, traces, and deploy history live in separate places | Pivot from symptom to exemplar trace to correlated log and recent change | Follow one failed request across dashboard, trace, and log | Core implementation, mostly prebuilt |
| HolmesGPT | Incident evidence is slow to collect across operational sources | Read-only evidence adapters, hypothesis testing, and an inspectable investigation record | A small script collects health, metrics, logs, and git/deploy context before invoking any terminal agent | Mention after DIY pattern |
| K8sGPT | Kubernetes state and events are hard to interpret | Deterministic analyzers first, model explanation second | Show a structured evidence bundle pattern; do not require Kubernetes | Exclude from core; extension example |
| PR-Agent | Reviewers lack time and change context is scattered | Versioned review brief, diff evidence, risk focus, and human disposition | Give a generic headless agent the diff, acceptance criteria, and test results; require structured findings | Fold into security audit, not a separate lesson |
| Semgrep MCP | Fluent model review can miss known code patterns or invent findings | Deterministic scanner evidence composed with model reasoning | Run a scanner CLI, preserve JSON, ask the agent to explain and validate one result | Core pattern; MCP optional |
| Snyk Agent Scan | Agents, skills, and MCP servers expand the software supply chain and authority surface | Capability bill of materials, provenance, scopes, static inspection, sandboxing, and gates | Inventory configured capabilities and classify read/write/network/secrets scope | Optional 2-hour exercise |
| LiteLLM | Multiple model providers create inconsistent auth, budget, routing, and logs | A policy-enforcing model gateway and provider-neutral request envelope | Use one tiny adapter interface and record model/config/cost metadata | Extension only |
| Ollama | Some evidence cannot be sent to a hosted provider | Explicit data placement and locally governed inference | Swap the adapter endpoint while keeping the audit brief/schema unchanged | Extension only; local is not automatically safe |
| Stakpak and similar DevOps agents | Teams want an integrated operational agent | Combine evidence adapters, policy, execution, verification, and audit trail | The workshop builds this small control loop itself | Mention as packaged alternatives |
| garak and LLM red-team tools | An LLM application may itself be vulnerable or unreliable | Adversarial evaluation of model behavior and integrations | None in this module; the Module 2 app is not an LLM product | Out of scope |

## Cross-tool conclusions

1. [INFERENCE tool-repositories,practitioner-ai-operations] K8sGPT and HolmesGPT are not two unrelated products to memorize. They sit on a spectrum from deterministic diagnosis plus explanation to agentic cross-source investigation.
2. [INFERENCE tool-repositories,practitioner-ai-security] PR-Agent, Semgrep MCP, and Agent Scan address three different layers: change reasoning, deterministic code evidence, and the agent extension supply chain.
3. [INFERENCE practitioner-model-infrastructure] LiteLLM and Ollama change where and how model calls run; neither improves the incident or audit method by itself.
4. [INFERENCE practitioner-observability] Installing the observability stack is necessary plumbing, but the learning outcome is answering an incident question with correlated evidence.
5. [INFERENCE safe-remediation,mcp-security,practitioner-ai-operations] The same external policy must constrain Codex, Claude, or any other headless terminal agent. Prompt wording is guidance, not an authorization boundary.

## Recommended workshop story

```text
real user-facing regression
→ one actionable alert
→ correlated evidence packet
→ agent investigates read-only
→ external policy permits rollback or requires escalation
→ recovery is verified
→ recurring audit searches for the class of weakness that allowed the regression
```

[PROPOSAL] This single arc demonstrates the important concepts while giving every original tool a clear conceptual home or an explicit reason for exclusion.

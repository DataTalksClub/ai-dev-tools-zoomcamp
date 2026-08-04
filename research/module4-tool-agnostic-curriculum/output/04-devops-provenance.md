# Provenance report: `04-devops.md`

Private writing record. This file is not part of the published article.

## Claim map

| Article claim | Evidence | Certainty in article |
| --- | --- | --- |
| The Module 2 app uses React, FastAPI, Postgres, containers, public deployment, and CI/CD | [FACT current-module-4,syllabus-proposal] and `articles/02-end-to-end.md` | Direct |
| OpenTelemetry provides vendor-neutral traces, metrics, logs, and a collector boundary | [FACT opentelemetry-signals,observability-pipeline] | Direct |
| Python backend traces/metrics are the stable core; browser instrumentation remains experimental | [FACT observability-pipeline] | Direct and linked to current OTel docs |
| Prometheus alerts should be few, sustained, symptom-based, and actionable | [FACT alerting-sre] | Direct and linked to Prometheus guidance |
| Alertmanager groups, deduplicates, routes, silences, and inhibits alerts | [FACT alerting-sre] | Direct and linked to current docs |
| Practitioners report alert fatigue, unused dashboards, missing runbooks, incomplete context, and reluctance to grant agent write access | [FACT practitioner-observability,practitioner-ai-operations] | Explicitly framed as practitioner discussion, not prevalence |
| Automatic remediation should require a known signature, allowlisted reversible/idempotent action, bounded target, no security/data ambiguity, and independent verification | [INFERENCE safe-remediation,alerting-sre] | Presented as the article's policy design, not a universal standard |
| HolmesGPT connects agents to observability evidence; K8sGPT runs analyzers and can add model explanations | [FACT tool-repositories] | Direct and linked to official repos |
| `codex exec` supports read-only non-interactive runs and JSON Schema output | Fresh Codex manual plus local `codex-cli 0.146.0 --help` | Direct; command verified against installed CLI flags |
| `claude -p` supports plan permissions, tool restriction, JSON output, and JSON Schema; the adapter must extract `structured_output` from its metadata envelope | Official Claude CLI docs plus a local Claude Code 2.1.220 smoke test on 2026-08-02 | Direct; full command and response structure verified locally |
| Deterministic scanner evidence should be combined with model reasoning and human validation | [FACT owasp-secure-code-review,agent-security-review] and [INFERENCE practitioner-ai-security] | Direct recommendation with product examples |
| Current OpenAI quality-first example is `gpt-5.6-sol`; `max` is reasoning effort rather than a separate model | [FACT current-audit-models] and current OpenAI model guidance checked 2026-08-02 | Direct and dated |
| Claude Fable 5 requires 30-day retention and has cyber safeguards that can reroute/block requests | [FACT current-audit-models] and current Anthropic Fable pages checked 2026-08-02 | Direct and dated |
| ChatGPT is not an independent vote when backed by the same GPT family | [INFERENCE current-audit-models] | Clearly explained as model-family independence |
| Agent Scan may start configured MCP commands and remote analysis sends component information to a provider | [FACT tool-repositories] | Direct, with cautious wording and official repo link |
| LiteLLM is a gateway; Ollama provides local inference; garak targets LLM-application evaluation | [FACT tool-repositories] | Brief classification only |
| After the workshop, prioritize user-journey reliability, safer delivery, broader security evidence, and agent governance in that order | [INFERENCE alerting-sre,nist-ssdf,nist-incident-response,safe-remediation,mcp-security] | Presented as the author's recommended sequence, not a universal maturity model |

## Time-sensitive statements

Refresh these before publication or recording:

- OpenTelemetry language signal maturity and browser status.
- Codex and Claude CLI flags.
- The JSON Schema subset shared by Codex and Claude, including Claude's handling of the optional `$schema` declaration.
- GPT-5.6 model IDs and supported reasoning effort.
- Claude Fable 5 availability, safeguards, and retention.
- Agent Scan execution/data behavior.
- Repository ownership, licensing, and current feature scope for named tools.

## Certainty audit

- The article does not claim that practitioners' Reddit reports establish adoption rates or product accuracy.
- The article does not claim that model agreement proves a vulnerability.
- The article does not claim certain automated root-cause analysis.
- The article does not claim that the example stack or responder has been implemented in this repository.
- The article labels the 90-minute sequence as the author's proposed teaching plan.
- The article labels the post-workshop sequence as the author's recommendation.

## Material deviations from the approved guideline

- None. The article keeps the single prepared regression, one actionable alert, read-only investigation, externally authorized rollback/escalation, one live scanner/model audit, and optional capability-audit extension.

# Tool-to-concept map

| Current lesson/tool | Durable concept | Minimal portable implementation | Product remains useful as |
| --- | --- | --- | --- |
| Production risk model | Trust boundaries and risk decisions | Markdown data-flow/permission/threat table | A scanner or diagram aid |
| PR-Agent | Change assurance | Agent reviews diff + intent + threat notes + check output into a standard template | Turnkey PR integration |
| Semgrep MCP | Security evidence pipeline | Run standard scanners/tests via CLI; save structured findings; agent triages; rerun after fix | Strong deterministic SAST adapter |
| Snyk Agent Scan | Agent/toolchain security | Inventory instructions/tools/packages/permissions; inspect provenance and suspicious content in a sandbox | Specialized discovery and agent-risk checks |
| K8sGPT | Evidence-grounded diagnosis | Collect runtime state/logs/events; agent forms hypotheses; verify via direct commands/health checks | Kubernetes-specific collector/analyzer |
| HolmesGPT | Incident investigation | Prepared signals + change timeline + runbook; agent correlates and tests hypotheses | Broad live-observability integration |
| LiteLLM | AI usage governance | Policy file + scoped credentials + wrapper + audit events | Full model gateway/enforcement plane |
| Ollama | Data-placement/model choice | Route an allowed task to a local endpoint and trace its data path | Local model serving adapter |

- [INFERENCE current-module-4,tool-repositories] This mapping preserves every intended learning area while removing product configuration from the definition of success.
- [INFERENCE tool-repositories] Products should be shown after the baseline workflow so learners can see what convenience, scale, coverage, or integration each one adds.

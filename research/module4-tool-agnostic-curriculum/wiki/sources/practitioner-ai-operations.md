# Practitioner discussions: AI-assisted operations

Sources:

- [FACT practitioner-ai-operations] [Anyone using AI for actual SRE/oncall operations?](https://www.reddit.com/r/sre/comments/1t6wqux/anyone_using_ai_for_actual_sreoncall_operations/), r/sre, accessed 2026-08-02.
- [FACT practitioner-ai-operations] [Integrating AI for DevOps and Best Practices you've found???](https://www.reddit.com/r/devops/comments/1rijpmf/integrating_ai_for_devops_and_best_practices/), r/devops, accessed 2026-08-02.
- [FACT practitioner-ai-operations] [AI SRE tools in 2026](https://www.reddit.com/r/sre/comments/1u232k6/ai_sre_tools_in_2026_updated_list_what_i_actually/), r/sre, accessed 2026-08-02.
- [FACT practitioner-ai-operations] Additional Kubernetes discussions found by searching for K8sGPT production experience and safe agent access.

Summary: Practitioners report value in evidence collection, correlation, summarization, runbook retrieval, and draft postmortems. Trust falls sharply when an agent can change production state.

## Claims

- [FACT practitioner-ai-operations] Participants reported that agents can query multiple data sources and find correlations quickly, but did not reliably identify root cause when system context, naming, ownership, or documentation was incomplete.
- [FACT practitioner-ai-operations] Reported useful tasks included first-triage evidence gathering, natural-language telemetry queries, runbook retrieval when runbooks exist, incident timelines, postmortem drafts, and proposed commands that a human approves.
- [FACT practitioner-ai-operations] Reported failure modes included following the loudest rather than most important signal, surface-level Kubernetes explanations, timeouts, missing organization context, and fear of remediation blast radius.
- [FACT practitioner-ai-operations] A strong theme was read access plus inspectable proposals, with a per-action human checkpoint before writes. Some participants saw narrow actions such as certificate rotation or scaling as earlier candidates for bounded automation than open-ended repair.
- [FACT practitioner-ai-operations] A Kubernetes discussion criticized using regular expressions to restrict commands and recommended enforcing the boundary with Kubernetes RBAC and limited credentials instead. This illustrates that prompts and string filters are not authorization controls.

## Teaching consequence

[INFERENCE practitioner-ai-operations,safe-remediation] The DIY exercise should implement an evidence packet and a policy boundary, not promise automatic root-cause analysis. The agent may recommend any action, but only an external allowlist and least-privilege credential can authorize a write.

## Limitations

These are unverified personal reports. Several threads contain vendor authors and promotional replies. The research uses them to identify practical friction and adoption boundaries, while primary SRE and security guidance supports the actual policy.

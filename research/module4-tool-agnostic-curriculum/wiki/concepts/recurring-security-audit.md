# Recurring security audit

## Three audit depths

1. **Every change:** deterministic tests/scanners plus a focused agent review of the diff and affected trust boundaries.
2. **Scheduled repository audit:** weekly or release-time deep review of selected security themes across the full repository, history, dependencies, deployment configuration, and prior findings.
3. **Human-led audit:** periodic review of authentication/authorization, business logic, data flows, infrastructure/IAM, high-severity or disputed findings, and audit effectiveness. [INFERENCE owasp-secure-code-review,agent-security-review]

## Proposed multi-model workflow

```text
versioned audit brief + repository snapshot + deterministic findings
                    /                              \
        GPT-5.6 Sol (max)                  Claude Fable 5
             independent structured findings
                    \                              /
                normalize + deduplicate + validate
                              |
                 human triage / issue / patch PR
                              |
                    regression evidence + tracking
```

- [FACT current-audit-models] `gpt-5.6-sol` with `max` reasoning is the accurate OpenAI configuration name; ChatGPT is an interactive surface, not a separate independent model when it uses GPT-5.6.
- [FACT current-audit-models] Claude Fable 5 is a valid current Anthropic model but introduces classifier refusal and 30-day retention considerations.
- [INFERENCE agent-security-review] Reviewers should run independently before seeing each other's findings to reduce anchoring; agreement raises priority but does not prove a vulnerability.
- [INFERENCE owasp-secure-code-review,agent-security-review] Each accepted finding needs location/evidence, vulnerable behavior or abuse path, impact, confidence/uncertainty, a suggested reproduction or test, and remediation guidance.
- [INFERENCE agent-security-review] Agents may propose patches on branches, but a model should not both originate a high-severity finding and be the only validator of its fix.

## Audit themes to rotate

- [INFERENCE owasp-secure-code-review] Authentication and authorization.
- [INFERENCE owasp-secure-code-review] Input handling, injection, unsafe commands, and file access.
- [INFERENCE owasp-secure-code-review,observability-pipeline] Secrets and sensitive-data exposure, including logs/telemetry.
- [INFERENCE nist-ssdf,owasp-secure-code-review] Dependencies, container, CI/CD, and infrastructure configuration.
- [INFERENCE owasp-secure-code-review] Business logic, race conditions, abuse cases, and resource limits.
- [INFERENCE owasp-prompt-injection,mcp-security] Agent instructions, tools, permissions, and prompt-injection paths.

## Audit record

Record repository commit, audit brief version, model IDs/configurations, evidence inputs, raw findings, validation status, human disposition, fixes, and regression tests. Model upgrades should be evaluated on known vulnerable/safe fixtures before replacing the audit baseline. [INFERENCE nist-ai-rmf,agent-security-review]

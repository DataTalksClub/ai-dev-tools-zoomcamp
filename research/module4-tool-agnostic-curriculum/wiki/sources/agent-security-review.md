# Official agent-assisted security review guidance

Primary locators:

- [FACT agent-security-review] https://support.anthropic.com/en/articles/11932705-automated-security-reviews-in-claude-code/
- [FACT agent-security-review] https://developers.openai.com/codex/use-cases
- [FACT agent-security-review] https://red.anthropic.com/2026/cvd/

Summary: Current coding-agent products support on-demand, change-triggered, and deep repository review, but their publishers still retain deterministic checks and human validation.

- [FACT agent-security-review] Claude Code documents both on-demand terminal security review and automatic pull-request review and says these complement rather than replace existing security practice and manual review.
- [FACT agent-security-review] Official Codex use cases include change-focused security scans, deep repository scans, dependency-incident audits, and remediation with regression evidence.
- [FACT agent-security-review] Anthropic's 2026 vulnerability-disclosure program uses external human triage and review before reporting high/critical findings; it describes human validation as the rate-limiting step.
- [INFERENCE agent-security-review,owasp-secure-code-review] A model finding should be accepted only when it identifies concrete code/config evidence, a plausible impact path, and a reproducible validation method; agreement between two models is prioritization evidence, not proof.

Limitations: Product documentation is partly promotional and does not establish comparative detection accuracy. The course should evaluate the workflow on known fixtures rather than claim one model is the best auditor.

Related: [recurring security audit](../concepts/recurring-security-audit.md)

Accessed: 2026-08-02.

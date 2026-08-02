# OWASP LLM01:2025 Prompt Injection

Locator: https://genai.owasp.org/llmrisk/llm01-prompt-injection/

Summary: Treat external text as untrusted input and constrain what an AI-mediated workflow can expose or do.

- [FACT owasp-prompt-injection] Prompt injection can arise from direct input or external content processed by the model.
- [FACT owasp-prompt-injection] Recommended controls include segregating untrusted content, least-privilege access, input/output controls, adversarial testing, and human approval for high-risk operations.
- [INFERENCE owasp-prompt-injection] Agent instructions, repository files, issue text, logs, and tool descriptions belong in a trust-boundary model rather than being treated as harmless context.

Limitations: This is risk guidance, not a complete agent security verification standard.

Related: [agent capability security](../concepts/agent-capability-security.md)

Accessed: 2026-08-02. Version: OWASP LLM Top 10 2025.

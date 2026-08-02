# Agent and toolchain security

- [FACT owasp-prompt-injection] External content may alter model behavior; least privilege, separation of untrusted content, and approval for high-risk operations reduce impact.
- [FACT mcp-security] Locally installed agent servers can execute code with client privileges, access local resources, and create data-exfiltration or loss risk.
- [FACT mcp-security] Consent, sandboxing, scope minimization, credential separation, token validation, and auditable identity are concrete controls.
- [INFERENCE mcp-security,owasp-prompt-injection] The lesson should inventory every capability source—not only MCP: repository instructions, skills, hooks, plugins, packages, shell commands, remote APIs, model endpoints, and inherited credentials.

Suggested learner outcome: Produce a capability bill of materials with provenance, read/write/network/secrets scope, untrusted-input exposure, approval needs, and a mitigation or removal for one unsafe capability.

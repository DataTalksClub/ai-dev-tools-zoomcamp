# Model Context Protocol Security Best Practices

Locator: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices

Summary: MCP illustrates general agent-tool security problems: installing code, delegating authority, handling credentials, obtaining consent, and preserving attribution.

- [FACT mcp-security] Local MCP servers may execute with the client's filesystem and network privileges and can create code-execution, exfiltration, and data-loss risk.
- [FACT mcp-security] Guidance calls for exact command display, explicit consent, sandboxing, restricted resources, and progressive least-privilege scopes.
- [FACT mcp-security] Token passthrough harms control enforcement, attribution, audit trails, and trust-boundary integrity.
- [INFERENCE mcp-security] These controls apply to scripts, plugins, hooks, skills, and CLI tools even when MCP is not used.

Limitations: Protocol-specific details such as OAuth resource metadata are not core curriculum for learners using only local CLI tools.

Related: [agent capability security](../concepts/agent-capability-security.md)

Accessed: 2026-08-02. Documentation version observed: 2025-11-25.

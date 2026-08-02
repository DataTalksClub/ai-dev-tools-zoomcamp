# Practitioner discussions: AI-assisted security review and agent tooling

Sources:

- [FACT practitioner-ai-security] [Claude Code Security](https://www.reddit.com/r/cybersecurity/comments/1raqles/claude_code_security/), r/cybersecurity, accessed 2026-08-02.
- [FACT practitioner-ai-security] [Am I overthinking Claude Code security or is this actually a risk?](https://www.reddit.com/r/cybersecurity/comments/1tfksxd/am_i_overthinking_claude_code_security_or_is_this/), r/cybersecurity, accessed 2026-08-02.
- [FACT practitioner-ai-security] [I've been daily driving Semgrep MCP server](https://www.reddit.com/r/mcp/comments/1lkdpv9/), r/mcp, accessed 2026-08-02.
- [FACT practitioner-ai-security] [MCP Safety Warden](https://www.reddit.com/r/cybersecurity/comments/1svfn93/introducing_mcp_safety_warden_a_proxy_for_vetting/), r/cybersecurity, accessed 2026-08-02.

Summary: Practitioners disagree on the quality of model security findings, but broadly surface the need for independent evidence, separation of duties, and control of the agent's own capabilities.

## Claims

- [FACT practitioner-ai-security] Security participants reported both useful discoveries and substantial false positives or misses compared with fuzzers and linters. Several argued that the same agent or model family should not write, review, fix, and certify its own code.
- [FACT practitioner-ai-security] Commonly proposed workflows layer deterministic scanners, focused model review, and manual examination of security-sensitive business logic rather than treating any one output as a verdict.
- [FACT practitioner-ai-security] Semgrep MCP users described value in running local deterministic scans from the agent workflow. The durable pattern is structured scanner evidence plus explanation; MCP is one possible transport.
- [FACT practitioner-ai-security] Agent-security discussions focus on undeclared capabilities, tool poisoning, prompt injection, credentials, input/output gates, and telemetry around tool execution. Some examples are projects advertised by their authors and must not be treated as independent validation.
- [FACT practitioner-ai-security] Developers explicitly worry about terminal agents that can read the repository, network, credentials, and shell—not only MCP servers. Inventory and enforcement therefore must cover the entire execution environment.

## Teaching consequence

[INFERENCE practitioner-ai-security,owasp-secure-code-review,mcp-security] Teach a capability inventory and an evidence pipeline. A model finding becomes a candidate issue that must survive code evidence, a reproduction or deterministic check, and human disposition.

## Limitations

Reddit evidence is anecdotal and includes sarcasm, speculation, low-vote posts, and self-promotion. It cannot establish scanner accuracy or product security. Official documentation and standards remain the authority for capabilities and controls.

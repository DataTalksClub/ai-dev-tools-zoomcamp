# Portable execution model

## Baseline contract

- [HUMAN] The implementation must work with Codex, Claude Code, and comparable terminal agents in interactive or headless mode.
- [INFERENCE current-module-4,tool-repositories] The least-common-denominator interface should be repository files plus ordinary CLI programs, not a vendor-specific plugin, hook, or MCP configuration.
- [INFERENCE nist-ssdf,opentelemetry-signals] Evidence producers should favor deterministic commands, explicit inputs, versioned configuration, exit status, and structured output where available.
- [INFERENCE owasp-prompt-injection,mcp-security] The reasoning agent should receive only needed evidence, run with explicit filesystem/network/secret scope, and require approval before material state changes.
- [INFERENCE nist-ai-rmf] Headless runs need a declared task, allowed actions, data policy, output schema, time/cost boundary, and durable audit record.

## Separation of responsibilities

```text
collector/checker -> evidence files -> coding agent -> proposed decision/action
                                            |
                                  policy + approval gate
                                            |
                                      action command
                                            |
                                    independent verify
```

The agent may invoke each stage, but the stages should remain separately observable. This prevents a fluent narrative from hiding missing evidence or an unverified action.

## Feasible do-it-yourself building blocks

- [INFERENCE current-module-4] A Markdown/JSON risk model and capability inventory.
- [INFERENCE nist-ssdf,owasp-secure-code-review] A shell or task-runner script that executes existing linters, tests, dependency checks, and policy checks and normalizes results.
- [INFERENCE owasp-secure-code-review] A portable review prompt/task file that consumes a diff, specification, threat notes, and check outputs.
- [INFERENCE opentelemetry-signals,nist-incident-response] A prepared operational evidence bundle and investigation template.
- [INFERENCE nist-ai-rmf] A small policy file plus wrapper that permits or denies model/data/action combinations.
- [INFERENCE nist-ai-rmf,mcp-security] JSON Lines audit events recording actor, task, inputs by reference, tool command, result, approval, and verification.

[INFERENCE nist-ssdf,current-module-4] “Implement ourselves” should mean composing the control plane and evidence workflow, not reimplementing static analysis, secret detection, telemetry collection, or model serving.

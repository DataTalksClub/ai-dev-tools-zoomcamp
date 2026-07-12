# Module 4 — Open-Source AI Tools for Security, Audit, and DevOps

> [!NOTE]
> This 2026 module page is currently a draft. You can use it to see what we are preparing, but the final videos, exercises, homework, and requirements may change before the cohort starts.

## Overview

This module focuses on open-source AI tools around the production workflow:

- AI pull request audit
- AI-accessible security scanning
- agent, MCP, and reusable workflow security scanning
- Kubernetes diagnostics
- incident investigation
- AI tool governance

Module 4 is intentionally narrow:

```text
Only open-source AI tools.
Only security, audit, and DevOps.
No general coding agents.
No LLM application evals.
No AI test-generation focus.
```

## Core Tool Stack

Required:

- PR-Agent
- Semgrep MCP Server
- Snyk Agent Scan
- K8sGPT
- LiteLLM
- Ollama

Optional or instructor-led:

- HolmesGPT
- Stakpak
- garak
- other agent security scanners

## Lessons

### Lesson 4.1 — Production AI Risk Model

Goal: understand the risks before adding tools.

Topics:

- AI-generated code risk
- agent tool risk
- MCP server risk
- skill/plugin/extension supply-chain risk
- CI/CD risk
- Kubernetes and operations risk
- model gateway and data exposure risk

Deliverable:

```text
security/ai-production-risk-model.md
```

### Lesson 4.2 — AI PR Audit with PR-Agent

Goal: use AI-assisted review at the pull request boundary.

Labs:

- configure PR-Agent
- generate a PR description
- run a review
- ask questions about risky files
- update changelog notes
- manually evaluate the output

Deliverables:

```text
.github/workflows/pr-agent.yml
.pr_agent.toml
docs/pr-agent-output.md
docs/pr-audit-checklist.md
```

Teaching point: AI PR review is not approval. It is an audit assistant.

### Lesson 4.3 — AI-Accessible Security Scanning with Semgrep MCP

Goal: show how an AI assistant can use a deterministic security scanner.

Lab:

1. Add an intentionally vulnerable pattern to the app.
2. Ask an MCP-compatible assistant to run Semgrep MCP.
3. Review the finding.
4. Ask the assistant to explain the finding.
5. Fix the issue.
6. Re-run the scan.
7. Record the remediation.

Deliverables:

```text
security/semgrep-findings.md
security/custom-rule.yml
security/remediation-notes.md
```

Teaching point: the LLM explains and orchestrates; Semgrep provides the evidence.

### Lesson 4.4 — Agent, MCP, and Extension Security Scanning with Snyk Agent Scan

Goal: audit the agent extension pack from Module 3.

Lab:

1. Use the Module 3 instructions, reusable workflows, subagents, hooks, and MCP server.
2. Run Agent Scan.
3. Review detected risks.
4. Fix one issue in a workflow, tool description, or permission boundary.
5. Re-scan.
6. Write a permission table.

Deliverables:

```text
security/agent-scan-report.json
security/agent-scan-notes.md
security/tool-permissions.md
security/mcp-threat-model.md
```

Teaching point: agent extensions are a supply chain. Instructions, skills, MCP servers, plugins, and tool descriptions deserve review.

### Lesson 4.5 — Kubernetes Diagnostics with K8sGPT

Goal: introduce AI-assisted DevOps diagnosis without turning the course into a Kubernetes course.

Suggested local environments:

- kind
- k3d
- minikube

Lab: deploy a toy version of the Module 2 app to a local cluster, intentionally break it, run K8sGPT, then verify with `kubectl`.

Deliverables:

```text
ops/k8s-broken-deployment.yaml
ops/k8sgpt-report.json
ops/k8sgpt-diagnosis.md
```

Teaching point: K8sGPT should be grounded in cluster state. Learners must verify with `kubectl`.

### Lesson 4.6 — Incident Investigation with HolmesGPT

Goal: show AI as an SRE investigation assistant.

This can be optional or instructor-led for the first 2026 cohort.

Possible deliverables:

```text
ops/holmes-investigation.md
ops/incident-summary.md
ops/follow-up-actions.md
```

Teaching point: AI can correlate and summarize operational evidence, but humans confirm root cause and own remediation.

### Lesson 4.7 — AI Tool Governance with LiteLLM and Ollama

Goal: control how AI tools access models and sensitive data.

Topics:

- open-source tool vs hosted model
- local model vs hosted model
- virtual keys
- tool-specific keys
- budget limits
- model routing
- audit logs
- prompt/data retention
- redaction
- local model fallback

Deliverables:

```text
ops/litellm-config.yaml
docs/ai-tool-policy.md
docs/model-routing.md
docs/data-handling.md
```

Teaching point: "open-source AI tool" does not automatically mean "private." The model, gateway, logs, and data flow matter.

## Module Deliverable: AI Security/Audit/DevOps Report

Students apply Module 4 to their Module 2/3 project.

Required deliverables:

```text
security/
  ai-production-risk-model.md
  semgrep-findings.md
  agent-scan-report.json
  agent-scan-notes.md
  tool-permissions.md
  mcp-threat-model.md

ops/
  k8sgpt-report.json
  k8sgpt-diagnosis.md
  litellm-config.yaml

docs/
  pr-agent-output.md
  pr-audit-checklist.md
  ai-tool-policy.md
  data-handling.md
```

Optional deliverables:

```text
ops/
  holmes-investigation.md
  incident-summary.md
  follow-up-actions.md
```

The final report should answer:

- What did we audit?
- Which AI tools were used?
- Which findings were real?
- Which findings were false positives or not relevant?
- What was fixed?
- What remains risky?
- Which tools have read/write access?
- Which model provider sees which data?
- Which actions require human approval?

## Previous Cohort Materials

The previous version of this module is archived here:

- [2025 archived CI/CD and DevOps module](../cohorts/2025/05-cicd-devops/)

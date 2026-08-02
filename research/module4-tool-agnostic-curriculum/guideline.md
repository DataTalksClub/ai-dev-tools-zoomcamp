# Guideline: 90-minute Module 4 outline for discussion

Status: proposed outline; not approved for article writing or implementation

## Working title

**Module 4 — From Deployment to Operations: Observability, Agent Response, and Security Audits** [PROPOSAL]

The title describes the system learners will operate. Product names belong inside implementation examples, not in the module structure. [HUMAN]

## Audience and promise

The learner has the Module 2 application: React frontend, FastAPI backend, Postgres, containers, public deployment, and CI/CD. [FACT current-module-4,syllabus-proposal]

In 90 minutes, the learner will turn that application from merely deployed into minimally operable. They will be able to:

1. follow one failed backend request through a metric, trace, structured log, and deployment version;
2. create one alert that represents sustained user impact and contains enough context to act;
3. invoke Codex, Claude, or another headless terminal agent as a read-only first responder;
4. enforce outside the model whether a known rollback may run or a human must take over;
5. run a repeatable security audit that combines deterministic evidence, model reasoning, and human validation. [INFERENCE observability-pipeline,alerting-sre,safe-remediation,agent-security-review]

The optional extra 30 minutes deepens one or two controls; it must not be required to complete the core story. [HUMAN]

## Central idea

The module teaches one feedback loop:

```text
change
→ observe user impact
→ alert with context
→ investigate from evidence
→ authorize a bounded response or escalate
→ verify recovery
→ audit the code and the response trail
```

Deployment is not the end of delivery. An operable system must expose user impact, preserve evidence, constrain automation, verify recovery, and let a human reconstruct important decisions. [INFERENCE nist-incident-response,alerting-sre,safe-remediation]

## Why this is problem-first rather than tool-first

The original tools expose real problems, but a 90-minute catalogue would produce fragile knowledge. The outline therefore starts with the problem and adds products only after a small DIY implementation demonstrates the pattern. [HUMAN]

| Problem | Concept taught | DIY version | Products mentioned afterward |
| --- | --- | --- | --- |
| We cannot explain a failed request | Correlated metrics, traces, logs, and deployment identity | Instrument one FastAPI path; export through OTLP | OpenTelemetry, Collector, Prometheus, Loki, Tempo, Grafana |
| Alerts are noisy or context-free | User-impact symptoms, duration, actionability, ownership, runbook | One sustained 5xx alert with a structured webhook | Prometheus/Alertmanager and equivalent platforms |
| Humans collect the same evidence under pressure | Read-only evidence adapters and a structured incident packet | Shell/Python orchestrator invokes a generic headless agent | HolmesGPT, K8sGPT, commercial AI-SRE products |
| Agent confidence gets mistaken for authority | External policy, least privilege, reversibility, verification, escalation | Allowlist one versioned rollback; block everything else | Agent platforms and policy engines |
| Model reviews are persuasive but fallible | Deterministic checks + independent reasoning + human disposition | Scanner JSON plus one model review and manual validation | Semgrep MCP, PR-Agent, Codex, Claude security review |
| Agent extensions become a supply chain | Capability inventory, provenance, read/write/network/secrets scope | Small capability bill of materials | Snyk Agent Scan and other MCP/agent scanners |
| Model calls need placement and governance | Provider-neutral interface, data policy, identity, budget, audit | A tiny CLI adapter and recorded model metadata | LiteLLM, Ollama, hosted model APIs |

[INFERENCE problem-first-tool-landscape] K8sGPT, Agent Scan, gateways, and local inference are valid examples, but not all belong in the core live build.

## Concrete teaching architecture

```text
Module 2 app + CI/CD
        |
  OpenTelemetry SDK
        |
OpenTelemetry Collector
   /      |       \
metrics  logs    traces
   \      |       /
       Grafana
 dashboard + one alert
             |
      incident webhook
             |
   evidence collector ──→ headless agent
             |                  |
       external policy ← proposed action
          /        \
 allowlisted       escalation packet
 rollback                to human
     |
 recovery check + append-only incident record

Separate path: deterministic security check → model review → human disposition
```

The collector is the stable telemetry boundary. The agent adapter is the stable reasoning boundary. The external policy is the stable authorization boundary. Backends and model vendors can change independently. [INFERENCE observability-pipeline,mcp-security,safe-remediation]

## The prepared incident

Use one deliberately bad deployment that increases 5xx responses on an important backend operation. It provides a complete, teachable story:

- the dashboard shows user-visible errors beginning after a deployment;
- an exemplar or trace link leads to a failed request;
- correlated structured logs expose the concrete failure without leaking sensitive data;
- the incident packet includes the active commit and previous known-good deployment;
- the agent proposes the versioned rollback runbook;
- external policy recognizes the known signature and allows only that runbook;
- a health request and error-rate query verify recovery. [PROPOSAL]

The instructor then changes one fact—remove the known signature, make evidence conflict, or involve data/security—to show the exact same agent being forced to escalate. This demonstrates the human boundary without requiring a second full incident build. [PROPOSAL]

## 90-minute workshop outline

### 0–10 minutes — The operational gap

Start from the deployed Module 2 application and trigger the prepared regression.

Questions:

- Is the app failing for users?
- Which operation is affected?
- Did the latest deployment cause it?
- What evidence can a responder trust?
- What is the responder allowed to change?

Show the end-to-end loop and establish three boundaries: telemetry, reasoning, and authorization. Do not begin with installation commands. [PROPOSAL]

### 10–30 minutes — Observe one request end to end

Teach:

- traces describe the request path;
- metrics aggregate behavior and support alert conditions;
- logs preserve event detail;
- stable service/environment/version attributes and trace IDs connect the evidence;
- telemetry is also sensitive, costly data that needs redaction and cardinality discipline. [FACT observability-pipeline]

Live work:

- add or inspect OpenTelemetry instrumentation on one FastAPI path;
- send OTLP to the collector;
- trigger one successful and one failed request;
- pivot in the prebuilt Grafana stack from error metric to trace to correlated log and deployment version.

React/browser tracing is an optional extension because current browser instrumentation remains experimental. [FACT observability-pipeline]

### 30–45 minutes — Create one alert worth waking up for

Teach:

- page on sustained user-visible symptoms, not every internal cause;
- dashboards hold diagnostic context; alerts imply action;
- thresholds need duration/slack;
- alerts need service, severity, symptom, time, evidence links, recent change, owner, and runbook;
- grouping, deduplication, inhibition, and metamonitoring matter in a mature system. [FACT alerting-sre]

Live work:

- create or inspect one sustained 5xx-rate rule;
- test it with the prepared regression;
- inspect its structured webhook payload.

Practitioner evidence supports keeping the core to one carefully designed alert: teams report alert fatigue, rotting rule packs, missing runbooks, and dashboards that nobody uses. [FACT practitioner-observability]

### 45–70 minutes — Agent as first responder, policy as authority

Teach this sequence:

```text
alert → collect facts → form/test hypotheses → propose action
      → policy decision → act or escalate → verify → record
```

The DIY responder:

1. receives the alert webhook;
2. runs allowlisted, read-only queries for health, metrics, logs/traces, and deployment/git history;
3. writes a bounded evidence packet;
4. invokes a configured headless terminal-agent adapter;
5. validates the response against a schema;
6. sends the proposed action to an external policy check;
7. runs only the exact allowlisted rollback script or writes an escalation packet;
8. verifies and records the result. [PROPOSAL]

Portable adapter contract:

```text
input:  versioned task + evidence directory + output schema
output: structured facts, hypotheses, proposed action, uncertainty
limits: working directory, read-only credentials, timeout, command budget, network scope
```

Codex CLI and Claude Code headless mode are concrete adapters. Model prompts do not grant authority; shell wrappers, credentials, sandboxing, and policy do. [INFERENCE mcp-security,practitioner-ai-operations]

Autonomy levels:

| Level | What happens | Core policy |
| --- | --- | --- |
| 0 | Alert enrichment | Automatic |
| 1 | Read-only investigation and recommendation | Automatic within limits |
| 2 | Tested, reversible, versioned runbook | Only for an allowlisted signature and deterministic postcondition |
| 3 | Patch/PR in isolation | Human reviews; never auto-merge in this module |
| 4 | Novel, destructive, broad, security/data/secret action | Human required |

Automatic repair requires a known signature, versioned runbook, bounded blast radius, reversibility/idempotence, deterministic recovery check, strict retry/time/cost limits, and a full log. Unknown causes, conflicting evidence, security/data implications, missing verification, or failed retries escalate. [INFERENCE safe-remediation]

Practitioners describe evidence gathering, incident summaries, and proposed commands as useful; unreliable root-cause claims and write access remain the difficult boundary. [FACT practitioner-ai-operations]

### 70–87 minutes — Recurring security audit: evidence before eloquence

Teach three layers:

1. deterministic checks for known patterns and dependencies;
2. focused model reasoning for context, abuse paths, business logic, and missed interactions;
3. human validation and disposition. [INFERENCE owasp-secure-code-review,agent-security-review]

Live work:

- run one deterministic scanner and preserve structured output;
- run one headless model with a versioned audit brief against the same commit;
- require each finding to include code evidence, impact/abuse path, uncertainty, and a validation method;
- validate or reject one finding and record the disposition.

Current quality-first examples may include OpenAI `gpt-5.6-sol` with `max` reasoning and Anthropic `claude-fable-5`. A scheduled deeper audit can run both independently; the 90-minute live exercise requires only one so it does not depend on two paid accounts. ChatGPT is an interactive product surface, not an independent model vote when it uses the same GPT family. [FACT current-audit-models] [PROPOSAL]

Semgrep MCP and PR-Agent are examples after the DIY flow. The pattern is scanner evidence plus contextual review, not dependence on MCP or one PR bot. Practitioner discussions report both useful model findings and false positives/misses, supporting independent evidence and separation of duties. [FACT practitioner-ai-security]

### 87–90 minutes — Close the loop

Given a commit or incident ID, show that we can reconstruct:

- deployed version and user impact;
- alert and evidence inspected;
- model/configuration and proposed action;
- policy decision and command executed;
- recovery verification or escalation;
- related security finding and human disposition.

End on the operating principle: the model may reason; the system must observe, authorize, verify, and remember. [PROPOSAL]

## Optional extension to 120 minutes

Choose based on audience; do not attempt every option.

### Recommended extension: ambiguous incident and capability audit

- **90–105:** replay the incident with conflicting or security-sensitive evidence; learners inspect the escalation packet and improve its next-action recommendation.
- **105–120:** inventory the agent's skills, MCP servers, shell, filesystem, network, and credentials; classify provenance and read/write/network/secrets scope; remove or mitigate one unsafe capability.

This adds the two concepts the compressed demo can only show briefly: good escalation under uncertainty and security of the responder itself. Snyk Agent Scan is then shown as a product that automates part of the inventory/inspection problem. [PROPOSAL]

Alternative extensions include adding the second independent model audit, instrumenting the frontend, writing alert tests, or swapping the model adapter to a gateway/local endpoint. [PROPOSAL]

## Deliverables

Keep artifacts small enough that learners understand them:

```text
observability/
  collector.yaml
  compose.yaml
  dashboard.json
  alerts.yaml
incident-response/
  collect-evidence.sh
  responder-task.md
  evidence.schema.json
  autonomy-policy.yaml
  runbooks/rollback.sh
  incidents/
security-audit/
  audit-brief.md
  findings.schema.json
  runs/
docs/
  operations-and-security-report.md
```

The stack configuration should be mostly prepared before the workshop. Learners should edit the semantic parts—instrumentation, alert meaning, evidence, policy, and validation—not spend the session debugging infrastructure downloads. [PROPOSAL]

## Tool decisions

### Core, because they implement the running system

- OpenTelemetry SDK and Collector;
- Prometheus, Loki, Tempo, Grafana, and alert delivery;
- a deterministic security scanner with structured output;
- one configurable terminal-agent adapter. [PROPOSAL]

### Mention after the concept

- HolmesGPT for cross-source investigation;
- K8sGPT for Kubernetes-specific analysis/explanation;
- PR-Agent for pull-request workflows;
- Semgrep MCP as an agent transport over deterministic scanning;
- Snyk Agent Scan for extension/capability discovery;
- Stakpak and similar packaged DevOps agents. [INFERENCE tool-repositories]

### Extension only

- LiteLLM for multi-provider gateway policy;
- Ollama for local inference/data placement;
- formal LLM red-team tools such as garak when the target is itself an LLM application. [INFERENCE practitioner-model-infrastructure,tool-repositories]

Kubernetes is not a prerequisite. This module extends the Module 2 Docker/AWS system. [HUMAN]

## Important production practices we acknowledge but do not teach deeply

- SLIs/SLOs, error budgets, and multi-window burn-rate alerts;
- synthetic browser monitoring, frontend real-user monitoring, profiling, and host/database capacity;
- sampling, retention, PII redaction, tenant isolation, and observability cost control;
- canary/progressive delivery, feature flags, chaos testing, backups, and restore drills;
- on-call ownership, incident command, status communication, and blameless postmortems;
- secrets/dependency/container/IaC scanning, SBOMs, build provenance/signing, penetration testing, and disclosure;
- evaluation sets for model/provider upgrades and measurement of audit false positives/negatives;
- high availability and metamonitoring for the observability/response system. [INFERENCE nist-ssdf,nist-incident-response,alerting-sre,observability-pipeline]

These are excluded because they would obscure the workshop's main feedback loop, not because they are unimportant.

## Guardrails and non-goals

- Do not present dashboards or successful telemetry ingestion as proof of observability value.
- Do not copy a large alert pack or page on every resource fluctuation.
- Do not promise certain automated root-cause analysis.
- Do not use prompt instructions or command regexes as authorization.
- Do not give the agent unrestricted production/cloud credentials.
- Do not auto-merge model-generated changes or let a model certify its own fix.
- Do not send source or telemetry to a provider without an explicit data/retention decision.
- Do not claim local inference is automatically private or production-ready.
- Do not rebuild telemetry storage, static analysis, or model serving; build the orchestration, policy, evidence, and audit layer around standard interfaces. [INFERENCE mcp-security,practitioner-ai-operations,practitioner-model-infrastructure]

## Research confidence and disagreements

Primary standards and official documentation support the architecture, alert design, safe automation controls, and layered security review. Reddit/social research supports the relevance of the pain points but is anecdotal, self-selected, and sometimes promotional. It should appear in the article as practitioner experience, never as measured industry prevalence. [FACT practitioner-observability,practitioner-ai-operations,practitioner-ai-security]

Open questions that remain product decisions rather than research gaps:

1. Is the working title right?
2. Is the prepared incident specifically a bad deployment rollback, or should it be a different bounded repair?
3. Should the optional 30 minutes prioritize the ambiguous escalation plus agent capability audit, as recommended, or the second independent model audit?
4. Should the workshop repository include both Codex and Claude adapters, or one reference adapter plus documented commands for the other?

No public article or implementation should begin until this outline is discussed and explicitly approved. [HUMAN]

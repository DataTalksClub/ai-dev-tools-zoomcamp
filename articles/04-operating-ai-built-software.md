# Operate an AI-Built App with Observability, Agents, and Security Audits

In the [second article](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/articles/02-end-to-end.md)
in this series, I used a coding assistant to build and deploy a full-stack app.
The app is [snake-royale](https://github.com/alexeygrigorev/snake-royale), a
multi-user version of the classic Snake game. It has a React frontend and a
FastAPI backend. We added Postgres, containers and a pipeline that deploys
every change.

That gets the app online, but it doesn't tell me whether the app still works.

If score submissions start returning `500`, I need to know that users are
affected and find the failed requests. Then I need to connect them to the
latest deployment and decide what to do. CI/CD can ship a bad release as
efficiently as a good one.

I also want an agent to become the first line of support. It can collect the
same evidence I would collect, compare it with recent changes, and propose the
next action. But I don't want a model with general cloud credentials deciding
what to change in production.

Here, I build the system around that agent:

- how the app produces evidence
- which failures deserve an alert
- what an agent investigates first
- what it may fix without a person
- when it must escalate
- how we audit both the code and the agent

OpenTelemetry sends data to Prometheus, Loki and Tempo in the concrete example,
and Grafana displays it. We'll run the responder with Codex or Claude Code.
The products are replaceable. I want to keep the boundaries between evidence,
reasoning, permission and verification.

## Overview

We start with one bad deployment. An important backend operation begins
returning `500`, so the error rate rises. The alert sends a structured payload
to a small responder. The responder gathers evidence before it starts an
agent, and a separate policy checks the action the agent proposes.

![A deployed app emits telemetry, raises an alert, and sends evidence to an
agent. An external policy either escalates the incident or permits a known
rollback, which the system verifies and records.](images/04-operate-app-overview.png)

The agent can reason about any action, but we expose only one action to it: a
versioned rollback script that we approved before the incident. If the evidence
doesn't match that case, the responder sends a human an incident report
instead.

A model supplies confidence, while the policy wrapper enforces permission.

## Instrument before choosing a dashboard

We first instrument the app so it records what it's doing. I use
[OpenTelemetry](https://opentelemetry.io/docs/) because it gives us a
vendor-neutral format for traces, metrics, and logs.

Each kind of evidence answers a different question:

- A metric tells us that the score-submission error rate increased.
- A trace shows the path of one failed request through FastAPI and the
  database call.
- A log records the exception and the values we deliberately chose to keep.

We add the service name, environment and deployed commit to every record. We
also put the trace ID in structured logs. We can now move from an error rate on
a chart to one failed request. From there, we find its log entry and the code
version that served it.

I ask the coding assistant to instrument one important operation first:

```text
Instrument the FastAPI backend with OpenTelemetry.

Start with the endpoint that submits a game score.

- export traces and metrics with OTLP
- include service name, environment and deployed git commit as resource
  attributes
- keep application logs as structured JSON on stdout
- inject the trace ID and service name into each log record
- add one custom counter for score-submission results
- do not record passwords, tokens, request bodies or user names

Write a test that submits one score and verifies that the instrumentation does
not change the response.
```

I don't start with the browser. OpenTelemetry's current JavaScript
documentation still labels [browser instrumentation as experimental](https://opentelemetry.io/docs/languages/js/).
The backend gives us stable traces and metrics for the incident we want to
teach. We can add browser tracing later when we need the path from a click to
an API request.

## Put a collector between the app and storage

The app sends OTLP to an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/).

The collector receives and processes the telemetry, then exports it to our
chosen backends:

- Prometheus stores metrics.
- Loki stores logs.
- Tempo stores traces.
- Grafana reads all three.

We could export directly from the app to each backend. Then every backend
change would require an application change, and a slow backend could affect
the app's telemetry exporters. The collector gives us one stable boundary and
handles work such as batching and retries outside the request path.

I give the assistant the architecture rather than asking it to choose an
observability stack:

```text
Add an observability/ directory with Docker Compose configuration for:

- an upstream OpenTelemetry Collector
- Prometheus for metrics
- Loki for logs
- Tempo for traces
- Grafana for dashboards and alerting

The app sends OTLP only to the collector. Configure Grafana so I can move from
a trace to logs with the same trace ID and from a metric exemplar to its trace.

Keep high-cardinality values such as trace IDs out of Loki labels. Store them
as structured metadata instead.

Add make targets to start the stack, generate sample traffic and stop it.
```

For a 90-minute session, I prepare most of the Compose and datasource
configuration beforehand. We edit the instrumentation and use the telemetry
during the session. Watching five containers download isn't an observability
lesson.

## Follow one failed request

Before adding an alert, I break the score-submission path and send a request.

Then I try to answer these questions in order:

1. Did users receive errors?
2. Which operation failed?
3. Can I open one representative request?
4. Which log belongs to that request?
5. Which deployment served it?

If the dashboard shows CPU usage but can't answer those questions, I haven't
instrumented the incident I care about.

This came up repeatedly when I looked through practitioner discussions. Teams
can have an expensive observability stack and still debug from raw console
logs. In one [discussion about alert fatigue](https://www.reddit.com/r/sre/comments/1nm7sbi/alert_fatigue_is_killing_me/),
SREs kept returning to three actions. Measure customer impact, attach a runbook
and remove alerts that nobody can act on.

We use the dashboard to investigate, but it isn't the finished result.

## Create one actionable alert

I don't import a large alert pack. I create one alert for a sustained increase
in failed score submissions.

I require both of these conditions:

- enough requests failed to affect users
- the failure lasted long enough that one brief error doesn't start an
  incident

This follows the [Prometheus alerting guidance](https://prometheus.io/docs/practices/alerting/).
Keep alerts few, allow small blips and page on symptoms that require action.
CPU, memory and database connections still belong on the dashboard because
they help explain the incident. They don't all need to wake someone up.

I ask the assistant for the rule and its test together:

```text
Create one Prometheus alert for a sustained user-visible error rate on score
submission.

Use the custom request/result metric from the FastAPI instrumentation. Choose a
threshold that the load generator can cross during the demo, and require the
condition to hold for two minutes.

Include these labels and annotations:

- affected service and environment
- severity and owner
- user-visible symptom
- start time
- Grafana dashboard link
- active deployment version
- runbook path

Add a test for the alert expression and document why this is an alert rather
than a dashboard-only metric.
```

In a larger setup, [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)
groups and deduplicates related alerts. It also routes, silences and inhibits
them. For this example, Grafana sends one webhook to our responder. The webhook
contains the symptom and links. It doesn't contain a model prompt or a command
to run.

## Collect evidence before starting the agent

I keep the responder small enough that a shell or Python script can handle the
first version.

It receives the alert and collects a fixed evidence directory:

```text
incidents/2026-08-02T10-30-00Z/
  alert.json
  health.json
  metrics.json
  traces.json
  logs.jsonl
  deployment.json
  recent-commits.txt
```

The script uses read-only credentials and known queries. The model
doesn't invent a `kubectl`, cloud, or database command and run it against the
live system. It starts from the same bounded packet every time.

Then we give the agent a versioned task:

```text
You are the first responder for one production alert.

Read the files in the incident directory. Do not modify code or system state.

Return:

- observed facts, with the evidence file for each fact
- up to three hypotheses, ordered by support
- checks that would distinguish the hypotheses
- one proposed action, or ESCALATE
- uncertainty and missing evidence

Do not call something the root cause unless the evidence rules out the main
alternatives. A proposed action is not permission to run it.
```

We also require a JSON schema for the response. The schema catches a missing
field, but it doesn't make the diagnosis true. We still need evidence and a
policy decision.

## Keep the responder tool-agnostic

The responder invokes a command with four inputs:

```text
task + evidence directory + output schema + resource limits
```

It expects one structured response through an interface that doesn't mention a
model vendor.

With Codex, the adapter can call
[`codex exec`](https://learn.chatgpt.com/docs/non-interactive-mode.md):

```bash
codex exec \
  --sandbox read-only \
  --ephemeral \
  --output-schema incident-response/response.schema.json \
  --output-last-message incidents/2026-08-02T10-30-00Z/response.json \
  -C . \
  - < incident-response/responder-task.md
```

With Claude Code, the adapter uses [print mode](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
and exposes only file-reading tools:

```bash
claude -p \
  --permission-mode plan \
  --tools "Read,Grep,Glob" \
  --no-session-persistence \
  --output-format json \
  --json-schema "$(jq -c . incident-response/response.schema.json)" \
  < incident-response/responder-task.md \
  > incidents/2026-08-02T10-30-00Z/response.json
```

The exact flags will change, but we keep the same adapter interface. It accepts
one task and bounded evidence. It enforces permissions, structured output, a
timeout and an audit record.

Projects such as [HolmesGPT](https://github.com/HolmesGPT/holmesgpt) connect an
agent to live observability sources and investigate across them.
[K8sGPT](https://github.com/k8sgpt-ai/k8sgpt) runs Kubernetes analyzers and can
ask a model to explain the results. They solve versions of the same problem.
Our small responder shows the same design without making Kubernetes or one
agent platform a prerequisite.

## Confidence is not permission

An agent can be 95% confident and still be wrong. More importantly, it can be
confident about an action we never wanted it to take.

The responder sends the proposed action to code outside the model.

That code checks an allowlist such as:

```yaml
actions:
  rollback_last_release:
    required_signature: error_rate_after_deployment
    command: runbooks/rollback.sh
    verify: runbooks/verify-recovery.sh
    max_attempts: 1
    timeout_seconds: 300
```

The rollback can run only when all of these conditions hold:

- the evidence matches a known failure signature
- we approved and versioned the runbook before the incident
- the action affects one bounded target
- we can reverse it or run it repeatedly without making the state worse
- no security, authorization, sensitive-data, or data-integrity question is
  unresolved
- an independent check can tell us whether the service recovered
- the responder hasn't exhausted its time or action budget

Everything else goes to a person, including conflicting evidence, novel
commands and broad outages. Database repairs, secret rotations, failed
rollbacks and incidents we can't verify also require a person.

This is close to what practitioners report in [discussions about AI on call](https://www.reddit.com/r/sre/comments/1t6wqux/anyone_using_ai_for_actual_sreoncall_operations/).
In those discussions, operators use agents to collect logs and metrics, draft
timelines and retrieve runbooks. Reliable root-cause analysis remains hard when
context is missing. Write access also risks increasing the blast radius.

[Google's SRE guidance](https://sre.google/sre-book/automation-at-google/)
also treats automation as a force multiplier rather than a substitute for
engineering judgment. We automate the case we can specify and test. We don't
turn every incident into an open-ended production task.

## Escalate with a useful report

"I couldn't fix it" isn't an escalation report.

When the policy rejects an action, the responder writes:

- what users are experiencing
- facts and links to their evidence
- the active deployment and recent changes
- hypotheses already checked
- commands or runbooks attempted
- the current service state
- what remains unknown
- the safest next action for a person

We can demonstrate both branches with one prepared incident. First, the
evidence matches the known post-deployment error signature, so the rollback
runs and the responder verifies that the error rate falls. Then we remove the
deployment match or introduce evidence of a data-integrity problem. The same
agent now has to escalate.

The model didn't get less intelligent in the second run. We changed what the
policy authorized it to do.

## Audit the code with more than a model opinion

Operational response covers failures we can observe. A recurring security
audit looks for weaknesses before they become incidents.

I split the audit into three parts:

1. A deterministic scanner finds known code patterns and dependency issues.
2. A model reviews context, abuse paths, authorization, and business logic.
3. A person validates the evidence and decides what to fix.

For example, run Semgrep and keep its machine-readable output:

```bash
semgrep scan \
  --config auto \
  --json \
  --output security-audit/semgrep.json \
  .
```

Then give the model the repository commit, threat context, and scanner result:

```text
Audit this repository for security weaknesses.

Treat security-audit/semgrep.json as evidence, not as a verdict. Also inspect
authorization, data flows, shell/file operations, CI/CD, observability data,
and business-logic abuse cases that pattern rules may miss.

For every finding include:

- file and line evidence
- the concrete abuse or failure path
- impact and uncertainty
- how a person can reproduce or disprove it
- a proposed fix and regression test

Do not change the code. Do not mark a finding resolved.
```

[Semgrep MCP](https://github.com/semgrep/semgrep/blob/develop/cli/src/semgrep/mcp/README.md)
can expose the same scanner to an agent through MCP. A deterministic tool
produces evidence, and the model explains or challenges it. MCP is one way to
connect the two.

[PR-Agent](https://github.com/The-PR-Agent/pr-agent) applies model review at
the pull-request boundary. Claude Code includes
[automated security reviews](https://support.anthropic.com/en/articles/11932705-automated-security-reviews-in-claude-code/),
and Codex supports non-interactive review and structured output. These tools
can help, but no single one should handle the entire lifecycle. We separate
writing, reviewing, fixing and certifying the change.

## Use two reviewers only when the audit needs them

For every change, I would run deterministic checks and one focused review of
the diff. For a release or scheduled deep audit, I would use two independent
model families and keep their outputs separate until both finish.

As of August 2026, two quality-first examples are:

- OpenAI [`gpt-5.6-sol`](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
  with `max` reasoning effort
- Anthropic [`claude-fable-5`](https://www.anthropic.com/claude/fable).

The name "GPT-5.6 Sol Max" refers to `gpt-5.6-sol` with the reasoning effort
set to `max`, not a separate model. OpenAI recommends reserving `max` for the
hardest quality-first tasks and comparing it with lower settings on real
examples.

Fable 5 has two important constraints for this use case. Anthropic requires
30-day retention for Fable traffic, and its cyber safeguards can route or
block some security requests. We must decide whether the source code may go to
that provider and handle a legitimate defensive audit that doesn't run as
expected.

ChatGPT can help a person investigate a finding interactively. If it uses the
same GPT-5.6 family as the automated reviewer, it's another interface, not an
independent third opinion.

Agreement between two models raises the priority of a finding. It doesn't
prove the finding. A reproduction, scanner result, test, or informed human
review still decides.

## Audit the agent too

The responder now has instructions, CLI adapters and filesystem access. It
also has model credentials and perhaps MCP servers. We need to audit all of
them.

Create a capability table:

```text
Capability | Source | Read | Write | Network | Secrets | Approval
-----------|--------|------|-------|---------|---------|---------
metrics    | local  | yes  | no    | local   | no      | no
logs       | local  | yes  | no    | local   | no      | no
git        | system | yes  | no    | no      | no      | no
rollback   | repo   | no   | yes   | deploy  | scoped  | policy
```

Review where each capability came from and which version we trust. Record what
input it processes and which credential enforces its limits. A sentence in the
prompt that says "read only" isn't the same as a read-only token.

[Snyk Agent Scan](https://github.com/snyk/agent-scan) is one tool for
inventorying agents, skills, and MCP servers and looking for agent-specific
risks. Its own setup also proves the point: scanning an MCP configuration may
start server commands, and remote analysis sends component information to a
provider. We need to understand the scanner's permissions and data path too.

## Place the remaining tools

Once we name the problems, we can place the rest of the original tool list:

- HolmesGPT and K8sGPT collect operational evidence that a model can explain.
- PR-Agent handles model review at the pull-request boundary. Semgrep MCP
  connects deterministic scanning to an agent.
- Agent Scan inventories the agent extension supply chain.
- LiteLLM adds a gateway for model routing, keys, budgets, and logs when many
  apps or providers need one policy.
- Ollama runs models locally when data placement requires it.
- garak tests LLM applications themselves, which isn't the problem in our
  Snake Royale app.

A local model doesn't automatically make the workflow private because the
host, network and prompt history still matter. So do local logs, endpoint
authentication and model quality. A gateway centralizes model access policy,
but it doesn't make a weak incident process reliable.

For this module, I would mention LiteLLM and Ollama after the adapter works. We
can point the same interface at a gateway or local endpoint later without
changing how we collect evidence, grant permission or verify recovery.

## Fit it into 90 minutes

We can't teach the full observability and security landscape in one session.

I would teach one complete path:

- 0–10 minutes - break the deployed app and identify the questions we can't
  answer
- 10–30 minutes - instrument one FastAPI request and follow its metric, trace,
  log and deployment version
- 30–45 minutes - create and test one sustained error-rate alert
- 45–70 minutes - run the read-only responder, check policy, roll back and
  verify recovery
- 70–87 minutes - run one deterministic scan and one model review, then
  validate one finding
- 87–90 minutes - reconstruct the incident from the audit record

If we extend the session to two hours, I would spend the extra time on the
ambiguous incident and the capability table. A second live model review is
less important than seeing why the first responder must stop.

## Next steps after this module

After this module, we have a narrow operating baseline. We can observe one
important user journey, respond to one known failure and audit one class of
security finding. I wouldn't add every production practice in one batch. I
would extend the system in four stages.

![After the first observable and auditable response, continue with reliability,
safer delivery, deeper security and agent governance.](images/04-next-steps-roadmap.png)

Start with reliability by defining a service-level indicator (SLI) for an
important user journey such as score submission, then set a service-level
objective (SLO). Replace the demo threshold with an error-budget burn-rate
alert. Add an external synthetic check so we notice when the app or the
monitoring path stops responding.

Next, make deployments safer with a canary or progressive rollout. Put risky
changes behind feature flags, and keep the previous release ready for rollback.
Test database backups by restoring one because a backup we have never restored
is only a promise.

Then broaden the security evidence by scanning dependencies, secrets,
containers and infrastructure code. Generate an SBOM, record build provenance
and add manual penetration testing for authorization and business-logic paths.
Define how the team receives and handles vulnerability reports.

Raise agent autonomy last by keeping the capability table current, testing model
upgrades against known incidents and measuring which audit findings people
accept or reject. Add budgets, provider-retention rules and monitoring for the
responder. Give the agent another automatic action only after incident records
show that the action is repetitive, bounded and independently verifiable.

If I could add only one thing after this module, I would start with the SLI and
SLO for the app's most important user journey. They tell us which failures
matter before we add more dashboards, alerts or agents.

## Next in the series

With these pieces, we can see a failure and investigate it. We respond within
a fixed policy, then audit the code and the responder.

In the final module, we apply this way of working to a project of your own. We
take it from an empty folder to something running and maintained.

You can find the course materials and the next cohort in
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp).
It's free.

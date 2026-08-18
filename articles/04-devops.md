# DevOps and Observability for an AI-Built App

This is the forth article in a series based on AI Dev Tools Zoomcamp, the free course we run at DataTalks.Club.

All articles in the series:

- Part 1: [AI-Native Development: Specifications, Loop and Graph Engineering](https://alexeyondata.substack.com/p/ai-native-development-specifications)
- Part 2: [Build and Ship a Full-Stack App with AI Coding Assistants](https://alexeyondata.substack.com/p/ai-native-development-specifications)
- Part 3: [Deploy a Full-Stack App with AI Coding Assistants](https://alexeyondata.substack.com/p/ai-native-development-specifications)
- Part 4: DevOps and Observability for an AI-Built App (this article)
- Part 5: TBA

In part 2, we developed an end-to-end application for conducting system design interviews. In part 3, we deployed it to AWS.

In this part, we will take the application we deployed previously, and make it more production-ready:

- Define dev and prod environments
- Introduce observability: logs, metrics, alerts
- Use AI as the first responder when the application stops working


**This article is a draft and will be updated after the workshop**


## Overview

Right now, every push to `main` goes straight to the one environment we have,
and nothing tells us the app is unhealthy until we notice by hand. We fix that
in three steps: separate dev from prod so a bad change never reaches users
directly, add the telemetry and alerting that would have caught last part's
failure on its own, and give an agent a narrow, auditable way to respond.

## Dev and prod environments

So far, a push to `main` deploys straight to the only environment we have.
That's fine for a demo, but it means every change - tested or not - reaches
the same instance our users hit.

We want a place to deploy to first, and a
deliberate, separate step to promote a change from there to production.

We already have infrastructure as code for our deployment from the previous
part, and it already parameterizes what differs between environments, such as
the domain and the instance size. That means we don't design anything new -
we ask for a second, independent copy of what we already have, and treat what
we already have as dev from now on.

```text
Create a second, independent copy of our deployment infrastructure for a
production environment.

It must be able to run alongside the existing one with its own database and compute. The existing becomes the dev environment.
```

Once prod exists, split the deploy step in CI/CD so each environment gets its
own path:

```text
Split our CI/CD deploy step into two:

Deploy to dev: on every push to main, after tests pass, deploy to the dev
environment automatically (we already do it today)

Deploy to prod: a manual workflow that promotes the version running in dev to prod.
```

The key property is that prod never builds from source on its own - it
redeploys the exact commit that already proved itself in dev. Promotion is a
deliberate, logged action, not a side effect of pushing code.



## Instrumenting 

Two environments buy us a safe place to promote from, but not visibility. A
bad deploy can still sit in prod for hours before anyone notices, because
nothing yet tells us the app is unhealthy. And even once we notice, "error
rate went up" isn't enough - we need to get from that to one failed request,
its log, and the commit that served it. A dashboard that only shows CPU and
memory can look perfectly fine while the one thing users care about is
silently failing. That's what we fix next.


We use [OpenTelemetry](https://opentelemetry.io/docs/) for this: a
vendor-neutral format for traces, metrics, and logs. A metric tells us the
canvas-broadcast error rate went up; a trace shows one failed request's path
through the backend; a log holds the exception. Tagging all three with the
same service name, environment, and deployed commit is what lets us walk from
a spike on a chart to the one request, and the one log line, behind it.

We ask the coding assistant to instrument one important operation first:

```text
Instrument the FastAPI backend with OpenTelemetry.

Export traces and metrics with OTLP (no collector yet). Include service name, environment and deployed git commit
```

The app sends OTLP to an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/),
which exports it to whichever backends we pick.

Exporting straight
from the app to each backend instead would mean an application change every
time a backend changes, and a slow backend could stall the app's own
exporters. The collector is one stable boundary that handles batching and
retries outside the request path.


```text
Add OTLP collector.

Create the observability/ directory with Docker Compose for an OpenTelemetry
Collector, Prometheus, Loki, Tempo, and Grafana.
```

## Build the dashboard

The collector is running, but nothing draws it yet. We ask for one panel - the
one the rest of this article leans on:

```text
Add one Grafana panel: canvas-broadcast error rate, with exemplars enabled so
a point links to its trace.
```

## Look at it locally first

Before shipping anywhere, we run the stack next to the app on our own machine
and generate one real trace, so we know the prompt above actually worked
before going looking for it in dev or prod:

```sh
docker compose -f observability/docker-compose.yaml up -d
```

Then we hit the app a few times so there's something to see, and open Grafana
at `http://localhost:3000` - no tunnel needed here, since nothing on a laptop
is public in the first place. Once the panel we just asked for shows real
numbers, it's safe to ship.

## Run it in dev and prod, and reach it privately

A demo dashboard on a laptop can't tell us about a real failure, so this stack
needs to run next to the app in every environment. We deploy it the same way as
everything else - push to main, dev picks it up automatically, then a
promotion ships it to prod:

```text
Deploy the observability/ stack alongside the app, in every environment.
```

## Follow one failed request

Let's break the app:

```text
Introduce a bug that makes canvas broadcasts fail for a fraction of calls.
```

Same pipeline as before: main, then dev, then a promotion to prod. Then we use
the app normally until one edit fails.

With that one failure in hand, we open the dashboard and answer these, in
order, by moving between panels rather than guessing:

1. Did users receive errors? - the canvas-broadcast error-rate panel moved.
2. Which operation failed? - that's the panel that moved; the metric is
   already labeled by operation.
3. Can we open one representative request? - click an exemplar on that panel
   to jump straight to one trace.
4. Which log belongs to that request? - the trace carries a trace ID; look it
   up in Loki.
5. Which deployment served it? - the trace and the log both carry the
   deployed commit as an attribute.

A dashboard that can't answer these - even a good-looking one - hasn't
instrumented the incident we actually care about.


## Create one actionable alert

We don't import a large alert pack - just one alert for a sustained increase in
failed canvas broadcasts, requiring both:

- enough requests failed to affect users
- the failure lasted long enough that one brief blip doesn't page anyone

This follows the [Prometheus alerting guidance](https://prometheus.io/docs/practices/alerting/):
keep alerts few, tolerate small blips, and page on symptoms that need action.
CPU, memory and connection counts still belong on the dashboard - they help
explain an incident, they just don't need to wake anyone up on their own.

We ask the assistant for the rule and its test together:

```text
Create a Prometheus alert for a sustained canvas-broadcast error rate.
```

## Wake the on-call engineer

Everything from here lives in one folder in the app repo, `on-call-engineer/`.
Rather than stand up something to receive a webhook, we poll: a script checks
Prometheus's alert API on an interval and starts the on-call agent the moment
our alert shows up firing.

```text
Add an on-call-engineer/ folder with a script that polls Prometheus's
/api/v1/alerts every minute.
```

For this proof of concept, that script runs from a cron job on our own
machine. Nothing needs to be reachable from the internet for this to work -
the script reaches out to Prometheus, not the other way around.

A cron job on a laptop only works while someone remembers to leave it
running, though. The production version of the same idea is a scheduled
serverless function - an AWS Lambda on an EventBridge schedule, a Cloud Run
job on Cloud Scheduler, or your platform's equivalent - firing the identical
poll script every minute. Nothing runs between checks: the platform starts
the function, it polls, and if the alert isn't firing it exits and gets torn
down immediately. That's a stronger version of "provisioned only when
needed" than standing up a box on alert, since even the polling itself costs
nothing while the app is healthy. We don't build that here, but the poll
script doesn't change to get there - only what's calling it on a timer.

## Let it investigate and fix

The agent isn't handed a pre-built evidence bundle - it collects its own,
with read access to exactly the systems it needs: Prometheus, Loki, Tempo,
and `git log`. And it's allowed to do more than look: edit code in a fresh
checkout, run the test suite, and push a fix if it has one.

```text
You are the on-call agent for one production alert: {alert.json}

You have read access to Prometheus, Loki, Tempo, and git log. Investigate
first - write your evidence and reasoning to incidents/<timestamp>/, and
don't call something the root cause unless the evidence rules out the main
alternatives.

If you find a fix you're confident in, make it on a fresh branch, run the
test suite, and push only if it passes. If you're not confident, or nothing
you tried passes, don't push - write an escalation instead (see below).
```

## Keep it tool-agnostic

The wake script invokes a command with four inputs - task, read access to the
evidence sources, an output schema, resource limits - and expects one
structured response back, through an interface that doesn't mention a model
vendor.

With Codex, the wake script can call
[`codex exec`](https://learn.chatgpt.com/docs/non-interactive-mode.md):

```bash
mkdir -p incidents/2026-08-02T10-30-00Z

timeout 20m codex exec \
  --sandbox workspace-write \
  --ephemeral \
  --output-schema on-call-engineer/response.schema.json \
  --output-last-message incidents/2026-08-02T10-30-00Z/response.json \
  -C . \
  - < on-call-engineer/agent-task.md
```

With Claude Code, it uses [print mode](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
with a fresh git worktree as its only writable path:

```bash
mkdir -p incidents/2026-08-02T10-30-00Z

set -o pipefail
timeout 20m claude -p \
  --permission-mode acceptEdits \
  --add-dir ./worktree \
  --no-session-persistence \
  --output-format json \
  --json-schema "$(jq -c . on-call-engineer/response.schema.json)" \
  < on-call-engineer/agent-task.md \
  | jq -e '.structured_output' \
  > incidents/2026-08-02T10-30-00Z/response.json
```

Claude's JSON output carries extra timing and session metadata, so the wake
script extracts `structured_output` to give both commands the same shape. The
flags will change; the interface - one task, scoped access, a timeout, an
audit record - doesn't have to.

[HolmesGPT](https://github.com/HolmesGPT/holmesgpt) and
[K8sGPT](https://github.com/k8sgpt-ai/k8sgpt) connect an agent to live
observability sources at larger scale. Our on-call engineer shows the same
design without making Kubernetes or one agent platform a prerequisite.

## Cap the blast radius instead of trusting the confidence

An agent can be 95% confident and still be wrong, so we don't rely on its
confidence - we rely on where a fix can land. A pushed branch only reaches
`main`, which only reaches dev automatically: the same pipeline from "Dev and
prod environments." Prod still needs a person to promote it. That's what
makes it safe to let the agent write code unsupervised at all - the worst a
bad fix does on its own is fail CI or sit untouched in dev.

A few things stay off-limits regardless of confidence, and go to a person
instead:

- anything touching auth, secrets, or a database migration
- more than one push attempt per incident
- a failure it can't reproduce, or a fix its own tests don't confirm
- conflicting evidence, or an outage broader than one operation

[SRE practitioners](https://www.reddit.com/r/sre/comments/1t6wqux/anyone_using_ai_for_actual_sreoncall_operations/)
report the same split in practice: agents collect evidence and draft fixes
well, but reliable root-cause analysis stays hard when context is missing,
and write access raises the blast radius. [Google's SRE book](https://sre.google/sre-book/automation-at-google/)
frames automation the same way - a force multiplier, not a substitute for
judgment. We automate the case we can specify and test, not every incident.

## Escalate with a useful report

"I couldn't fix it" isn't an escalation report. When nothing it tried passes,
the agent instead writes what users are experiencing, the evidence behind it,
the active deployment and recent changes, the hypotheses already checked,
what was attempted, the current state, what's still unknown, and the safest
next action for a person.

One prepared incident can demonstrate both branches: when the evidence points
to a small, well-tested fix, it pushes to dev and the wake script's next run
confirms the error rate falls; make the failure ambiguous instead, or touch a
data-integrity question, and the same agent has to escalate. It didn't get
less capable in the second run - the evidence didn't clear the bar.

## Fit it into 90 minutes

One complete path, not the full landscape:

- 0–10 minutes - break the deployed app and identify the questions we can't
  answer
- 10–25 minutes - split CI/CD into dev and prod, and manually promote one
  commit from dev to prod
- 25–45 minutes - instrument one FastAPI request and follow its metric, trace,
  log and deployment version
- 45–60 minutes - create and test one sustained error-rate alert
- 60–85 minutes - wake the on-call agent, let it investigate, push a fix to
  dev, and verify the error rate falls
- 85–90 minutes - reconstruct the incident from the audit record

If we extend the session to two hours, we'd spend the extra time on a
second, more ambiguous incident where the agent has to escalate instead of
push.

## Next steps after this module

After this module we have a narrow operating baseline: promote a change
deliberately, observe one important user journey, respond to one known
failure. We'd extend it in four stages rather than add every practice at once.

![After the first observable and auditable response, continue with reliability,
safer delivery, deeper security and agent governance.](images/04-next-steps-roadmap.png)

Start with reliability: an SLI/SLO for an important journey like canvas sync,
an error-budget burn-rate alert instead of the demo threshold, and an external
synthetic check so we notice when the app or the monitoring path itself goes
down.

Then make deployments safer - canaries or progressive rollout, risky changes
behind feature flags, the previous release always ready for rollback - and
actually restore a database backup once, since an untested backup is only a
promise.

Then broaden the security evidence: scan dependencies, secrets, containers and
infrastructure code, generate an SBOM and build provenance, and add manual
penetration testing plus a clear path for vulnerability reports.

Raise agent autonomy last. Keep a written record of what the on-call agent
can read and write and what enforces each limit, test model upgrades against
past incidents, and only widen its blast radius once incident records show
the narrower version is repetitive, bounded and independently verifiable.

If we could add only one thing, it's the SLI/SLO for the app's most important
journey - it tells us which failures matter before we add more dashboards,
alerts or agents.

## Next in the series

With these pieces, we can promote a change deliberately, see a failure and
investigate it, and let an agent fix it within a blast radius we already
trust.

In the final module, we apply this way of working to a project of your own -
from an empty folder to something running and maintained.

You can find the course materials and the next cohort in
[AI Dev Tools Zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp).
It's free.

# Homework 4: DevOps and Observability for AI-Built Apps

In this homework, you'll investigate a failure in [Order Tracker](https://github.com/alexeygrigorev/order-tracker), a small app for creating orders and checking their status. The starter has a web page, API, tests, and a Docker Compose setup.

Fork the starter on GitHub, then clone your fork. You'll add observability and an incident responder that reacts to an alert without you starting it manually. It should deploy a verified fix when policy permits, or save an escalation packet. Ask your coding agent to help with the implementation, but check each result yourself.

You need Docker with Compose and Python with `uv` for the tests. The starter's README explains how to run it. No cloud deployment account or Kubernetes cluster is required.

## Question 1: Run the app

Start Order Tracker:

```bash
docker compose up --build -d --wait
```

Now check it:

```bash
curl http://localhost:8000/healthz
```

What does the health check return?

- `{"status":"ok"}`
- `{"status":"error"}`
- `{"orders":3}`
- `pong`

For this and the next questions, you can ask your coding assistant to help select the correct option.

## Question 2: Instrument one endpoint

Imagine a customer says they cannot open an order. You check the website and everything looks okay. We need a better way to undestand what's happening in the system. For that we use metrics, logs and traces.

Ask your agent to add OpenTelemetry metrics, logs, and traces for order lookups. The request metric should include the route and HTTP status code.
For now, export the signals to the console so you can inspect them with `docker compose logs app`.

After the agent's changes, rebuild the app with `docker compose up --build -d --wait`.

Then lookup the order `standard-1001`:

```bash
curl -i http://localhost:8000/api/orders/standard-1001
```

Find the request metric in the app logs.

Which HTTP status code does the metric record for this lookup?

- 200
- 301
- 404
- 500

## Question 3: Build the telemetry pipeline

In Question 2, you needed to see the telemetry in app's standard output. But that's not how we usually do it - we want to save them somewhere. You need a way to search logs, inspect traces, and see error counts over time in one place.

Ask your agent to add an OpenTelemetry Collector, Prometheus, Loki, Tempo, and Grafana to Docker Compose. Send the app's metrics, logs, and traces through the Collector, and create a Grafana dashboard for request counts and errors. Save the configuration in your repository.

Rebuild the stack with `docker compose up --build -d --wait`, then run:

```bash
curl -i http://localhost:8000/api/orders/standard-1002
```

In Grafana, find the request metric for this lookup. Check that its log and trace also appear. Which HTTP status code does the metric show?

- 404
- 200
- 301
- 500

## Question 4: Configure the alert

The dashboard helps when you are watching it. An alert should notify the responder when order lookups start returning server errors.

Ask your agent to add a Grafana alert for order lookup `5xx` responses. Include the endpoint, time window, and dashboard link in the alert, and handle periods with no `5xx` responses. Prepare a webhook contact point, but keep delivery disabled until Question 6.

Run the lookup from Question 3 again:

```bash
curl -i http://localhost:8000/api/orders/standard-1002
```

Wait for the alert to evaluate. What state does Grafana show?

- Normal
- Firing
- Pending
- No data

## Question 5: Build the automatic responder

An alert can tell you something is wrong, but it cannot investigate or safely deploy a fix on its own. The responder will collect evidence, ask a coding agent to investigate, and use a policy to decide what happens next.

Ask your agent to build a webhook receiver under `incident-response/`. For each new incident, it should save a bounded evidence packet with the running image ID, error count, endpoint, and relevant logs or traces, using read-only, allowlisted queries. Duplicate alerts should start only one investigation. Have it launch Codex or Claude Code in headless mode with the packet and prepare a fix in an isolated worktree, without credentials for the running app or observability stack. Define `incident-response/response.schema.json` for its findings and proposed action.

Ask your agent to define `incident-response/autonomy-policy.yaml` and enforce it outside the model. Commit and deploy with `docker compose up --build -d --wait` only after allowlist checks, a regression test, and the full test suite pass. Otherwise, save an escalation packet and leave the running version alone. Run Semgrep, validate its findings, and record the responder's tools and credentials in `security-audit/capability-table.md`.

Ask your agent to add `incident-response/test-responder.sh` that sends the same sample alert twice with a fake coding agent. Run it:

```bash
bash incident-response/test-responder.sh
```

How many investigations does the responder start for the duplicate alerts?

- 1
- 0
- 2
- 3

## Question 6: Watch the agent fix the incident

Now connect the live alert to the responder and watch the full recovery path.

Ask your agent to create `incident-response/test-incident.sh`. It should check the sample orders to find a failing lookup, generate enough failures to fire the alert, and wait for one incident record, one evidence packet, and one agent run. Enable webhook delivery, then run:

```bash
bash incident-response/test-incident.sh
```

Watch the agent investigate and prepare a fix. Do not start the agent or apply the fix manually.

If policy permits the fix, watch the tests pass and Docker Compose deploy it. Repeat the failing request, confirm it works, record the new image ID, and wait for the alert to clear. If policy rejects the proposal, confirm that the running version stays in place and an escalation packet explains why. Also test the rejection path with a proposal that changes a disallowed file.

Which observation confirms that an approved fix recovered the app?

- The failing request succeeds, a new image is deployed, and the alert clears
- The model reports high confidence
- The existing tests pass without another deployment
- The app's health check stays green while the request still fails

## Submission

Write `docs/operations-and-security-report.md` for one incident ID. Include the original and deployed image IDs, user impact, alert, evidence, model and configuration, proposed action, policy decision, command run or escalation, recovery checks, and any related security finding. Link to the supporting files in your repository.

Submit your homework on the [course platform](https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4). Use the link to your repository. Commit and push the report, dashboard and alert configuration, incident evidence, responder policy, end-to-end test, and security audit.

## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public". Read more about why it matters here: https://datatalks.club/blog/benefits-of-learning-in-public.html

Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

### Example post for LinkedIn:

```
🚀 Week 4 of AI Dev Tools Zoomcamp by @DataTalksClub complete!

I investigated a failed Order Tracker release and recovered the app.

Today I learned how to:

✅ Instrument an app with OpenTelemetry: metrics, logs, traces
✅ View the signals together in Grafana
✅ Alert on real user impact, not CPU graphs
✅ Trigger a headless coding agent from an alert
✅ Deploy a checked fix or escalate automatically

Here's my repo: <LINK>

Following along with this amazing course - who else is automating ops with AI?

You can sign up here: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```

### Example post for Twitter/X:

```
🤖 Made Order Tracker observable and tested an incident response loop!

📈 Metrics, logs, traces
🔔 Alerts on real user impact
🕵️ Agent investigates, policy authorizes
✅ Fix and verify, or escalate

My repo: <LINK>

The model may reason. The system must observe, authorize, verify, and remember.

Join me: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```

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

In Question 2, you found telemetry in the app's console output. As more requests arrive, you need a way to search logs, inspect traces, and see error counts over time in one place.

Ask your agent to add an OpenTelemetry Collector, Prometheus, Loki, Tempo, and Grafana to Docker Compose. Send the app's metrics, logs, and traces through the Collector, and create a Grafana dashboard for request counts and errors. Save the configuration in your repository.

Rebuild the stack with `docker compose up --build -d --wait`, then run:

```bash
curl -i http://localhost:8000/api/orders/missing
```

In Grafana, find this `404` request in the metrics, then find its log entry and trace. Which field in the log lets you locate the trace for the same request?

- Trace ID
- Container name
- Order status
- HTTP method

## Question 4: Configure the alert

Add an alert for order lookup `5xx` responses. Include the affected endpoint, time window, and dashboard link in its payload. Check the alert query against a failing lookup.

Prepare a webhook contact point for the responder you will build next. Keep webhook delivery disabled until Question 6, when the responder is ready and you can observe the full sequence.

What should wake the responder?

- The firing alert's webhook
- Every incoming order request
- A successful Docker Compose build
- Opening the Grafana dashboard

## Question 5: Build the automatic responder

Add a webhook receiver under `incident-response/`. For each new incident, it should first save a bounded evidence packet: the running container's image ID, the error count and affected endpoint, and relevant logs or traces. Use only read-only, allowlisted queries. Repeated alerts for the same incident should start one investigation.

Have the receiver launch Codex or Claude Code in headless mode with that packet. Define `incident-response/response.schema.json` for the likely cause, supporting evidence, and one proposed action. Let the agent prepare a fix in an isolated worktree, without credentials for the running app or observability stack.

Define `incident-response/autonomy-policy.yaml` and enforce it with code outside the model. A change may be committed and deployed with `docker compose up --build -d --wait` only if its files and commands are allowlisted and a regression test and the full test suite pass. Otherwise, save an escalation packet and leave the running version alone. Run Semgrep, validate its findings, and record the responder's tools and credentials in `security-audit/capability-table.md`.

What authorizes an automatic deployment?

- The policy checks and tests pass
- The model reports high confidence
- The alert has high severity
- The agent proposes any code change

## Question 6: Watch the agent fix the incident

Create `incident-response/test-incident.sh` to check the status of the sample orders and find a failing request. Enable webhook delivery, then use the script to generate enough failures to fire the alert. Have it wait for one incident record, one evidence packet, and one agent run. Watch the agent investigate and prepare a fix. Do not start the agent or apply the fix manually.

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

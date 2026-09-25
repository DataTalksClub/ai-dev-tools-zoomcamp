# Homework 4: DevOps and Observability for AI-Built Apps

In this homework, you'll investigate a failure in [Order Tracker](https://github.com/alexeygrigorev/order-tracker), a small app for creating orders and checking their status. The starter has a web page, API, tests, and a local CI/CD workflow.

Fork the starter on GitHub, then clone your fork. You'll add observability and an incident responder that reacts to an alert without you starting it manually. It should deploy a verified fix when policy permits, or save an escalation packet. Ask your coding agent to help with the implementation, but check each result yourself.

You need Docker with Compose, Python with `uv`, and `act` for the local deployment workflow. The starter's README explains how to run it. No cloud deployment account or Kubernetes cluster is required.

## Question 1: Find the failing request

Run the starter's tests and deploy it locally with the included `act` workflow. Open the web page and check the status of each sample order. Use your browser's Network tab or the API to inspect the request that fails. The tests and `/healthz` still pass.

What HTTP status does the failing order lookup return?

- `200`
- `404`
- `422`
- `500`

For this and the next questions, you can ask your coding assistant to help select the correct option.

## Question 2: Connect metrics, logs, and traces

Ask your agent to instrument the order lookup endpoint with OpenTelemetry. Record request counts by status, create traces, and write structured logs with a trace ID. Keep customer details and credentials out of telemetry.

Add an OpenTelemetry Collector that sends metrics to Prometheus, logs to Loki, and traces to Tempo. Run these tools with Docker Compose and view them in Grafana. Make a successful and a failing lookup, then find both in the telemetry.

Which value lets you connect a failed log entry to its request trace?

- Trace ID
- Container name
- Order status
- HTTP method

## Question 3: Trigger an alert

Create a Grafana dashboard for order lookups and failed requests, with links to relevant logs and traces. Save the dashboard in your repository. Add an alert for order lookup `5xx` responses with the affected endpoint and dashboard link in its payload. Configure a webhook contact point that sends the firing alert to a local responder.

Generate enough failed lookups to fire the alert. What should start the responder?

- The firing alert's webhook
- Every incoming order request
- A successful CI build
- Opening the Grafana dashboard

## Question 4: Collect evidence before calling the model

Add a webhook receiver under `incident-response/`. When it receives an alert, it should assign an incident ID and collect a bounded evidence packet before launching the model. Include the deployed commit from `/version`, the error count and affected endpoint, and relevant logs or traces from a short time window. Use only read-only, allowlisted queries.

Send the same alert twice. Confirm that it produces one incident record and starts only one investigation.

Which evidence identifies the exact code running when the alert fired?

- The commit reported by `/version`
- The time the container started
- The number of orders in SQLite
- The name of the Grafana dashboard

## Question 5: Fix or escalate automatically

Have the webhook receiver launch Codex or Claude Code in headless mode with the saved evidence. Define `incident-response/response.schema.json` for a structured response with the likely cause, supporting evidence, and one proposed action. Let the agent prepare a fix in an isolated worktree, without credentials for the running app or observability stack.

Define `incident-response/autonomy-policy.yaml` and enforce it with code outside the model. The runner may commit and deploy a fix only when the changed files and commands are allowlisted, a regression test covers the failing request, and the local CI workflow passes. After deployment, verify that the request works and the alert clears. Otherwise, keep the running version and save an escalation packet with the reason.

Which result permits automatic deployment?

- The policy checks and tests pass
- The model reports high confidence
- The alert has high severity
- The agent proposes any code change

## Question 6: Verify the full loop

Create `incident-response/test-incident.sh` to test the loop from the original failing version. It should generate enough failed requests to fire the alert, wait for one incident record and one responder run, then check for either a verified deployment or an escalation packet. Run it without starting the agent or applying a fix manually.

Also feed the policy runner a proposal that changes a disallowed file. Confirm that it does not deploy. Run Semgrep, validate its findings yourself, and list the responder's tools, credentials, and allowed actions in `security-audit/capability-table.md`.

Write `docs/operations-and-security-report.md` for one incident ID. Include the deployed version, user impact, alert, evidence, model and configuration, proposed action, policy decision, command run or escalation, recovery checks, and any related security finding. Link to the supporting files in your repository.

What should happen when the policy rejects a proposal?

- Keep the running version and save an escalation packet
- Deploy the proposal and report the policy failure
- Delete the running container
- Ask the model to approve its own proposal

## Submission

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

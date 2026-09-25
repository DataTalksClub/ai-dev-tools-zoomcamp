# Homework 4: DevOps and Observability for AI-Built Apps

In this homework, you'll investigate a failure in [Order Tracker](https://github.com/alexeygrigorev/order-tracker), a small app for creating orders and checking their status. The starter has a web page, API, tests, and a local CI/CD workflow.

Fork the starter on GitHub, then clone your fork. You'll add observability and an incident responder that reacts to an alert without you starting it manually. It should deploy a verified fix when policy permits, or save an escalation packet. Ask your coding agent to help with the implementation, but check each result yourself.

You need Docker with Compose, Python with `uv`, and `act` for the local deployment workflow. The starter's README explains how to run it. No cloud deployment account or Kubernetes cluster is required.

## Question 1: Run, test, and record the baseline

Run the starter's tests and deploy it locally with the included `act` workflow. Open the web page and check the status of each sample order. Use your browser's Network tab or the API to inspect the requests.

Write `docs/baseline.md` with the test result, the deployed commit from `/version`, the health check result, and the request and response for any order that does not work. Save the request so you can repeat it later. Do not fix the app yet.

Which result should your baseline report record?

- The existing tests pass, but one order lookup returns `500`
- The existing tests fail before the app starts
- The health check returns `500` for every request
- Every sample order lookup returns `200`

For this and the next questions, you can ask your coding assistant to help select the correct option.

## Question 2: Add metrics

Ask your agent to instrument the order lookup endpoint with OpenTelemetry. Record request counts by status code and endpoint. Send metrics through an OpenTelemetry Collector to Prometheus, and view them in Grafana.

Repeat the request saved in Question 1. Confirm that the request counter increases for the affected endpoint and `5xx` status.

Which metric best shows the failure affecting users?

- The count of `5xx` order lookup responses
- The total number of containers started
- The app container's disk size
- The number of commits in the repository

## Question 3: Add logs, traces, and a dashboard

Add structured logs with a trace ID and OpenTelemetry traces for order lookups. Send logs to Loki and traces to Tempo. Keep customer details and credentials out of both.

Create a Grafana dashboard for request volume and errors, with links to relevant logs and traces. Save its configuration in your repository. Repeat the saved request and locate its metric, log entry, and trace.

Which value connects a failed log entry to its request trace?

- Trace ID
- Container name
- Order status
- HTTP method

## Question 4: Configure the alert

Add an alert for order lookup `5xx` responses. Include the affected endpoint, time window, and dashboard link in its payload. Check the alert query against the request saved in Question 1.

Prepare a webhook contact point for the responder you will build next. Keep webhook delivery disabled until Question 6, when the responder is ready and you can observe the full sequence.

What should wake the responder?

- The firing alert's webhook
- Every incoming order request
- A successful CI build
- Opening the Grafana dashboard

## Question 5: Build the automatic responder

Add a webhook receiver under `incident-response/`. For each new incident, it should first save a bounded evidence packet: the deployed commit from `/version`, the error count and affected endpoint, and relevant logs or traces. Use only read-only, allowlisted queries. Repeated alerts for the same incident should start one investigation.

Have the receiver launch Codex or Claude Code in headless mode with that packet. Define `incident-response/response.schema.json` for the likely cause, supporting evidence, and one proposed action. Let the agent prepare a fix in an isolated worktree, without credentials for the running app or observability stack.

Define `incident-response/autonomy-policy.yaml` and enforce it with code outside the model. A change may be committed and deployed only if its files and commands are allowlisted, a regression test covers the failing request, and the local CI workflow passes. Otherwise, save an escalation packet and leave the running version alone. Run Semgrep, validate its findings, and record the responder's tools and credentials in `security-audit/capability-table.md`.

What authorizes an automatic deployment?

- The policy checks and tests pass
- The model reports high confidence
- The alert has high severity
- The agent proposes any code change

## Question 6: Watch the agent fix the incident

Create `incident-response/test-incident.sh` to replay the request from Question 1. Enable webhook delivery, then run the script to generate enough failures to fire the alert. Have it wait for one incident record, one evidence packet, and one agent run. Watch the agent investigate and prepare a fix. Do not start the agent or apply the fix manually.

If policy permits the fix, watch the local workflow run tests and deploy it. Repeat the saved request, confirm it works, check that `/version` changed, and wait for the alert to clear. If policy rejects the proposal, confirm that the running version stays in place and an escalation packet explains why. Also test the rejection path with a proposal that changes a disallowed file.

Which observation confirms that an approved fix recovered the app?

- The saved request succeeds, a new version is deployed, and the alert clears
- The model reports high confidence
- The existing tests pass without another deployment
- The app's health check stays green while the request still fails

## Submission

Write `docs/operations-and-security-report.md` for one incident ID. Include the baseline and deployed versions, user impact, alert, evidence, model and configuration, proposed action, policy decision, command run or escalation, recovery checks, and any related security finding. Link to the supporting files in your repository.

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

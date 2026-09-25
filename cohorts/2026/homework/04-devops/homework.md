# Homework 4: DevOps and Observability for AI-Built Apps

In this homework, you'll investigate a failure in [Order Tracker](https://github.com/alexeygrigorev/order-tracker), a small app for creating orders and checking their status. The starter has a web page, API, tests, and a local CI/CD workflow.

Fork the starter on GitHub, then clone your fork. You'll add observability and an incident responder that reacts to an alert without you starting it manually. It should deploy a verified fix when policy permits, or save an escalation packet. Ask your coding agent to help with the implementation, but check each result yourself.

You need Docker with Compose, Python with `uv`, and `act` for the local deployment workflow. The starter's README explains how to run it. No cloud deployment account or Kubernetes cluster is required.

## Question 1: Run the starter

Start Order Tracker and open its web page. Create an order and check its status. Run the tests, then use the included `act` workflow to build and deploy a release locally. Check `/version` to confirm which commit is running.

Where does the starter store its orders when Docker Compose recreates the app container?

- In a Docker volume
- In the browser
- In the container's temporary files
- In the GitHub Actions log

For this and the next questions, you can ask your coding assistant to help select the correct option.

## Question 2: Instrument the app

Ask your agent to instrument the order lookup endpoint with OpenTelemetry. Record request counts and errors, create traces, and write structured logs with a request or trace ID. Keep customer details and credentials out of telemetry.

Add an OpenTelemetry Collector that sends metrics to Prometheus, logs to Loki, and traces to Tempo. Use Docker Compose to run these tools alongside Order Tracker. Check that a status lookup produces all three signals.

Which three signals are you collecting?

- Metrics, logs, and traces
- Tests, builds, and deploys
- CPU, RAM, and disk
- Requests, responses, and cookies

## Question 3: Create a dashboard and alert

Create a Grafana dashboard for order lookups, failed requests, logs, and traces. Save its configuration in your repository. Add one alert for failed order lookups that includes the affected endpoint and a link to the dashboard. Configure a webhook contact point so the alert can start a local responder.

Open the dashboard and check a successful order lookup. What should the alert represent?

- Real user impact, with context to start investigating
- Any CPU usage above 80%
- Every log line the app produces
- Each new deployment

## Question 4: Find the failing request and collect evidence

Check the status of the sample orders on the deployed app. One request fails even though the existing tests and health check pass. Confirm that your dashboard shows the error and your alert fires.

Add a small webhook receiver under `incident-response/`. When it receives an alert, it should assign an incident ID and automatically save an evidence packet: the deployed commit, error rate, affected endpoint, and relevant logs or traces. Limit collection to read-only queries and a short time window. Make repeated alerts for the same incident reuse the packet rather than starting duplicate responders.

How should the responder collect evidence?

- With read-only, allowlisted queries
- With full production admin credentials
- By trial and error on the production database
- It doesn't — the model decides what to look at

## Question 5: Automate the response

Have the webhook receiver launch Codex or Claude Code in headless mode with the saved evidence. Ask it for the likely cause, supporting evidence, and one proposed action in a structured response. Let it prepare a fix in an isolated worktree, without giving it credentials for the running app or observability stack.

Implement a policy runner outside the model. Permit an automatic deployment only when the change stays within allowlisted files and commands and includes a regression test for the failing request. Commit the permitted change, then run the local workflow so tests must pass before deployment. Check that the request works and the alert clears. If any check fails, leave the running version alone and save an escalation packet with the evidence, proposal, and reason for stopping.

What authorizes an action proposed by the responder?

- The autonomy policy and allowlists — code outside the model
- The model's confidence score
- The severity field of the alert
- Nothing — the responder acts on its own

## Question 6: Test the full loop and audit it

Create `incident-response/test-incident.sh` to test the loop from the original failing version. It should generate enough failed requests to fire the alert, wait for one incident record and one responder run, then check for either a verified deployment or an escalation packet. Run it without starting the agent or applying a fix manually. Also test one proposal that the policy rejects and confirm that it does not deploy.

Run Semgrep on your repository and review its findings with your agent. Validate the findings yourself. List the responder's tools, credentials, and allowed actions, and remove access it doesn't need.

Write `docs/operations-and-security-report.md` for one incident ID. Include the deployed version, user impact, alert, evidence, model and configuration, proposed action, policy decision, command run or escalation, recovery checks, and any related security finding. Link to the supporting files in your repository.

Which deterministic scanner did you pair with model review?

- Semgrep
- Pytest
- Playwright
- Terraform

## Submission

Submit your homework on the [course platform](https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4). Use the link to your repository. Commit and push the report, dashboard and alert configuration, incident evidence, responder policy, and security audit.

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

# Homework 4: DevOps and Observability for AI-Built Apps

In this homework, you'll investigate a failure in [Order Tracker](https://github.com/alexeygrigorev/order-tracker), a small app for creating orders and checking their status. The starter has a web page, API, tests, and a Docker Compose setup.

Fork the starter on GitHub, then clone your fork. You'll add observability and an incident responder that reacts to an alert. Ask your coding agent to help with the implementation, but check each result yourself.

You need Docker with Compose and Python with `uv` for the tests. The starter's README explains how to run it.

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

In Question 2, we looked at the logs to see the telemetry. Let's now save it into a proper telemetry storage.

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

The dashboard shows errors when you open it, but it does not notify anyone on its own. An alert watches the `5xx` metric and changes state when server errors occur. Later, Grafana will send an HTTP request called a webhook to the responder so it can start investigating automatically.

Ask your agent to add a Grafana alert for `5xx` responses. Include the endpoint, time window, and dashboard link in the alert, and handle periods with no `5xx` responses. For now, check the alert's state in Grafana. You will connect it to the responder in Question 6.

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

When an alert fires, the on-call engineer needs to look into it and solve it. If they cannot do it, they escalate it to developers.

In our case, we'll have an agent that's doing exactly that.

Ask your coding assistant to build a service in `incident-response/` that receives alerts from Grafana at `POST /alerts` on port `8001`. When an alert arrives, it should save the running app's image ID, the number of errors, the affected endpoint, and useful logs or traces.

The service should start the coding assistant automatically in headless mode to review the problem. The agent should explain what the evidence shows and either propose a fix in a worktree or say why no code change is justified. Save its response with the evidence.

Start the responder. Send a test alert about the `404` order lookups you saw in Question 3 directly to its endpoint:

```bash
curl -X POST http://localhost:8001/alerts \
  -H 'Content-Type: application/json' \
  -d '{"alerts":[{"status":"firing","labels":{"alertname":"OrderLookup404","endpoint":"/api/orders/{id}","status_code":"404"}}]}'
```

Wait for the agent to finish, then read its saved response. This test does not deploy a fix.

What action did the agent recommend for the `404` alert, and what evidence did it cite? Include the paths to the saved evidence and response.

## Question 6: Watch the agent fix the incident

Now test the complete flow with a real Grafana alert. Imagine a customer trying to open order `express-1002`. Something goes wrong with this lookup, even though `/healthz` still reports that the app is healthy.

Start the responder and connect the Grafana alert to it through a webhook. Ask your coding assistant to make the responder run the tests before it deploys an agent's fix with Docker Compose. If the tests fail, it should leave the running app in place and record why it could not deploy.

Record the current image ID with `docker compose images -q app`. Then make the same request the customer made:

```bash
curl -i http://localhost:8000/api/orders/express-1002
```

Repeat the request until the alert fires. Watch Grafana send the webhook to `/alerts`, the responder collect evidence, and the coding agent start automatically. Do not call `/alerts` yourself, start the agent, or fix the code manually.

After the responder deploys the fix, run the same `curl` command and `docker compose images -q app` again. Check the response and the alert state in Grafana. What shows that the customer's problem is fixed?

- The failing request succeeds, a new image is deployed, and the alert clears
- The model reports high confidence
- The existing tests pass without another deployment
- The app's health check stays green while the request still fails

## Submission

Submit your homework on the [course platform](https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4). Use the link to your repository. Commit and push your telemetry and alert configuration, responder, incident evidence, and agent's fix.

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

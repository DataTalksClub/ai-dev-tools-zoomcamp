# Homework 4: DevOps and Observability for AI-Built Apps

Homework 3 got your app deployed. This homework makes sure you know whether it still works.

If an important endpoint starts returning `500`, you need to know that users are affected, find the failed requests, connect them to the deployment that caused them, and decide what to do. CI/CD ships a bad release as efficiently as a good one.

This homework builds the loop that closes that gap:

```text
change
→ observe user impact
→ alert with context
→ investigate from evidence
→ authorize a bounded response or escalate
→ verify recovery
→ audit the code and the response trail
```

We also put an agent inside that loop as the first line of support. It collects the same evidence you would collect, compares it with recent changes, and proposes an action. What it does not get is general production credentials. A model supplies confidence; code outside the model enforces permission.

Keep using the coding agent from the previous homework — this week also in headless mode. You will need Docker for the telemetry stack.

Prerequisite: the deployed app from Homework 3.

## Homework Idea

Break your own app on purpose, then run the full loop: instrument it, catch the breakage with an alert, let a headless agent investigate from evidence, authorize or escalate a bounded response, and verify the recovery.

The deliverable is an operations and security report: given one incident ID, a reader should be able to reconstruct the deployed version, the user impact, the evidence, the model's proposal, the policy decision, and the recovery.

## Question 1: Instrumentation

First, find what you can't answer about a broken deployment — CPU graphs alone don't count as observability. Ask your agent to instrument the backend with OpenTelemetry: metrics, traces, and structured logs, without leaking secrets.

Which three signals does observability rest on in this module?

- Metrics, logs, and traces
- Tests, builds, and deploys
- CPU, RAM, and disk
- Requests, responses, and cookies

For this and next questions you can ask your coding assistant to select the correct option.

## Question 2: The telemetry pipeline

Wire up the pipeline: an OpenTelemetry Collector feeding Prometheus, Loki, and Tempo, viewed together in Grafana.

Which project provides the vendor-neutral instrumentation standard we use?

- OpenTelemetry
- OpenAPI
- OAuth
- OpenSSL

## Question 3: Dashboards

Which tool do we use to view metrics, logs, and traces together?

- Grafana
- pgAdmin
- Excel
- VS Code

## Question 4: Alerts

Now write one alert that represents real user impact — not high CPU — and carries enough context in its payload to act on.

A good alert represents:

- Real user impact, with context to start investigating
- Any CPU usage above 80%
- Every log line the app produces
- Each new deployment

## Question 5: Evidence first

Before any model gets involved, collect a bounded, repeatable evidence packet: recent deploys, error rates, affected endpoints, logs — with read-only, allowlisted queries only.

How does the responder collect evidence?

- With read-only, allowlisted queries
- With full production admin credentials
- By trial and error on the production database
- It doesn't — the model decides what to look at

## Question 6: The agent responder

Now run a headless coding agent (Codex or Claude Code) as a read-only first responder. Give it the evidence packet and a structured task:

```text
Here is the evidence packet for incident <ID>.
Compare it with recent changes, find the most likely
root cause, and propose one action.
You have read-only access. Respond in the JSON schema.
```

What authorizes the action the responder proposes?

- The autonomy policy and allowlists — code outside the model
- The model's confidence score
- The severity field of the alert
- Nothing — the responder acts on its own

## Question 7: Security audit

Finally, audit the code and the responder itself: run a deterministic scanner, add model review, and validate the findings yourself. Also inventory the responder's capabilities and credentials.

Which deterministic scanner do we pair with model review in the security audit?

- Semgrep
- Pytest
- Playwright
- Terraform

## Question 8: Incident report

Put it all together in `docs/operations-and-security-report.md`. Given one incident ID, the report should let a reader reconstruct:

- the deployed version and the user impact
- the alert and the evidence inspected
- the model and configuration used, and the action proposed
- the policy decision and the command actually executed
- the recovery verification, or the escalation packet

Describe one incident you ran through this loop: what was the user impact, what did the responder propose, and what did you authorize?

## Submission

Submit your homework here: https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4

Use the link to your repository in the homework submission form — it should contain the report with the observability, incident-response, and security-audit folders from the module deliverables.

Don't forget to commit your code at every step.

## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public". Read more about why it matters here: https://aishippingblog.com/p/benefits-of-learning-in-public

Learning in public is one of the most effective ways to accelerate your growth. Here's why:

1. Accountability: Sharing your progress creates commitment and motivation to continue
2. Feedback: The community can provide valuable suggestions and corrections
3. Networking: You'll connect with like-minded people and potential collaborators
4. Documentation: Your posts become a learning journal you can reference later
5. Opportunities: Employers and clients often discover talent through public learning

Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

### Example post for LinkedIn:

```
🚀 Week 4 of AI Dev Tools Zoomcamp by @DataTalksClub complete!

My app now tells me when it's broken — and an AI agent helps me fix it!

Today I learned how to:

✅ Instrument an app with OpenTelemetry: metrics, logs, traces
✅ Build a telemetry pipeline with Grafana
✅ Alert on real user impact, not CPU graphs
✅ Run a headless coding agent as a read-only first responder
✅ Gate automated actions behind allowlists and autonomy levels

Here's my repo: <LINK>

Following along with this amazing course - who else is automating ops with AI?

You can sign up here: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```

### Example post for Twitter/X:

```
🤖 Made my app observable and gave an AI agent on-call duties!

📈 Metrics, logs, traces
🔔 Alerts on real user impact
🕵️ Agent investigates, policy authorizes
✅ Human verifies the recovery

My repo: <LINK>

The model may reason. The system must observe, authorize, verify, and remember.

Join me: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/
```

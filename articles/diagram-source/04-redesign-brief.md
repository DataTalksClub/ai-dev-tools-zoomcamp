# Article 4 diagram redesign brief

The accepted `04-devops-overview` and `04-build-once` diagrams establish the
delivery model. The remaining figures need distinct visual jobs rather than
more linear workflows.

## Observability: a layered system

Show that metrics, logs, and traces travel through one collector with shared
service, environment, and deployed-version context. Put the three signals in a
single correlated-telemetry boundary, then split into two independent
consumers: dashboards for investigation and alert rules for detecting user
impact. The five-second lesson is that dashboards do not generate alerts.

## Operations: a bounded agent response

Replace the busy response loop with one entry path and one fork:

`Alert -> Evidence packet -> Investigate`

- Reproducible bug -> smallest tested fix -> normal CI/CD
- No safe fix -> explain or escalate without changing code

Keep one obvious entry point, one fork, zero crossings, and no production node.
The five-second lesson is that the agent does not fix production directly.

## Next steps: operational foundations for autonomy

Replace the roadmap chain with a readiness stack. The current operating
baseline is the foundation. Reliability, safer delivery, and security evidence
are three peer supports. Agent governance is the cap and wider authority comes
last. The five-second lesson is that autonomy rests on independent operational
evidence; it is not simply the next feature.

## Visual constraints

- Prefer layers, containment, a single fork, or physical stacking over chains.
- Use one obvious entry point and a five-second reading path.
- Minimize simultaneous branches, colors, and connector crossings.
- Delete a figure if its replacement cannot add a relationship the prose does
  not already communicate.

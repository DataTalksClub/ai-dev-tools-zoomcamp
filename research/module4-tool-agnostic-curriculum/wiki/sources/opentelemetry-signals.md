# OpenTelemetry Signals

Locator: https://opentelemetry.io/docs/concepts/signals/

Summary: Operational claims should be grounded in observable system signals rather than an agent's narrative alone.

- [FACT opentelemetry-signals] OpenTelemetry identifies traces, metrics, and logs as complementary system signals; baggage provides contextual information across signals.
- [FACT opentelemetry-signals] Traces represent request paths, metrics represent runtime measurements, and logs record events.
- [INFERENCE opentelemetry-signals] A vendor-neutral diagnosis lab can give an agent a prepared evidence bundle containing these signals plus changes, configuration, and runbooks.

Limitations: OpenTelemetry defines telemetry, not a complete incident investigation method.

Related: [operational investigation](../concepts/operational-investigation.md)

Accessed: 2026-08-02. Page modified: 2026-03-10.

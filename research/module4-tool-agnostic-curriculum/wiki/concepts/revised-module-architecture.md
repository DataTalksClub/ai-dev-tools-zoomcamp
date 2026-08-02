# Revised module architecture

## System path

```text
React + FastAPI + Postgres from Module 2
                 |
       OpenTelemetry instrumentation
                 |
        OpenTelemetry Collector
          /          |          \
 Prometheus       Loki         Tempo
   metrics        logs         traces
          \          |          /
                  Grafana
             dashboards + alerts
                       |
              incident orchestrator
                       |
          sandboxed first-line coding agent
             /                       \
 known safe runbook             human escalation
       |                        + evidence packet
 verify recovery
```

- [HUMAN] The subject is the Module 2 application and deployment pipeline.
- [INFERENCE observability-pipeline] The application emits standard telemetry to one collector endpoint; storage and visualization remain replaceable.
- [INFERENCE alerting-sre] Dashboards expose traffic, errors, latency, saturation, health, and recent deployment context; alerts focus on sustained user-visible symptoms.
- [INFERENCE safe-remediation] The agent begins read-only, collects evidence, and may cross into mutation only through an eligible pre-approved runbook.
- [INFERENCE safe-remediation,nist-incident-response] Every response ends in recovery verification or a human-ready escalation and produces an audit record.

## Recommended teaching stack

- [INFERENCE observability-pipeline,alerting-sre] **Core:** OpenTelemetry SDK/auto-instrumentation, upstream OpenTelemetry Collector, Prometheus, Loki, Tempo, Grafana, Alertmanager-compatible webhook, one terminal coding agent.
- [FACT observability-pipeline,alerting-sre] **Why Loki and Tempo:** metrics can tell learners that the system is unhealthy; correlated logs and traces help explain which request and component failed.
- [INFERENCE observability-pipeline] **Why the upstream Collector:** it teaches the standard boundary and avoids binding instrumentation to Grafana-specific collection syntax. Grafana Alloy can be a production comparison.
- [FACT observability-pipeline] **Scope choice:** instrument the FastAPI backend for traces and metrics and correlate structured stdout logs in the core lab. Browser tracing is optional because current OpenTelemetry browser instrumentation is experimental.

## Minimal alerts

1. Public health/availability check fails for a sustained interval.
2. User-visible 5xx/error rate is elevated.
3. p95 request latency is elevated.
4. Optional: saturation such as DB connection or host/container resource pressure.
5. Metamonitoring: the telemetry/alert path itself stops working. [INFERENCE alerting-sre]

These alerts should be deliberately triggered through prepared failure scenarios, not left as decorative YAML.

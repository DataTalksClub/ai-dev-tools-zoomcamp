# Prometheus and Google SRE alerting guidance

Primary locators:

- [FACT alerting-sre] https://prometheus.io/docs/practices/alerting/
- [FACT alerting-sre] https://prometheus.io/docs/alerting/latest/alertmanager/
- [FACT alerting-sre] https://sre.google/sre-book/monitoring-distributed-systems/
- [FACT alerting-sre] https://sre.google/sre-book/effective-troubleshooting/

Summary: Alerts should represent actionable user symptoms, while dashboards and correlated telemetry preserve the detail needed to find causes.

- [FACT alerting-sre] Prometheus guidance recommends few alerts, symptom-based conditions, tolerance for brief blips, and pages only when action is required.
- [FACT alerting-sre] For online services, user-visible error rate and latency are primary alert candidates.
- [FACT alerting-sre] Alertmanager groups, deduplicates, routes, silences, and inhibits alerts so one underlying incident does not create an alert storm.
- [FACT alerting-sre] Google SRE uses traffic, errors, latency, and saturation as four golden signals and recommends simple, robust paging rules.
- [FACT alerting-sre] Monitoring should itself be monitored, ideally with an external black-box check that exercises the alert path.
- [FACT alerting-sre] Effective troubleshooting combines system knowledge with metrics, logs, traces, configuration, and timeline correlation.
- [INFERENCE alerting-sre] An alert sent to an agent should contain symptom, severity, service, start time, dashboard/trace links, recent deployment, and runbook—not merely a threshold name.

Limitations: SLO burn-rate alerting is an important production extension but may be too much machinery for the first lab; simple sustained error/latency/availability alerts can establish the concept.

Related: [agent escalation policy](../concepts/agent-escalation-policy.md)

Accessed: 2026-08-02. Individual pages are continuously maintained.

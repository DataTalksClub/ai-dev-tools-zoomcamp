# Practitioner discussions: observability and alerting

Sources:

- [FACT practitioner-observability] [Alert fatigue is killing me](https://www.reddit.com/r/sre/comments/1nm7sbi/alert_fatigue_is_killing_me/), r/sre, accessed 2026-08-02.
- [FACT practitioner-observability] Additional r/sre and r/devops discussions found during the same research pass on OpenTelemetry adoption, unused dashboards, and large self-hosted observability stacks.

Summary: The recurring practitioner problem is not absence of telemetry. It is collecting signals that nobody uses and paging on conditions that do not imply an action.

## Claims

- [FACT practitioner-observability] Participants repeatedly described non-actionable alerts as notices or dashboard material, not pages. They recommended customer-impact symptoms, clear ownership, runbooks, and regular deletion or repair of noisy alerts.
- [FACT practitioner-observability] One experienced participant described muting alerts without runbooks and filing ownership tickets; others warned that imported alert packs create floods because the most important product alerts are application-specific.
- [FACT practitioner-observability] Discussions about OpenTelemetry showed a real tradeoff: an extra collection layer adds setup and operating cost, while a standard protocol reduces direct coupling to one backend and supports gradual migration.
- [FACT practitioner-observability] Some teams reported having dashboards and log aggregation while engineers still debugged from raw console logs. This suggests that a workshop must demonstrate an incident question answered by correlated telemetry rather than treating successful installation as the outcome.

## Teaching consequence

[INFERENCE practitioner-observability,alerting-sre] Build one useful request journey and one actionable alert. Do not spend the workshop installing every dashboard or copying a large default rule pack.

## Limitations

Reddit discussions are self-selected, anecdotal, and sometimes promotional. They demonstrate vocabulary, pain, and disagreement, not prevalence or measured effectiveness. Normative recommendations should remain grounded in Prometheus, OpenTelemetry, and SRE primary guidance.

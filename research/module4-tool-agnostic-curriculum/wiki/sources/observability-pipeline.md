# OpenTelemetry and Grafana observability pipeline guidance

Primary locators:

- [FACT observability-pipeline] https://opentelemetry.io/docs/collector/deploy/
- [FACT observability-pipeline] https://opentelemetry.io/docs/languages/python/
- [FACT observability-pipeline] https://opentelemetry.io/docs/languages/js/getting-started/browser/
- [FACT observability-pipeline] https://prometheus.io/docs/guides/opentelemetry/
- [FACT observability-pipeline] https://grafana.com/docs/tempo/latest/set-up-for-tracing/
- [FACT observability-pipeline] https://grafana.com/docs/loki/latest/
- [FACT observability-pipeline] https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/

Summary: A production-oriented telemetry pipeline separates instrumentation, collection/processing, storage, and visualization and correlates signals through consistent resource attributes and trace identifiers.

- [FACT observability-pipeline] OpenTelemetry Collector supports agent and gateway deployment patterns and provides a vendor-neutral OTLP boundary between applications and backends.
- [FACT observability-pipeline] A collector/pipeline is recommended between applications and trace storage because it supplies batching, retry, and decoupling from backend availability.
- [FACT observability-pipeline] Grafana can correlate Tempo traces with Loki logs and Prometheus metrics; trace-to-log navigation requires shared identifiers such as trace IDs and service names.
- [FACT observability-pipeline] Prometheus supports OTLP metrics ingestion but disables its receiver by default because unauthenticated ingestion can be unsafe.
- [FACT observability-pipeline] Python OpenTelemetry traces and metrics are stable while its logs signal remains under development; browser instrumentation is experimental and mostly unspecified.
- [FACT observability-pipeline] Loki recommends low-cardinality labels and structured metadata for high-cardinality values such as trace IDs, request IDs, and user IDs.
- [INFERENCE observability-pipeline] For this course, backend traces and metrics plus structured stdout logs with injected trace IDs form the stable core; browser tracing is a useful optional extension.

Limitations: Grafana documentation naturally favors Grafana Alloy/Cloud. An upstream OpenTelemetry Collector is the more portable teaching baseline, while Alloy can be mentioned as a production distribution.

Related: [revised module architecture](../concepts/revised-module-architecture.md)

Accessed: 2026-08-02. Individual pages are continuously maintained.

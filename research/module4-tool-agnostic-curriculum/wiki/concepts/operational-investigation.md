# Operational investigation

- [FACT opentelemetry-signals] Logs, metrics, and traces provide different observable views of runtime behavior.
- [FACT nist-incident-response] Incident work belongs to preparation, detection, response, recovery, and continuous improvement.
- [INFERENCE opentelemetry-signals,nist-incident-response,current-module-4] The durable diagnostic loop is: define symptom and impact; assemble a timeline; inspect correlated signals and recent changes; state competing hypotheses; run a discriminating check; identify and fix the cause; verify recovery; record prevention.
- [INFERENCE tool-repositories] Kubernetes analyzers and SRE agents can accelerate collection and explanation, but they are adapters into this loop.

Suggested learner outcome: Investigate a prepared failure from raw evidence, explicitly distinguish observed facts from hypotheses, and prove recovery with a predefined health check.

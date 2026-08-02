# AI usage governance

- [FACT nist-ai-rmf] AI risk management requires defined tasks, application scope, roles, third-party dependencies, oversight, measurement, and documentation.
- [FACT nist-csf-2] Governance establishes risk strategy, expectations, roles, and policy across the cybersecurity lifecycle.
- [INFERENCE nist-ai-rmf,current-module-4] A portable governance exercise should start with policy: which identity may send which data class to which model/provider for which task, within which budget, retention, logging, and approval constraints.
- [INFERENCE tool-repositories] A gateway, local model runner, shell wrapper, CI policy, or organization platform may enforce parts of the policy; none is the concept itself.

Suggested learner outcome: Define a small policy, test allowed and denied cases, trace one request's data path, and show an audit record without leaking sensitive content.

# Change assurance

- [FACT owasp-secure-code-review] Secure change review starts with application intent, architecture, assets, threat context, and changed components—not a diff in isolation.
- [FACT owasp-secure-code-review] Automated analysis can prioritize attention, while business logic, authorization, state transitions, and control effectiveness need manual reasoning.
- [INFERENCE owasp-secure-code-review,current-module-4] A portable lab should ask any terminal agent to construct a review packet containing change intent, affected trust boundaries, high-risk files, check results, candidate findings, evidence, uncertainty, and recommended disposition.
- [INFERENCE nist-ssdf] The result should be an inspectable assurance record, not a bot comment as the end goal.

Suggested learner outcome: Given a proposed change, produce and defend a risk-based merge recommendation, identify what automated checks did and did not establish, and record follow-up work.

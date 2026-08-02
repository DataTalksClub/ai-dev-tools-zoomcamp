# Current OpenAI and Anthropic models for demanding code audit work

Primary locators:

- [FACT current-audit-models] https://developers.openai.com/api/docs/guides/latest-model
- [FACT current-audit-models] https://developers.openai.com/api/docs/models
- [FACT current-audit-models] https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
- [FACT current-audit-models] https://platform.claude.com/docs/en/manage-claude/api-and-data-retention

Summary: The user-named model families are current, but surfaces, model IDs, reasoning settings, refusals, cost, and data-retention policies must be distinguished.

- [FACT current-audit-models] OpenAI's current flagship is `gpt-5.6-sol`; `gpt-5.6` aliases to it, and reasoning effort includes `max`. “GPT-5.6 Sol Max” is therefore a model-plus-effort configuration, not a separate model ID.
- [FACT current-audit-models] OpenAI positions GPT-5.6 Sol for complex reasoning/coding and states that defensive code review, vulnerability research, patching, debugging, and security education remain supported despite cyber safeguards.
- [FACT current-audit-models] Claude Fable 5 (`claude-fable-5`) is Anthropic's most capable generally released model for demanding reasoning and long-horizon agentic work.
- [FACT current-audit-models] Claude Fable 5 includes cyber safety classifiers and may return refusals; its API use requires 30-day data retention and is not eligible for zero data retention.
- [INFERENCE current-audit-models] Sensitive proprietary code may therefore require a provider/retention decision before Fable 5 is allowed, and a fallback path should handle legitimate defensive requests that are refused.
- [INFERENCE current-audit-models] ChatGPT is an interactive product surface; if it uses GPT-5.6, it is not an independent third model for consensus. The independent reviewer comparison is better framed as OpenAI GPT-5.6 Sol versus Anthropic Claude Fable 5 (or another current Claude model).

Limitations: Model names, availability, safeguards, pricing, and retention are highly time-sensitive. They must be refreshed before the course is recorded.

Related: [recurring security audit](../concepts/recurring-security-audit.md)

Accessed: 2026-08-02.

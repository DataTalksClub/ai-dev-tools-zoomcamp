# Practitioner discussions: model gateways and local inference

Sources:

- [FACT practitioner-model-infrastructure] [LLM Proxy in Production](https://www.reddit.com/r/LLMDevs/comments/1l1n95h/llm_proxy_in_production_litellm_portkey_helicone/), r/LLMDevs, accessed 2026-08-02.
- [FACT practitioner-model-infrastructure] [Are you using AI Gateway in your GenAI stack?](https://www.reddit.com/r/LocalLLaMA/comments/1kmragz/are_you_using_ai_gateway_in_your_genai_stack/), r/LocalLLaMA, accessed 2026-08-02.
- [FACT practitioner-model-infrastructure] [Exploring User Privacy in Ollama](https://www.reddit.com/r/LocalLLaMA/comments/1idlz1x/exploring_user_privacy_in_ollama_are_local_llms/), r/LocalLLaMA, accessed 2026-08-02.
- [FACT practitioner-model-infrastructure] [Is anyone using ollama for production purposes?](https://www.reddit.com/r/ollama/comments/1knu8bm/is_anyone_using_ollama_for_production_purposes/), r/ollama, accessed 2026-08-02.

Summary: Gateways address organizational policy and operational consistency across providers. Local inference changes data placement, but does not by itself supply access control, retention policy, endpoint security, capacity, or adequate model quality.

## Claims

- [FACT practitioner-model-infrastructure] Gateway discussions identify provider abstraction, authentication, budgets, rate limits, fallback, caching, observability, evaluation, and data residency as production concerns.
- [FACT practitioner-model-infrastructure] Participants disagree on when a gateway justifies another operating layer; the need becomes clearer with multiple providers, applications, identities, or policy requirements than in a one-user workshop.
- [FACT practitioner-model-infrastructure] Local-model discussions value on-device or on-premises processing for sensitive inputs, while raising concerns about local history/log files, endpoint exposure, authentication, concurrency, model updates, hardware cost, and output quality.
- [FACT practitioner-model-infrastructure] “Runs locally” was not treated as equivalent to “private” or “production ready.” The surrounding host, storage, network, identity, logs, and application configuration still determine exposure.

## Teaching consequence

[INFERENCE practitioner-model-infrastructure,nist-ai-rmf] LiteLLM and Ollama solve legitimate but secondary deployment-policy problems. They should appear in the extension map, not consume core workshop time. The portable interface should make either usable later.

## Limitations

The discussions are anecdotal and product versions change quickly. Product capabilities must be checked against current official documentation before implementation.

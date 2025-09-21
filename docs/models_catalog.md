# Models Catalog

This document lists commonly used models and suggested routing in this project. Routing is controlled by environment variables in `.env`.

- OpenAI-compatible (Chat/Responses API): routed via `OPENAI_API_BASE`
- Anthropic Claude (native Messages API): routed via `CLAUDE_API_BASE`
- Gemini via OpenAI-compatible gateway: routed via `GEMINI_API_BASE`
- DeepSeek via OpenAI-compatible gateway: routed via `OPENAI_API_BASE`

See `ai_scientist/llm.py` and `ai_scientist/vlm.py` for integration.

## Environment Variables

```
OPENAI_API_BASE=https://api.openai-proxy.org/v1
OPENAI_API_KEY=...
CLAUDE_API_BASE=https://api.openai-proxy.org/anthropic
ANTHROPIC_API_KEY=...
GEMINI_API_BASE=https://api.openai-proxy.org/google
GEMINI_API_KEY=...
```

## OpenAI Family (including GPT‑5, GPT‑4.x, o-series)

- Note: GPT‑5 family is called with OpenAI Responses API first, then falls back to Chat Completions if unavailable. See `get_response_from_llm()` and `get_batch_responses_from_llm()` in `ai_scientist/llm.py`.

| Model | Type | Notes |
|---|---|---|
| gpt-5 | chat | Responses API preferred |
| gpt-5-2025-08-07 | chat | Responses API preferred |
| gpt-5-chat-latest | chat | Responses API preferred |
| gpt-5-mini | chat | Responses API preferred |
| gpt-5-mini-2025-08-07 | chat | Responses API preferred |
| gpt-5-nano | chat | Responses API preferred |
| gpt-5-nano-2025-08-07 | chat | Responses API preferred |
| gpt-4.1, gpt-4.1-mini, gpt-4.1-2025-04-14 | chat | Chat Completions |
| gpt-4o, gpt-4o-2024-05-13/08-06/11-20 | chat | Chat Completions |
| gpt-4o-mini, gpt-4o-mini-2024-07-18 | chat | Chat Completions |
| gpt-4o(-audio|search)-preview-* | chat | Chat Completions |
| chatgpt-4o-latest | chat | Chat Completions |
| gpt-4-turbo(-preview), gpt-4-1106-preview, ... | chat | Chat Completions |
| gpt-4(‑32k) variants | chat | Chat Completions |
| o1, o1-mini, o1-preview, o1-2024-12-17, ... | chat | Beta rules handled in `backend/__init__.py` |
| o3, o3-mini, o3-pro, o3-deep-research | chat | Chat Completions |
| o4-mini, o4-mini-deep-research | chat | Chat Completions |

## Anthropic Claude (Native Messages API)

- Routed via `anthropic.Anthropic` with optional `CLAUDE_API_BASE`.

| Model | Type | Notes |
|---|---|---|
| claude-opus-4-1-20250805 | chat | Newer Opus |
| claude-opus-4-0 | chat | Added to `AVAILABLE_LLMS` |
| claude-opus-4-20250514 | chat |  |
| claude-sonnet-4-0 | chat | Added to `AVAILABLE_LLMS` |
| claude-sonnet-4-20250514 | chat |  |
| claude-3-7-sonnet-20250219 | chat |  |
| claude-3-7-sonnet-latest | chat | Added to `AVAILABLE_LLMS` |
| claude-3-5-sonnet-20241022 | chat |  |
| claude-3-5-sonnet-20240620 | chat |  |
| claude-3-5-haiku-20241022 | chat |  |
| claude-3-5-haiku-latest | chat |  |
| claude-3-opus-20240229 | chat |  |
| claude-3-opus-latest | chat |  |
| claude-3-sonnet-20240229 | chat |  |
| claude-3-haiku-20240307 | chat |  |

## Gemini via OpenAI-compatible Gateway

- Implemented via `openai.OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_API_BASE)`.

| Model | Type |
|---|---|
| gemini-2.5-pro | chat |
| gemini-2.5-pro-preview-* | chat |
| gemini-2.5-flash | chat |
| gemini-2.5-flash-preview-* | chat |
| gemini-2.5-flash-lite, -lite-preview-* | chat |
| gemini-2.0-flash-preview-image-generation | chat |

## DeepSeek via OpenAI-compatible Gateway

- DeepSeek models are routed through `OPENAI_API_BASE` using the OpenAI client.

| Model | Type |
|---|---|
| deepseek-chat | chat |
| deepseek-reasoner | chat |
| deepseek-coder-v2-0724 | chat (integrated) |

## Notes on Rate Limits and Pricing

- The rate limits (RPM) and pricing listed in your source are not enforced by this codebase. They are determined by the provider behind your gateways. Use external monitoring/billing tools to track usage and costs.

## Where Models Are Registered

- `ai_scientist/llm.py`: `AVAILABLE_LLMS` controls argparse choices in various CLI scripts and provides routing logic.
- `ai_scientist/vlm.py`: vision-capable OpenAI models list.
- `ai_scientist/treesearch/backend/backend_anthropic.py`: sends Claude requests via Anthropic Messages API.
- `ai_scientist/treesearch/backend/__init__.py`: routes Claude/OpenAI backends and handles o1 beta rules.

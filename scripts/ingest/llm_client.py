"""Minimax-via-Anthropic structured-output client (copy of the battle-tested
version from the old Anti-OS tree, with the dotenv path rebased).

The only caller is `extract.py` (Phase C). Everything else is a `.env` read:

    ANTHROPIC_API_KEY   (required)
    ANTHROPIC_BASE_URL  (default https://api.minimaxi.com/anthropic)
    LLM_MODEL           (default MiniMax-M2.7-highspeed)

Retries (3x) + aggressive JSON recovery are kept as-is.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Type

from pydantic import BaseModel

try:
    from dotenv import load_dotenv

    # Rebase to agent-wiki/.env (this module lives at scripts/ingest/llm_client.py).
    # override=True so repo-local .env wins over ambient shell env (some users
    # have a global ANTHROPIC_BASE_URL that would otherwise shadow Minimax).
    _REPO_ROOT = Path(__file__).resolve().parents[2]
    load_dotenv(dotenv_path=_REPO_ROOT / ".env", override=True)
except ImportError:
    pass


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_BASE_URL = os.environ.get(
    "ANTHROPIC_BASE_URL", "https://api.minimaxi.com/anthropic"
)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# OPENAI_BASE_URL lets the OpenAI client talk to any OpenAI-protocol
# endpoint: DeepSeek (https://api.deepseek.com), local vLLM/Ollama
# servers, LiteLLM proxies, etc. When unset, the default OpenAI
# endpoint is used.
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "MiniMax-M2.7-highspeed")


def _extract_text_recursive(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    if hasattr(obj, "text") and isinstance(obj.text, str):
        return obj.text
    if isinstance(obj, list):
        return "".join(_extract_text_recursive(i) for i in obj)
    if isinstance(obj, dict):
        return "".join(
            _extract_text_recursive(v)
            for k, v in obj.items()
            if k == "text" or isinstance(v, (list, dict))
        )
    if hasattr(obj, "__dict__"):
        return _extract_text_recursive(obj.__dict__)
    return ""


def _repair_tags(raw_text: str) -> str:
    """Minimax occasionally emits `"tags": "#a #b"` instead of a JSON array."""
    if '"tags": "#' not in raw_text:
        return raw_text
    return re.sub(
        r'"tags":\s*"([^"]+)"',
        lambda m: f'"tags": {json.dumps([t.strip().lstrip("#") for t in m.group(1).split() if t.strip()])}',
        raw_text,
    )


def _loose_json_extract(raw_text: str) -> str:
    m = re.search(r"(\{.*\})", raw_text, re.DOTALL)
    return m.group(1) if m else raw_text


def generate_structured_output(
    system_prompt: str,
    user_content: str,
    response_format: Type[BaseModel],
    model: str | None = None,
    # 32 768 is large enough for the full ExtractionOutput from a 30K-word
    # chunk. 4096 truncates mid-JSON on dense Chinese / multi-page chunks;
    # L6 smoke showed classical-Chinese chunks dropping all pages due to
    # mid-list EOF. Minimax M2.7-highspeed's 256K context leaves generous
    # room even with this higher cap.
    max_tokens: int = 32_768,
    temperature: float = 0.2,
) -> tuple[BaseModel | None, dict]:
    """Returns (parsed_model_or_None, usage_dict).

    `usage_dict` carries {'tokens_in': int, 'tokens_out': int, 'model': str,
    'attempts': int} for cost tracking.
    """
    model = model or DEFAULT_MODEL
    usage: dict = {"tokens_in": 0, "tokens_out": 0, "model": model, "attempts": 0}

    max_retries = 3
    for attempt in range(max_retries):
        usage["attempts"] = attempt + 1

        if ANTHROPIC_API_KEY:
            try:
                import anthropic

                client = anthropic.Anthropic(
                    api_key=ANTHROPIC_API_KEY, base_url=ANTHROPIC_BASE_URL
                )
                schema_json = json.dumps(
                    response_format.model_json_schema(), indent=2
                )
                full_user = (
                    f"{user_content}\n\n"
                    f"IMPORTANT: return a valid JSON object matching:\n"
                    f"{schema_json}\n"
                    f"Return ONLY the JSON, no other text."
                )
                # Use streaming for large outputs. Anthropic SDK rejects
                # non-streaming when max_tokens × expected_rate > 10 min.
                if max_tokens > 12_000:
                    with client.messages.stream(
                        model=model,
                        max_tokens=max_tokens,
                        system=system_prompt,
                        messages=[{"role": "user", "content": full_user}],
                        temperature=temperature,
                    ) as stream:
                        raw_text = stream.get_final_text()
                        final_msg = stream.get_final_message()
                    try:
                        usage["tokens_in"] = int(
                            getattr(final_msg.usage, "input_tokens", 0) or 0
                        )
                        usage["tokens_out"] = int(
                            getattr(final_msg.usage, "output_tokens", 0) or 0
                        )
                    except Exception:
                        pass
                else:
                    response = client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        system=system_prompt,
                        messages=[{"role": "user", "content": full_user}],
                        temperature=temperature,
                    )
                    try:
                        usage["tokens_in"] = int(
                            getattr(response.usage, "input_tokens", 0) or 0
                        )
                        usage["tokens_out"] = int(
                            getattr(response.usage, "output_tokens", 0) or 0
                        )
                    except Exception:
                        pass

                    raw_text = _extract_text_recursive(response.content)
                if not raw_text:
                    if attempt < max_retries - 1:
                        continue
                    return None, usage

                raw_text = _loose_json_extract(raw_text)
                raw_text = _repair_tags(raw_text)
                try:
                    return response_format.model_validate_json(raw_text), usage
                except Exception as e:
                    if attempt < max_retries - 1:
                        continue
                    print(
                        f"[llm_client] final JSON parse error: {e}\nraw[:300]={raw_text[:300]}"
                    )
                    return None, usage
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                print(f"[llm_client] final anthropic call error: {e}")
                return None, usage

        elif OPENAI_API_KEY:
            try:
                from openai import OpenAI

                client_kwargs = {"api_key": OPENAI_API_KEY}
                if OPENAI_BASE_URL:
                    client_kwargs["base_url"] = OPENAI_BASE_URL
                client = OpenAI(**client_kwargs)

                # Native structured-output for GPT-4o / gpt-4.1 family.
                # DeepSeek, vLLM, etc. don't implement this — fall through
                # to JSON-mode below.
                if model.startswith("gpt-") and not OPENAI_BASE_URL:
                    response = client.beta.chat.completions.parse(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content},
                        ],
                        response_format=response_format,
                        temperature=temperature,
                    )
                    try:
                        usage["tokens_in"] = int(
                            getattr(response.usage, "prompt_tokens", 0) or 0
                        )
                        usage["tokens_out"] = int(
                            getattr(response.usage, "completion_tokens", 0) or 0
                        )
                    except Exception:
                        pass
                    return response.choices[0].message.parsed, usage

                # Generic OpenAI-compatible JSON-mode path. Works with
                # DeepSeek (deepseek-chat / deepseek-reasoner), vLLM,
                # Ollama, LiteLLM proxies.
                schema_json = json.dumps(
                    response_format.model_json_schema(), indent=2
                )
                full = (
                    f"{user_content}\n\n"
                    f"IMPORTANT: return a valid JSON object matching:\n"
                    f"{schema_json}\n"
                    f"Return ONLY the JSON, no other text."
                )
                # Try response_format=json_object first; if the model
                # rejects it (unsupported), retry without the flag.
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": full},
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        response_format={"type": "json_object"},
                    )
                except Exception:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": full},
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                try:
                    usage["tokens_in"] = int(
                        getattr(response.usage, "prompt_tokens", 0) or 0
                    )
                    usage["tokens_out"] = int(
                        getattr(response.usage, "completion_tokens", 0) or 0
                    )
                except Exception:
                    pass

                raw_text = response.choices[0].message.content or ""
                if not raw_text:
                    if attempt < max_retries - 1:
                        continue
                    return None, usage
                raw_text = _loose_json_extract(raw_text)
                raw_text = _repair_tags(raw_text)
                try:
                    return response_format.model_validate_json(raw_text), usage
                except Exception as e:
                    if attempt < max_retries - 1:
                        continue
                    print(
                        f"[llm_client] final JSON parse error: {e}\nraw[:300]={raw_text[:300]}"
                    )
                    return None, usage
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                print(f"[llm_client] final openai call error: {e}")
                return None, usage

        else:
            print(
                "[llm_client] No usable client. Set ONE of:\n"
                "  ANTHROPIC_API_KEY (+ optional ANTHROPIC_BASE_URL)\n"
                "    → Claude direct, or Minimax via its /anthropic shim\n"
                "  OPENAI_API_KEY (+ optional OPENAI_BASE_URL)\n"
                "    → OpenAI direct, DeepSeek (https://api.deepseek.com),\n"
                "      vLLM/Ollama proxies, LiteLLM\n"
                "See .env.example for templates, or run "
                "`python -m scripts.ingest.setup`."
            )
            return None, usage

    return None, usage

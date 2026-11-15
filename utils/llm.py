"""Configure model providers and validate their candidate-generation responses."""

import json
import os
import re
from collections.abc import Collection
from dataclasses import dataclass
from pathlib import Path

from langchain_core.messages import HumanMessage


@dataclass(frozen=True)
class ProviderConfig:
    key_environment: str
    default_model: str
    base_url: str | None


PROVIDERS = {
    "deepseek": ProviderConfig(
        key_environment="DEEPSEEK_API_KEY",
        default_model="deepseek-chat",
        base_url="https://api.deepseek.com",
    ),
    "openai": ProviderConfig(
        key_environment="OPENAI_API_KEY",
        default_model="gpt-4.1-mini",
        base_url=None,
    ),
    "qwen": ProviderConfig(
        key_environment="DASHSCOPE_API_KEY",
        default_model="qwen-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    "zhipu": ProviderConfig(
        key_environment="ZHIPUAI_API_KEY",
        default_model="glm-4-flash",
        base_url="https://open.bigmodel.cn/api/paas/v4",
    ),
}


def create_llm(provider=None, *, model=None, base_url=None):
    """Create only the selected provider, reading credentials from its environment."""
    provider = provider or os.environ.get("CONTEXT4INV_PROVIDER", "deepseek")
    model = model or os.environ.get("CONTEXT4INV_MODEL")
    if provider == "fma":
        from utils.local_model import FMAQwenChatModel

        return FMAQwenChatModel(**({"model_name": model} if model else {}))
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown model provider: {provider}")
    settings = PROVIDERS[provider]
    api_key = os.environ.get(settings.key_environment)
    if not api_key:
        raise ValueError(
            f"Set {settings.key_environment} to use the {provider} provider"
        )
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        api_key=api_key,
        model=model or settings.default_model,
        base_url=base_url
        or os.environ.get("CONTEXT4INV_BASE_URL")
        or settings.base_url,
        timeout=120,
        # request_candidates owns retries so there is one configured attempt limit.
        max_retries=0,
    )


def _parse_invariant_list(value) -> set[str]:
    if not isinstance(value, list):
        raise ValueError("Expected a list of nonempty invariant strings")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError("Expected a list of nonempty invariant strings")
    return set(value)


def _parse_named_candidates(data, allowed_keys, loop_count) -> dict[str, set[str]]:
    if not isinstance(data, dict):
        raise ValueError("Expected an object mapping names to invariant lists")
    if loop_count is not None:
        loop_names = {f"LOOP_{index}" for index in range(loop_count)}
        if not data or data.keys() - loop_names:
            raise ValueError(
                f"Expected one or more loop names from {sorted(loop_names)}"
            )
    candidates = {}
    for name, invariants in data.items():
        if allowed_keys is not None and name not in allowed_keys:
            continue
        candidates[name] = _parse_invariant_list(invariants)
    return candidates


def parse_candidates(
    content: str,
    *,
    grouped: bool = False,
    allowed_keys: Collection[str] | None = None,
    loop_count: int | None = None,
) -> set[str] | dict[str, set[str]]:
    """Read a list, variable-keyed candidates, or loop-keyed strengthening candidates."""
    content = content.strip()
    fence = re.fullmatch(
        r"```(?:json|answer)?\s*(.*?)\s*```", content, flags=re.DOTALL | re.IGNORECASE
    )
    data = json.loads(fence.group(1) if fence else content)
    if grouped:
        return _parse_named_candidates(data, allowed_keys, loop_count)
    return _parse_invariant_list(data)


def _save_transcript(history, destination, error=None) -> None:
    if destination is None:
        return
    text = "\n".join(message.pretty_repr() for message in history)
    if error is not None:
        text += f"\nRequest failed: {type(error).__name__}"
    Path(destination).write_text(text, encoding="utf-8")


def request_candidates(
    model,
    messages,
    history,
    attempts,
    *,
    grouped=False,
    allowed_keys=None,
    loop_count=None,
    transcript_path=None,
):
    """Bound API and response-format attempts, saving each response before parsing.

    Rejected JSON receives a formatting diagnostic in the next request. Transport
    failures consume an attempt but do not fabricate an assistant response.
    """
    request_messages = list(messages)
    last_error = None
    _save_transcript(history, transcript_path)
    for _ in range(attempts):
        try:
            response = model.invoke(request_messages)
        except Exception as error:
            last_error = error
            _save_transcript(history, transcript_path, error)
            continue
        history.append(response)
        _save_transcript(history, transcript_path)
        try:
            return parse_candidates(
                response.content,
                grouped=grouped,
                allowed_keys=allowed_keys,
                loop_count=loop_count,
            )
        except (ValueError, TypeError) as error:
            last_error = error
            feedback = HumanMessage(
                content=f"Invalid JSON response: {error}. Return only the required JSON structure."
            )
            request_messages.extend([response, feedback])
            history.append(feedback)
            _save_transcript(history, transcript_path)
    raise RuntimeError(
        f"Model request failed after {attempts} attempts: {last_error}"
    ) from last_error

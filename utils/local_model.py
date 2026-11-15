"""Optional local FMA model adapter, loaded only when its provider is selected."""

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import PrivateAttr
from transformers import AutoModelForCausalLM, AutoTokenizer


class FMAQwenChatModel(BaseChatModel):
    """Adapt Hugging Face text generation to LangChain's chat-model interface."""

    model_name: str = "fm-universe/qwen2.5-7b-fma"
    max_new_tokens: int = 4096
    temperature: float = 0.0
    device: str = "auto"

    _model: Any = PrivateAttr()
    _tokenizer: Any = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map=self.device,
        )

    @property
    def _llm_type(self) -> str:
        return "fma-qwen-chat"

    @staticmethod
    def _convert_messages(messages: list[BaseMessage]):
        """Map LangChain message roles to the tokenizer's chat-template roles."""
        role_map = {
            "human": "user",
            "ai": "assistant",
            "system": "system",
        }

        return [
            {
                "role": role_map.get(m.type, "user"),
                "content": m.content,
            }
            for m in messages
        ]

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate only the assistant continuation, excluding the encoded prompt."""
        model_messages = self._convert_messages(messages)

        text = self._tokenizer.apply_chat_template(
            model_messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        model_inputs = self._tokenizer(
            [text],
            return_tensors="pt",
        ).to(self._model.device)

        output_ids = self._model.generate(
            **model_inputs,
            max_new_tokens=kwargs.get("max_new_tokens", self.max_new_tokens),
            do_sample=self.temperature > 0,
            temperature=self.temperature if self.temperature > 0 else None,
        )

        generated_ids = output_ids[:, model_inputs.input_ids.shape[-1] :]

        content = self._tokenizer.batch_decode(
            generated_ids,
            skip_special_tokens=True,
        )[0].strip()

        if stop:
            for s in stop:
                idx = content.find(s)
                if idx != -1:
                    content = content[:idx]

        message = AIMessage(content=content)

        return ChatResult(generations=[ChatGeneration(message=message)])

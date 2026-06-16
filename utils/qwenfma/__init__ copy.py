from typing import Any, List, Optional
from pydantic import PrivateAttr

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class FMAQwenChatModel(BaseChatModel):
    model_name: str = "fm-universe/qwen2.5-7b-fma"
    max_new_tokens: int = 4096
    temperature: float = 0.0

    _model: Any = PrivateAttr()
    _tokenizer: Any = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,      # 如果不支持 bfloat16，改成 torch.float16
            device_map="cuda",              # 单卡优先用 cuda，别用 auto
            low_cpu_mem_usage=False,         # 关键：避免 meta tensor 残留
        )

        self._model.eval()

    @property
    def _llm_type(self) -> str:
        return "fma-qwen-chat"

    def _convert_messages(self, messages: List[BaseMessage]):
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
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        hf_messages = self._convert_messages(messages)

        text = self._tokenizer.apply_chat_template(
            hf_messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        model_inputs = self._tokenizer(
            [text],
            return_tensors="pt",
        ).to(self._model.device)

        generation_kwargs = {
            "max_new_tokens": kwargs.get("max_new_tokens", self.max_new_tokens),
            "do_sample": self.temperature > 0,
            "pad_token_id": self._tokenizer.eos_token_id,
        }

        if self.temperature > 0:
            generation_kwargs["temperature"] = self.temperature

        with torch.no_grad():
            output_ids = self._model.generate(
                **model_inputs,
                **generation_kwargs,
            )

        generated_ids = output_ids[:, model_inputs.input_ids.shape[-1]:]

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

        return ChatResult(
            generations=[
                ChatGeneration(message=message)
            ]
        )
    
from langchain_core.messages import AIMessage, HumanMessage

llm = FMAQwenChatModel()

# if __name__ == "__main__":
#     messages = [
#         AIMessage(content="Hi."),
#         HumanMessage(content="Your role is a poet. Write a short poem about AI in four lines."),
#     ]

#     response = llm.invoke(messages)
#     print(response.content)
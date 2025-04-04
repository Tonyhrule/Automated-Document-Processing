import os
from typing import Any
import json
from llama_index.core.base.llms.types import (
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core.llms.custom import CustomLLM
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Document
from cleanlab_studio import Studio
from helpers.oai import client

studio = Studio(os.environ["CLEANLAB_API_KEY"])
tlm = studio.TLM()

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


class TLMWrapper(CustomLLM):
    context_window: int = 16000
    num_output: int = 256
    model_name: str = "TLM"

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        # Prompt tlm for a response and trustworthiness score
        response = tlm.prompt(prompt)
        output = json.dumps(response)
        return CompletionResponse(text=output)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        # Prompt tlm for a response and trustworthiness score
        response = tlm.prompt(prompt)
        output = json.dumps(response)

        # Stream the output
        output_str = ""
        for token in output:
            output_str += token
            yield CompletionResponse(text=output_str, delta=token)


def tlm_query_engine(documents: list[str]):
    return VectorStoreIndex(
        [Document(text=document, metadata={"source": "tlm"}) for document in documents]
    ).as_query_engine(llm=TLMWrapper())


class LLMWrapper(CustomLLM):
    context_window: int = 128_000
    num_output: int = 256
    model_name: str = "gpt-4o-mini"

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.num_output,
        )
        output = response.choices[0].message.content

        trustworthiness = tlm.get_trustworthiness_score(prompt, output or "")

        return CompletionResponse(
            text=json.dumps(
                {
                    "response": output,
                    "trustworthiness_score": trustworthiness["trustworthiness_score"],  # type: ignore
                }
            )
        )

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.num_output,
            stream=True,
        )

        output = ""

        for token in response:
            output += token.choices[0].delta.content or ""

            yield CompletionResponse(
                text=json.dumps(
                    {
                        "response": output,
                    }
                ),
                delta=token.choices[0].delta.content or "",
            )

        trustworthiness = tlm.get_trustworthiness_score(prompt, output)

        yield CompletionResponse(
            text=json.dumps(
                {
                    "response": output,
                    "trustworthiness_score": trustworthiness["trustworthiness_score"],  # type: ignore
                }
            )
        )


def llm_query_engine(documents: list[str]):
    return VectorStoreIndex(
        [Document(text=document, metadata={"source": "tlm"}) for document in documents]
    ).as_query_engine(llm=LLMWrapper())

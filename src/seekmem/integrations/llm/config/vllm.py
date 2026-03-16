from typing import Optional

from pydantic import AliasChoices, Field

from seekmem.integrations.llm.config.base import BaseLLMConfig
from seekmem.settings import settings_config


class VllmConfig(BaseLLMConfig):
    """
    Configuration class for vLLM-specific parameters.
    Inherits from BaseLLMConfig and adds vLLM-specific settings.
    """

    _provider_name = "vllm"
    _class_path = "seekmem.integrations.llm.vllm.VllmLLM"

    model_config = settings_config("LLM_", extra="forbid", env_file=None)

    # vLLM-specific fields
    vllm_base_url: Optional[str] = Field(
        default="http://localhost:8000/v1",
        validation_alias=AliasChoices(
            "vllm_base_url",
            "VLLM_LLM_BASE_URL",
        ),
        description="vLLM base URL"
    )

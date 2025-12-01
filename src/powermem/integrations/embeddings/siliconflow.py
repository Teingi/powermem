import os
from typing import Literal, Optional

from openai import OpenAI

from powermem.integrations.embeddings.base import EmbeddingBase
from powermem.integrations.embeddings.config.base import BaseEmbedderConfig


class SiliconFlowEmbedding(EmbeddingBase):
    """
    SiliconFlow embedding provider implementation.
    
    SiliconFlow (硅基流动) is compatible with OpenAI API format.
    Base URL: https://api.siliconflow.cn/v1
    """
    
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        super().__init__(config)

        # Default model and dimensions for SiliconFlow
        self.config.model = self.config.model or "BAAI/bge-large-en-v1.5"
        # Default to 1024 to match database configuration
        self.config.embedding_dims = self.config.embedding_dims or 1024

        # SiliconFlow specific configuration
        api_key = (
            self.config.api_key 
            or os.getenv("SILICONFLOW_API_KEY") 
            or os.getenv("EMBEDDING_API_KEY")
        )
        # Default base URL for SiliconFlow
        base_url = (
            self.config.openai_base_url 
            or os.getenv("SILICONFLOW_BASE_URL") 
            or os.getenv("EMBEDDING_BASE_URL")
            or os.getenv("LLM_BASE_URL")
            or "https://api.siliconflow.cn/v1"
        )

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None):
        """
        Get the embedding for the given text using SiliconFlow.

        Args:
            text (str): The text to embed.
            memory_action (optional): The type of embedding to use. Must be one of "add", "search", or "update". Defaults to None.
        Returns:
            list: The embedding vector.
        """
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(
                input=[text], 
                model=self.config.model, 
                dimensions=self.config.embedding_dims
            )
            .data[0]
            .embedding
        )


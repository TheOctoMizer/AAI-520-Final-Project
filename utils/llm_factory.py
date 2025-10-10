"""Factory module for creating LLM instances."""
from langchain_openai import ChatOpenAI
from utils.config import LMSTUDIO_URL, LLM_NAME, ENTITY_EXTRACTOR


def create_chat_llm(temperature: float = 0.7, model_name: str = None) -> ChatOpenAI:
    """Create a standard chat LLM instance."""
    return ChatOpenAI(
        base_url=LMSTUDIO_URL,
        api_key="dummy",
        model_name=model_name or LLM_NAME,
        temperature=temperature
    )


def create_extraction_llm(temperature: float = 0) -> ChatOpenAI:
    """Create an LLM instance optimized for entity extraction."""
    return ChatOpenAI(
        base_url=LMSTUDIO_URL,
        api_key="dummy",
        model_name=ENTITY_EXTRACTOR,
        temperature=temperature
    )

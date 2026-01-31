
from crewai import LLM
from .config import get_settings

def create_llm() -> LLM:
    s = get_settings()
    return LLM(
        model=s.llm_model,
        api_key=s.llm_api_key,
        base_url=s.llm_base_url,
        temperature=s.temperature,
    )


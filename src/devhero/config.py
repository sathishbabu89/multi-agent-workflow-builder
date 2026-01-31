
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    # LLM
    llm_model: str = os.getenv("DEVZERO_LLM_MODEL", "deepseek-chat")
    llm_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    llm_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    temperature: float = float(os.getenv("DEVZERO_TEMPERATURE", "0.3"))

    # GitHub
    github_repo: str = os.getenv("GITHUB_REPO", "")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_branch: str = os.getenv("GITHUB_BRANCH", "main")

    # Cache/Storage
    cache_dir: Path = Path(os.getenv("CACHE_DIR", "repo_cache"))

def get_settings() -> Settings:
    s = Settings()
    return s

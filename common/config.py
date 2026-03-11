"""项目级配置读取。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_dotenv(dotenv_path: Path = ENV_FILE) -> None:
    """从项目根目录加载 .env，已存在的环境变量不覆盖。"""
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), _strip_quotes(value.strip()))


@dataclass(frozen=True)
class EmbeddingConfig:
    url: str
    model: str
    api_key: str
    timeout_seconds: float

    @property
    def auth_header(self) -> str:
        return f"Bearer {self.api_key}" if self.api_key else ""


load_dotenv()


def get_embedding_config() -> EmbeddingConfig:
    """读取 embedding 相关配置，默认走本地 Ollama。"""
    timeout_seconds = float(os.getenv("EMBEDDING_TIMEOUT_SECONDS", "30"))
    return EmbeddingConfig(
        url=os.getenv("EMBEDDING_URL", "http://localhost:11434/v1/embeddings"),
        model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
        api_key=os.getenv("EMBEDDING_API_KEY", "ollama"),
        timeout_seconds=timeout_seconds,
    )

import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

from common.config import get_embedding_config, load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_TMP_ROOT = PROJECT_ROOT / ".test_tmp"


@contextmanager
def local_temp_dir():
    temp_dir = TEST_TMP_ROOT / str(uuid.uuid4())
    temp_dir.mkdir(parents=True, exist_ok=True)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)



def test_load_dotenv_reads_values_from_file(monkeypatch):
    with local_temp_dir() as temp_dir:
        env_file = temp_dir / ".env"
        env_file.write_text(
            "\n".join(
                [
                    "EMBEDDING_URL=http://example.com/v1/embeddings",
                    "EMBEDDING_MODEL=test-embedding-model",
                    "EMBEDDING_API_KEY=test-secret",
                    "EMBEDDING_TIMEOUT_SECONDS=12.5",
                ]
            ),
            encoding="utf-8",
        )

        for key in (
            "EMBEDDING_URL",
            "EMBEDDING_MODEL",
            "EMBEDDING_API_KEY",
            "EMBEDDING_TIMEOUT_SECONDS",
        ):
            monkeypatch.delenv(key, raising=False)

        load_dotenv(env_file)
        config = get_embedding_config()

        assert config.url == "http://example.com/v1/embeddings"
        assert config.model == "test-embedding-model"
        assert config.api_key == "test-secret"
        assert config.timeout_seconds == 12.5
        assert config.auth_header == "Bearer test-secret"



def test_load_dotenv_does_not_override_existing_env(monkeypatch):
    with local_temp_dir() as temp_dir:
        env_file = temp_dir / ".env"
        env_file.write_text("EMBEDDING_MODEL=from-file", encoding="utf-8")
        monkeypatch.setenv("EMBEDDING_MODEL", "from-env")

        load_dotenv(env_file)

        assert get_embedding_config().model == "from-env"



def test_get_embedding_config_uses_defaults_when_env_missing(monkeypatch):
    for key in (
        "EMBEDDING_URL",
        "EMBEDDING_MODEL",
        "EMBEDDING_API_KEY",
        "EMBEDDING_TIMEOUT_SECONDS",
    ):
        monkeypatch.delenv(key, raising=False)

    config = get_embedding_config()

    assert config.url == "http://localhost:11434/v1/embeddings"
    assert config.model == "nomic-embed-text"
    assert config.api_key == "ollama"
    assert config.timeout_seconds == 30.0
    assert config.auth_header == "Bearer ollama"

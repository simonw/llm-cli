import pytest


@pytest.fixture
def log_path(tmpdir):
    return tmpdir / "logs.db"


@pytest.fixture
def keys_path(tmpdir):
    return tmpdir / "keys.json"


@pytest.fixture
def templates_path(tmpdir):
    path = tmpdir / "templates"
    path.mkdir()
    return path


@pytest.fixture(autouse=True)
def env_setup(monkeypatch, log_path, keys_path, templates_path):
    monkeypatch.setenv("LLM_KEYS_PATH", str(keys_path))
    monkeypatch.setenv("LLM_LOG_PATH", str(log_path))
    monkeypatch.setenv("LLM_TEMPLATES_PATH", str(templates_path))

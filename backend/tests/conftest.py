from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def logs_dir():
    return Path(__file__).resolve().parents[2] / "logs"

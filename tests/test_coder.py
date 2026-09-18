import pytest

from hcc_codifier import coder
from hcc_codifier.config import Settings


def test_raises_when_api_key_missing(monkeypatch):
    monkeypatch.setattr(coder, "settings", Settings(openai_api_key=None))

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        coder.extract_assessment("Chief complaint: headache.")

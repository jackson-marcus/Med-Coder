"""Fixtures: synthetic notes + stub embedder."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from make_notes import generate

import medcoder.coding.suggest as suggest_mod


class StubEmbedder:
    def embed(self, texts):
        for text in texts:
            vec = np.zeros(128, dtype=np.float32)
            for token in re.findall(r"[a-z0-9]+", str(text).lower()):
                vec[int(hashlib.md5(token.encode()).hexdigest(), 16) % 128] += 1.0
            yield vec


@pytest.fixture(scope="session")
def notes():
    return generate(n_notes=150, seed=4)


@pytest.fixture(autouse=True)
def stub_embedder(monkeypatch):
    import fastembed

    monkeypatch.setattr(fastembed, "TextEmbedding", lambda *a, **k: StubEmbedder())
    suggest_mod.invalidate()
    yield
    suggest_mod.invalidate()

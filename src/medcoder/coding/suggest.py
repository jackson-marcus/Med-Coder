"""Code suggestion: abbreviation expansion -> hybrid retrieval over ICD-10
descriptions (dense + BM25, RRF), with per-suggestion evidence."""

from __future__ import annotations

import functools
import re

import numpy as np
from rank_bm25 import BM25Okapi

from medcoder.coding.codes import ICD10, expand_abbreviations
from medcoder.settings import get_config


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


@functools.lru_cache(maxsize=1)
def _index():
    codes = list(ICD10)
    descriptions = [ICD10[c] for c in codes]
    from fastembed import TextEmbedding

    model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    dense = np.array([np.asarray(v, dtype=np.float32) for v in model.embed(descriptions)])
    dense /= np.linalg.norm(dense, axis=1, keepdims=True) + 1e-12
    bm25 = BM25Okapi([_tokenize(d) for d in descriptions])
    return codes, descriptions, dense, bm25, model


def invalidate() -> None:
    _index.cache_clear()


def suggest_codes(note: str, top_k: int | None = None) -> list[dict]:
    cfg = get_config()["retrieval"]
    top_k = top_k or cfg["top_k"]
    codes, descriptions, dense, bm25, model = _index()

    expanded = expand_abbreviations(note)
    q = np.asarray(next(iter(model.embed([expanded]))), dtype=np.float32)
    q /= np.linalg.norm(q) + 1e-12
    dense_rank = np.argsort(-(dense @ q))
    bm25_scores = np.asarray(bm25.get_scores(_tokenize(expanded)))
    bm25_rank = np.argsort(-bm25_scores)

    fused: dict[int, float] = {}
    for rank_list in (dense_rank[: cfg["candidates"]], bm25_rank[: cfg["candidates"]]):
        for rank, idx in enumerate(rank_list):
            fused[int(idx)] = fused.get(int(idx), 0.0) + 1.0 / (cfg["rrf_k"] + rank + 1)
    best = sorted(fused, key=fused.get, reverse=True)[:top_k]

    note_tokens = set(_tokenize(expanded))
    out = []
    for i in best:
        desc_tokens = set(_tokenize(descriptions[i]))
        evidence = sorted(note_tokens & desc_tokens - {"unspecified", "of", "the", "and"})
        out.append(
            {
                "code": codes[i],
                "description": descriptions[i],
                "score": round(fused[i], 5),
                "evidence_terms": evidence[:8],
            }
        )
    return out

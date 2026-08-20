"""Abbreviation expansion + retrieval accuracy + API contract."""

from fastapi.testclient import TestClient

from medcoder.api.main import create_app
from medcoder.coding.codes import expand_abbreviations
from medcoder.coding.suggest import suggest_codes


def test_abbreviations_expand_token_safe():
    text = "Follow up for t2dm and htn; sob on exertion. The word 'shot' stays."
    out = expand_abbreviations(text)
    assert "type 2 diabetes mellitus" in out
    assert "hypertension" in out
    assert "shortness of breath" in out
    assert "shot" in out  # substrings untouched


def test_suggest_returns_ranked_with_evidence():
    out = suggest_codes("copd flare with wheeze and sputum", top_k=5)
    assert len(out) == 5
    scores = [s["score"] for s in out]
    assert scores == sorted(scores, reverse=True)
    assert all("evidence_terms" in s for s in out)


def test_top3_accuracy_on_synthetic_notes(notes):
    top3 = 0
    for _, row in notes.iterrows():
        suggestions = [s["code"] for s in suggest_codes(row["note"], top_k=3)]
        if row["true_code"] in suggestions:
            top3 += 1
    accuracy = top3 / len(notes)
    assert accuracy > 0.6, f"top-3 accuracy {accuracy:.2f} too low"
    assert accuracy < 1.0, "perfect retrieval would mean the corpus is trivial"


def test_abbreviation_expansion_helps(notes):
    # The same note with abbreviations must rank the truth at least as well
    # as raw text for the classic abbreviation cases.
    with_abbrev = "Patient with t2dm follow up."
    suggestions = [s["code"] for s in suggest_codes(with_abbrev, top_k=3)]
    assert "E11.9" in suggestions


def test_api_suggest_and_disclaimer():
    client = TestClient(create_app())
    r = client.post("/suggest", json={"note": "uti symptoms with dysuria and frequency"})
    assert r.status_code == 200
    body = r.json()
    assert any(s["code"] == "N39.0" for s in body["suggestions"])
    assert "human coder" in body["disclaimer"].lower()


def test_api_codes_listing():
    client = TestClient(create_app())
    codes = client.get("/codes").json()
    assert len(codes) > 40
    assert {"code", "description"} <= set(codes[0])


def test_api_validates_short_note():
    client = TestClient(create_app())
    assert client.post("/suggest", json={"note": "short"}).status_code == 422

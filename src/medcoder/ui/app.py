"""Streamlit demo: paste a note, review suggested codes with evidence."""

from __future__ import annotations

import os

import httpx
import streamlit as st

API_URL = os.environ.get("MEDCODER_API_URL", "http://localhost:8150")

st.set_page_config(page_title="medcoder", page_icon="🏥", layout="wide")
st.title("🏥 medcoder")
st.caption("Assistive ICD-10 suggestions for professional coders — a human confirms every code")


def _ok() -> bool:
    try:
        return httpx.get(f"{API_URL}/health", timeout=3).status_code == 200
    except httpx.HTTPError:
        return False


if not _ok():
    st.error(f"API not reachable at {API_URL}. Start it with `make api`.")
    st.stop()

note = st.text_area(
    "Clinical note",
    "Follow up for t2dm, well controlled on metformin. BP elevated again; htn management discussed.",
    height=120,
)
if st.button("Suggest codes", type="primary") and len(note) >= 10:
    r = httpx.post(f"{API_URL}/suggest", json={"note": note, "top_k": 5}, timeout=120)
    if r.status_code != 200:
        st.error(r.json().get("detail", r.text))
    else:
        body = r.json()
        with st.expander("Abbreviations expanded"):
            st.markdown(body["expanded_note"])
        for s in body["suggestions"]:
            st.markdown(f"**{s['code']}** — {s['description']}")
            st.caption(f"score {s['score']} · evidence: {', '.join(s['evidence_terms']) or '—'}")
        st.info(body["disclaimer"])

"""API routes: /suggest, /codes, /health. Assistive only — coder confirms."""

from __future__ import annotations

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from medcoder.coding.codes import ICD10, expand_abbreviations
from medcoder.coding.suggest import suggest_codes

logger = logging.getLogger(__name__)
router = APIRouter()

DISCLAIMER = "Assistive suggestions for professional medical coders; not medical advice. A human coder must confirm every code."


class Note(BaseModel):
    note: str = Field(min_length=10, max_length=8000)
    top_k: int | None = Field(default=None, ge=1, le=10)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/codes")
def codes() -> list[dict]:
    return [{"code": c, "description": d} for c, d in ICD10.items()]


@router.post("/suggest")
def suggest(note: Note) -> dict:
    return {
        "expanded_note": expand_abbreviations(note.note),
        "suggestions": suggest_codes(note.note, top_k=note.top_k),
        "disclaimer": DISCLAIMER,
    }

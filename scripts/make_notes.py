"""Synthetic clinical notes with known ICD-10 ground truth.

Notes mix abbreviations, lay phrasing, and distractor context so retrieval is
honest work. Ground truth is the generating code.

Usage:
    uv run python scripts/make_notes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from medcoder.settings import get_config, resolve_path

TEMPLATES: dict[str, list[str]] = {
    "E11.9": [
        "Follow up for t2dm, well controlled on metformin.",
        "Patient with type 2 diabetes here for routine check, no complications noted.",
    ],
    "I10": [
        "BP elevated again; htn management discussed, continue lisinopril.",
        "Essential hypertension follow up, home readings reviewed.",
    ],
    "J44.1": [
        "copd flare with increased sputum and wheeze, started prednisone burst.",
        "Acute exacerbation of chronic obstructive pulmonary disease, nebs given.",
    ],
    "J45.909": [
        "Asthma stable on inhaler, no nocturnal symptoms.",
        "Mild intermittent asthma, technique reviewed.",
    ],
    "N39.0": [
        "Dysuria and frequency, urinalysis positive; treating uti with nitrofurantoin.",
        "Urinary tract infection symptoms for two days, cultures sent.",
    ],
    "K21.9": [
        "Heartburn after meals, worse lying down; gerd counseled, PPI started.",
        "Reflux symptoms persist, continue omeprazole.",
    ],
    "M54.50": [
        "lbp after lifting, no red flags, advised stretching.",
        "Low back pain one week, improving with NSAIDs.",
    ],
    "G43.909": [
        "Recurrent migraine with photophobia, triptan effective.",
        "Migraine headaches twice monthly, prophylaxis discussed.",
    ],
    "R07.9": [
        "cp on exertion resolved at rest, ECG unremarkable today.",
        "Chest pain, atypical, workup initiated.",
    ],
    "R10.9": [
        "Diffuse abd pain since yesterday, soft abdomen, observing.",
        "Abdominal pain unspecified location, labs ordered.",
    ],
    "F32.9": [
        "Low mood, anhedonia and poor sleep; mdd screening positive, starting SSRI.",
        "Major depressive disorder single episode, therapy referral placed.",
    ],
    "F41.9": [
        "Excessive worry most days, gad likely, discussed CBT options.",
        "Anxiety symptoms interfering with work, follow up in four weeks.",
    ],
    "E78.5": [
        "Lipid panel high, hld counseled on diet, statin considered.",
        "Hyperlipidemia follow up, LDL above goal.",
    ],
    "D64.9": [
        "Fatigue with pallor, hemoglobin low; anemia workup started.",
        "Anemia unspecified, iron studies pending.",
    ],
    "I48.91": [
        "Palpitations, irregularly irregular pulse; afib on ECG, rate control begun.",
        "Atrial fibrillation follow up, anticoagulation reviewed.",
    ],
    "J18.9": [
        "Productive cough with fever and crackles; cxr shows infiltrate, pneumonia treated.",
        "Community acquired pneumonia, started azithromycin.",
    ],
    "L03.90": [
        "Red warm tender lower leg, cellulitis suspected, cephalexin started.",
        "Cellulitis improving on antibiotics day three.",
    ],
    "S93.401A": [
        "Twisted right ankle on stairs, swelling laterally; sprain, RICE advised.",
        "Right ankle sprain initial visit, weight bearing as tolerated.",
    ],
    "R06.02": [
        "sob climbing stairs, lungs clear, further testing planned.",
        "Shortness of breath on exertion, oximetry normal at rest.",
    ],
    "G47.00": [
        "Cannot fall asleep most nights; insomnia, sleep hygiene reviewed.",
        "Chronic insomnia, melatonin trial discussed.",
    ],
}

DISTRACTORS = [
    "Patient works as a teacher and lives with family.",
    "No known drug allergies.",
    "Vaccinations up to date.",
    "Denies tobacco or alcohol use.",
    "Follow up scheduled in two weeks.",
]


def generate(n_notes: int, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    codes = list(TEMPLATES)
    rows = []
    for i in range(n_notes):
        code = codes[int(rng.integers(0, len(codes)))]
        note = str(rng.choice(TEMPLATES[code]))
        if rng.random() < 0.7:
            note += " " + str(rng.choice(DISTRACTORS))
        rows.append({"note_id": i + 1, "note": note, "true_code": code})
    return pd.DataFrame(rows)


def main() -> None:
    cfg = get_config()["data"]
    df = generate(cfg["n_notes"], cfg["seed"])
    out = resolve_path(cfg["processed_dir"])
    out.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out / "notes.parquet", index=False)
    print(f"Wrote {len(df)} notes over {df['true_code'].nunique()} codes -> {out}")


if __name__ == "__main__":
    main()

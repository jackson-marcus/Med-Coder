"""ICD-10-CM code subset + clinical abbreviation dictionary.

Codes and descriptions are public-domain administrative data (a curated
common-conditions subset; a real deployment loads the full CMS release file
with the same schema). This system ASSISTS coders — every suggestion requires
human confirmation.
"""

from __future__ import annotations

ICD10: dict[str, str] = {
    "E11.9": "Type 2 diabetes mellitus without complications",
    "E11.65": "Type 2 diabetes mellitus with hyperglycemia",
    "E10.9": "Type 1 diabetes mellitus without complications",
    "I10": "Essential primary hypertension",
    "I25.10": "Atherosclerotic heart disease of native coronary artery without angina pectoris",
    "I21.9": "Acute myocardial infarction unspecified",
    "I50.9": "Heart failure unspecified",
    "I48.91": "Unspecified atrial fibrillation",
    "J44.9": "Chronic obstructive pulmonary disease unspecified",
    "J44.1": "Chronic obstructive pulmonary disease with acute exacerbation",
    "J45.909": "Unspecified asthma uncomplicated",
    "J18.9": "Pneumonia unspecified organism",
    "J06.9": "Acute upper respiratory infection unspecified",
    "J02.9": "Acute pharyngitis unspecified",
    "N39.0": "Urinary tract infection site not specified",
    "N18.3": "Chronic kidney disease stage 3 unspecified",
    "K21.9": "Gastro-esophageal reflux disease without esophagitis",
    "K52.9": "Noninfective gastroenteritis and colitis unspecified",
    "K80.20": "Calculus of gallbladder without cholecystitis without obstruction",
    "M54.50": "Low back pain unspecified",
    "M54.2": "Cervicalgia",
    "M17.9": "Osteoarthritis of knee unspecified",
    "M19.90": "Unspecified osteoarthritis unspecified site",
    "M79.10": "Myalgia unspecified site",
    "G43.909": "Migraine unspecified not intractable without status migrainosus",
    "G40.909": "Epilepsy unspecified not intractable without status epilepticus",
    "R51.9": "Headache unspecified",
    "R07.9": "Chest pain unspecified",
    "R10.9": "Unspecified abdominal pain",
    "R05.9": "Cough unspecified",
    "R50.9": "Fever unspecified",
    "R53.83": "Other fatigue",
    "R42": "Dizziness and giddiness",
    "R06.02": "Shortness of breath",
    "F32.9": "Major depressive disorder single episode unspecified",
    "F41.9": "Anxiety disorder unspecified",
    "F41.0": "Panic disorder without agoraphobia",
    "G47.00": "Insomnia unspecified",
    "E78.5": "Hyperlipidemia unspecified",
    "E66.9": "Obesity unspecified",
    "E03.9": "Hypothyroidism unspecified",
    "E05.90": "Thyrotoxicosis unspecified without thyrotoxic crisis",
    "D64.9": "Anemia unspecified",
    "D50.9": "Iron deficiency anemia unspecified",
    "L03.90": "Cellulitis unspecified",
    "L30.9": "Dermatitis unspecified",
    "H66.90": "Otitis media unspecified unspecified ear",
    "H10.9": "Unspecified conjunctivitis",
    "S93.401A": "Sprain of unspecified ligament of right ankle initial encounter",
    "S52.501A": "Unspecified fracture of the lower end of right radius initial encounter",
    "T78.40XA": "Allergy unspecified initial encounter",
    "Z23": "Encounter for immunization",
    "O26.90": "Pregnancy related conditions unspecified unspecified trimester",
    "B34.9": "Viral infection unspecified",
    "A09": "Infectious gastroenteritis and colitis unspecified",
}

ABBREVIATIONS: dict[str, str] = {
    "t2dm": "type 2 diabetes mellitus",
    "dm2": "type 2 diabetes mellitus",
    "t1dm": "type 1 diabetes mellitus",
    "htn": "hypertension",
    "cad": "coronary artery disease atherosclerotic heart disease",
    "mi": "myocardial infarction",
    "chf": "heart failure",
    "afib": "atrial fibrillation",
    "copd": "chronic obstructive pulmonary disease",
    "uri": "upper respiratory infection",
    "uti": "urinary tract infection",
    "ckd": "chronic kidney disease",
    "gerd": "gastro esophageal reflux disease",
    "lbp": "low back pain",
    "oa": "osteoarthritis",
    "ha": "headache",
    "sob": "shortness of breath",
    "cp": "chest pain",
    "mdd": "major depressive disorder",
    "gad": "anxiety disorder",
    "hld": "hyperlipidemia",
    "fx": "fracture",
    "abd": "abdominal",
    "n/v": "nausea vomiting gastroenteritis",
}


def expand_abbreviations(text: str) -> str:
    """Expand known clinical abbreviations (token-safe, case-insensitive)."""
    import re

    def repl(match: re.Match) -> str:
        token = match.group(0)
        return ABBREVIATIONS.get(token.lower(), token)

    pattern = re.compile(
        r"(?<![a-z0-9])(" + "|".join(re.escape(a) for a in ABBREVIATIONS) + r")(?![a-z0-9])",
        re.IGNORECASE,
    )
    return pattern.sub(repl, text)

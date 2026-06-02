"""
Load realistic code vocabularies from synthetic-cprd/codelists/ for synthetic data generation.

Each CSV is auto-classified as SNOMED CT, ICD-10, or dm+d using these rules (in order):
  1. Column named 'icd10_code'                        → ICD-10
  2. Column named 'bnf_code' or 'dmd_id'              → dm+d
  3. No 'code' column                                 → skip
  4. Filename contains 'icd10' or 'secondary-care'   → ICD-10
  5. First code is purely numeric with 7+ digits      → SNOMED CT
  6. Anything else (CTV3/Read codes, etc.)            → skip
"""
import csv
import os
import re

CODELISTS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'codelists')
)

if not os.path.isdir(CODELISTS_DIR):
    raise FileNotFoundError(
        f"Codelists directory not found: {CODELISTS_DIR}\n"
        "Expected synthetic-cprd/codelists/ to exist."
    )


def _classify(fname, headers, first_code):
    """Return (kind, code_column) or None to skip."""
    if 'icd10_code' in headers:
        return ('icd10', 'icd10_code')
    if 'bnf_code' in headers or 'dmd_id' in headers:
        return ('dmd', 'code')
    if 'code' not in headers:
        return None
    fname_lower = fname.lower()
    if 'icd10' in fname_lower or 'secondary-care' in fname_lower:
        return ('icd10', 'code')
    if re.match(r'^\d{7,}$', first_code):
        return ('snomed', 'code')
    return None


def _load_all():
    snomed, icd10, dmd = {}, {}, {}

    for fname in sorted(os.listdir(CODELISTS_DIR)):
        if not fname.endswith('.csv'):
            continue
        path = os.path.join(CODELISTS_DIR, fname)
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = set(reader.fieldnames or [])
            rows = list(reader)

        # Find first non-empty code to classify the file
        probe_col = 'icd10_code' if 'icd10_code' in headers else 'code'
        first_code = next(
            (r.get(probe_col, '').strip() for r in rows if r.get(probe_col, '').strip()),
            ''
        )
        if not first_code:
            continue

        result = _classify(fname, headers, first_code)
        if result is None:
            continue
        kind, col = result
        target = {'snomed': snomed, 'icd10': icd10, 'dmd': dmd}[kind]

        for row in rows:
            code = row.get(col, '').strip()
            if code and code not in target:
                target[code] = row.get('term', '').strip() or code

    return snomed, icd10, dmd


_snomed, _icd10, _dmd = _load_all()

# Exported vocabularies -------------------------------------------------------

# SNOMED CT codes for Observation.medcodeid
SNOMED_CODES = list(_snomed.keys())

# (medcodeid, term, entity_type, vocabulary) — for MedDictionary table
SNOMED_TERMS = [(code, term, "Disorder", "SNOMED") for code, term in _snomed.items()]

# ICD-10 codes for hes_diagnosis.diagcode and hes_hospital.diag_01
ICD10_CODES = list(_icd10.keys())

# dm+d codes for DrugIssue.prodcodeid
DMD_CODES = list(_dmd.keys())

# (prodcodeid, productname, drugsubstancename, formulation) — for ProductDictionary table
DMD_TERMS = [(code, term, term, "Tablet") for code, term in _dmd.items()]

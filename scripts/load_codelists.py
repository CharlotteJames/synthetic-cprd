"""
Load realistic code vocabularies from reducehf/codelists/ for synthetic data generation.

Provides SNOMED CT, ICD-10, and dm+d code lists derived from the project's real codelists.
The reducehf/ directory must be a sibling of synthetic-cprd/ in the monorepo.
"""
import csv
import os

CODELISTS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'codelists')
)

if not os.path.isdir(CODELISTS_DIR):
    raise FileNotFoundError(
        f"Codelists directory not found: {CODELISTS_DIR}\n"
        "Expected synthetic-cprd/codelists/ to exist."
    )


# SNOMED CT codelists (primary care clinical events → Observation.medcodeid)
_SNOMED_FILES = [
    "nhsd-primary-care-domain-refsets-bmival_cod.csv",
    "nhsd-primary-care-domain-refsets-copd_cod.csv",
    "nhsd-primary-care-domain-refsets-diabp_cod.csv",
    "nhsd-primary-care-domain-refsets-dmtype1_cod.csv",
    "nhsd-primary-care-domain-refsets-dmtype2_cod.csv",
    "nhsd-primary-care-domain-refsets-gestdiab_cod.csv",
    "nhsd-primary-care-domain-refsets-hf_cod.csv",
    "nhsd-primary-care-domain-refsets-homeless_cod.csv",
    "nhsd-primary-care-domain-refsets-hyp_cod.csv",
    "nhsd-primary-care-domain-refsets-illsub_cod.csv",
    "nhsd-primary-care-domain-refsets-otherdmaudit_cod.csv",
    "bristol-atrial-fibrillation-snomed.csv",
    "bristol-copd-exacerbations.csv",
    "bristol-hdl-cholesterol.csv",
    "bristol-ischaemic-heart-disease-snomed.csv",
    "opensafely-asthma-annual-review-qof.csv",
    "opensafely-care-planning-medication-review-simple-reference-set-nhs-digital.csv",
    "opensafely-cholesterol-tests-numerical-value.csv",
    "opensafely-chronic-obstructive-pulmonary-disease-copd-review-qof.csv",
    "opensafely-copd-exacerbation.csv",
    "opensafely-current-copd.csv",
    "opensafely-ethnicity-snomed-0removed.csv",
    "opensafely-glycated-haemoglobin-hba1c-tests-numerical-value.csv",
    "opensafely-height-snomed.csv",
    "opensafely-house-bound.csv",
    "opensafely-not-house-bound.csv",
    "opensafely-systolic-blood-pressure-qof.csv",
    "opensafely-weight-snomed.csv",
    "primis-covid19-vacc-uptake-bmi.csv",
    "primis-covid19-vacc-uptake-bmi_stage.csv",
    "primis-covid19-vacc-uptake-chd_cov.csv",
    "primis-covid19-vacc-uptake-ckd15.csv",
    "primis-covid19-vacc-uptake-ckd35.csv",
    "primis-covid19-vacc-uptake-ckd_cov.csv",
    "primis-covid19-vacc-uptake-cld.csv",
    "primis-covid19-vacc-uptake-cns_cov.csv",
    "primis-covid19-vacc-uptake-diab.csv",
    "primis-covid19-vacc-uptake-dmres.csv",
    "primis-covid19-vacc-uptake-learndis.csv",
    "primis-covid19-vacc-uptake-resp_cov.csv",
    "primis-covid19-vacc-uptake-sev_mental.csv",
    "primis-covid19-vacc-uptake-sev_obesity.csv",
    "primis-covid19-vacc-uptake-smhres.csv",
    "reducehf-beathlessness4all.csv",
    "reducehf-body-mass-index-numeric-value.csv",
    "reducehf-current-smoker.csv",
    "reducehf-echocardiography-referral.csv",
    "reducehf-echocardiography-result.csv",
    "reducehf-fatigue.csv",
    "reducehf-former-smoker.csv",
    "reducehf-heart-failure-ae.csv",
    "reducehf-non-english-speaking.csv",
    "reducehf-np-any.csv",
    "reducehf-ntpro-num-only.csv",
    "reducehf-oedema4all.csv",
    "user-RochelleKnight-pregnancy_and_birth_snomed.csv",
    "user-RochelleKnight-prostate_cancer_snomed.csv",
    "user-YaminaB-migration-status.csv",
    "user-anschaf-diabetes-non-diagnostic-codes.csv",
    "user-elsie_horne-bmi_obesity_snomed.csv",
    "user-elsie_horne-ckd_snomed.csv",
    "user-elsie_horne-diabetes_snomed.csv",
    "user-elsie_horne-stroke_isch_snomed.csv",
]

# ICD-10 codelists (secondary care diagnoses → hes_diagnosis.diagcode / hes_hospital.diag_01)
# Entries are (filename, code_column) — most use "code" but one uses "icd10_code".
_ICD10_FILES = [
    ("bristol-atrial-fibrillation-icd10.csv", "code"),
    ("bristol-ischaemic-heart-disease-icd10.csv", "code"),
    ("opensafely-copd-secondary-care.csv", "code"),
    ("opensafely-type-1-diabetes-secondary-care.csv", "icd10_code"),
    ("reducehf-heart-failure-secondary-care.csv", "code"),
    ("reducehf-myocardial-infarction-icd10.csv", "code"),
    ("user-RochelleKnight-prostate_cancer_icd10.csv", "code"),
    ("user-RochelleKnight-stroke_isch_icd10.csv", "code"),
    ("user-alainamstutz-gestational-diabetes-icd10-bristol.csv", "code"),
    ("user-elsie_horne-bmi_obesity_icd10.csv", "code"),
    ("user-elsie_horne-ckd_icd10.csv", "code"),
    ("user-elsie_horne-diabetes_icd10.csv", "code"),
    ("user-elsie_horne-hypertension_icd10.csv", "code"),
]

# dm+d codelists (drug products → DrugIssue.prodcodeid)
_DMD_FILES = [
    "opensafely-antidiabetic-drugs.csv",
    "opensafely-copd-medications-new-dmd.csv",
    "opensafely-insulin-medication.csv",
    "user-elsie_horne-cocp_dmd.csv",
    "user-elsie_horne-diabetes_drugs_dmd.csv",
    "user-elsie_horne-hypertension_drugs_dmd.csv",
    "user-elsie_horne-hrt_dmd.csv",
    "user-r_denholm-non-metformin-antidiabetic-drugs_bristol.csv",
]


def _read_codes(files, code_col='code'):
    seen = set()
    codes = []
    for fname in files:
        path = os.path.join(CODELISTS_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                code = row.get(code_col, '').strip()
                if code and code not in seen:
                    seen.add(code)
                    codes.append(code)
    return codes


def _read_code_term_pairs(files, code_col='code'):
    seen = set()
    pairs = []
    for fname in files:
        path = os.path.join(CODELISTS_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                code = row.get(code_col, '').strip()
                term = row.get('term', '').strip()
                if not term:
                    term = code
                if code and code not in seen:
                    seen.add(code)
                    pairs.append((code, term))
    return pairs


def _read_icd10_codes():
    seen = set()
    codes = []
    for fname, col in _ICD10_FILES:
        path = os.path.join(CODELISTS_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                code = row.get(col, '').strip()
                if code and code not in seen:
                    seen.add(code)
                    codes.append(code)
    return codes


# Exported vocabularies -------------------------------------------------------

# SNOMED CT codes for Observation.medcodeid
SNOMED_CODES = _read_codes(_SNOMED_FILES)

# (medcodeid, term, entity_type, vocabulary) — for MedDictionary table
SNOMED_TERMS = [
    (code, term, "Disorder", "SNOMED")
    for code, term in _read_code_term_pairs(_SNOMED_FILES)
]

# ICD-10 codes for hes_diagnosis.diagcode and hes_hospital.diag_01
ICD10_CODES = _read_icd10_codes()

# dm+d codes for DrugIssue.prodcodeid
DMD_CODES = _read_codes(_DMD_FILES)

# (prodcodeid, productname, drugsubstancename, formulation) — for ProductDictionary table
DMD_TERMS = [
    (code, term, term, "Tablet")
    for code, term in _read_code_term_pairs(_DMD_FILES)
]

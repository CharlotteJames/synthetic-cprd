
# CONFIGURATION

N_PRACTICES = 100
N_PATIENTS = 10000
N_STAFF = 120
N_CONSULTATIONS = 50000
N_OBSERVATIONS = 12000
N_REFERRALS = 120
N_PROBLEMS = 180
N_DRUG_ISSUES = 400

OUTPUT_DIR = "./data/cprd/raw/"

import os as _os, sys as _sys, random as _random
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
from load_codelists import SNOMED_CODES, SNOMED_TERMS, DMD_CODES, DMD_TERMS
del _os, _sys

_rng = _random.Random(42)
_snomed_sample = _rng.sample(list(zip(SNOMED_CODES, [t[1] for t in SNOMED_TERMS])), min(1000, len(SNOMED_CODES)))
MEDCODE_POOL = [c for c, _ in _snomed_sample]
MEDICAL_DICTIONARY_TERMS = [(c, t, "Disorder", "SNOMED") for c, t in _snomed_sample]
del _rng, _snomed_sample, _random

PRODCODE_POOL = DMD_CODES
PRODUCT_DICTIONARY_TERMS = DMD_TERMS


# LOOKUP VALUES

GENDER_VALUES = [1, 2]
PATIENT_TYPE_VALUES = [1, 2, 3]
REGION_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
JOBCAT_VALUES = [1, 2, 3, 4, 5, 6]
OBSTYPE_VALUES = [1, 2, 3, 4]
NUMUNIT_VALUES = [1, 2, 3, 4, 5]
CONS_SOURCE_VALUES = [1001, 1002, 1003, 1004]

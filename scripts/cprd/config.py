
# CONFIGURATION

import os
import sys
import random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from load_codelists import SNOMED_CODES, SNOMED_TERMS, DMD_CODES, DMD_TERMS

# CONFIGURATION

N_PRACTICES     = int(os.environ.get("SYNTH_N_PRACTICES",     100))
N_PATIENTS      = int(os.environ.get("SYNTH_N_PATIENTS",      10000))
N_STAFF         = int(os.environ.get("SYNTH_N_STAFF",         120))
N_CONSULTATIONS = int(os.environ.get("SYNTH_N_CONSULTATIONS", 50000))
N_OBSERVATIONS  = int(os.environ.get("SYNTH_N_OBSERVATIONS",  12000))
N_REFERRALS     = int(os.environ.get("SYNTH_N_REFERRALS",     120))
N_PROBLEMS      = int(os.environ.get("SYNTH_N_PROBLEMS",      180))
N_DRUG_ISSUES   = int(os.environ.get("SYNTH_N_DRUG_ISSUES",   400))

OUTPUT_DIR = "./data/cprd/raw/"

_rng = random.Random(42)
_snomed_sample = _rng.sample(list(zip(SNOMED_CODES, [t[1] for t in SNOMED_TERMS])), min(1000, len(SNOMED_CODES)))
# CPRD-internal medcodeids: sequential 6-digit codes, distinct from SNOMED concept IDs
MEDCODE_POOL = [str(100000 + i) for i in range(len(_snomed_sample))]
# (medcodeid, term, snomedctconceptid) — medcodeid is CPRD-internal; snomedctconceptid is the SNOMED code
MEDICAL_DICTIONARY_TERMS = [
    (str(100000 + i), term, snomed_code)
    for i, (snomed_code, term) in enumerate(_snomed_sample)
]

# CPRD-internal prodcodeids: sequential 6-digit codes, distinct from DM+D IDs
PRODCODE_POOL = [str(200000 + i) for i in range(len(DMD_CODES))]
# (prodcodeid, termfromemis, dmdid) — prodcodeid is CPRD-internal; dmdid is the DM+D code
PRODUCT_DICTIONARY_TERMS = [
    (str(200000 + i), term, dmd_code)
    for i, (dmd_code, term) in enumerate(DMD_TERMS)
]


# LOOKUP VALUES

GENDER_VALUES = [1, 2]
PATIENT_TYPE_VALUES = [1, 2, 3]
REGION_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
JOBCAT_VALUES = [1, 2, 3, 4, 5, 6]
OBSTYPE_VALUES = [1, 2, 3, 4]
NUMUNIT_VALUES = [1, 2, 3, 4, 5]
CONS_SOURCE_VALUES = [1001, 1002, 1003, 1004]
REFURGENCY_VALUES = [1, 2, 3]       # Lookup: RefUrgency.txt (routine, urgent, dated)
REFSERVICETYPE_VALUES = [1, 2, 3]   # Lookup: RefServiceType.txt
REFMODE_VALUES = [1, 2, 3]          # Lookup: RefMode.txt
PARENTPROBREL_VALUES = [1, 2, 3]    # Lookup: ParentProbRel.txt
PROBSTATUS_VALUES = [1, 2]          # Lookup: ProbStatus.txt (active, past)
SIGN_VALUES = [1, 2]                # Lookup: Sign.txt (minor, significant)
QUANTUNIT_VALUES = [1, 2, 3, 4]     # Lookup: QuantUnit.txt

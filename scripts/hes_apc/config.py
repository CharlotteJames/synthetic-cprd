# CONFIGURATION

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from load_codelists import ICD10_CODES

# CONFIGURATION

N_EPISODES = 10000

OUTPUT_DIR = "data/hes_apc/raw/"
CPRD_DIR = 'data/cprd/raw/'


# LOOKUPS

SEX_VALUES = [1, 2]
ADMIMETH_VALUES = ["11", "12", "13", "21", "22", "28"]
DISMETH_VALUES = ["1", "2", "4", "8"]
EPISTAT_VALUES = [1, 3]
CLASSPAT_VALUES = [1, 2, 3, 4]
ADMINCAT_VALUES = [1, 2, 3]
MAINSPEF_VALUES = ["100", "110", "120", "300", "301", "430"]
TRETSPEF_VALUES = ["100", "110", "120", "300", "301", "430"]

OPCS_CODES = [
    "X401",
    "K401",
    "W371",
    "A012",
    "H331",
    "T123",
    "U205",
    "E856",
    "L703",
    "Y981",
]

HRG_CODES = [
    "AA26Z",
    "DZ11A",
    "EB03Z",
    "FZ38C",
    "LA08E",
]

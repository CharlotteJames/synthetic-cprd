
# ============================================================
# CONFIGURATION
# ============================================================

N_APPOINTMENTS = 8000

OUTPUT_DIR = "data/hes_op/raw/"
CPRD_DIR = "data/cprd/raw/"


# ============================================================
# LOOKUPS
# ============================================================

# Administrative category: 1=NHS, 2=Private
ADMINCAT_VALUES = [1, 1, 1, 1, 1, 2]

# Attendance type: 1=first face-to-face, 2=subsequent face-to-face,
#                  3=first telephone, 4=subsequent telephone
ATENTYPE_VALUES = [1, 2, 2, 2, 3, 4]

# Attended / DNA status
# 5=attended on time, 6=arrived late, 7=DNA no warning, 2=patient cancelled
ATTENDED_VALUES = [5, 5, 5, 5, 5, 5, 5, 6, 7, 7, 2]

# First attendance: 1=first, 2=follow-up, 3=DNA sent follow-up, 4=DNA sent discharge
FIRSTATT_VALUES = ["1", "1", "2", "2", "2", "3", "4"]

# Outcome of attendance
# 1=discharged, 2=another appointment given, 3=referral to other HCP,
# 4=another appointment to be given, 8=treatment incomplete
OUTCOME_VALUES = [1, 2, 2, 2, 3, 4, 8]

# Priority type: 1=routine, 2=urgent, 3=two week wait
PRIORITY_VALUES = [1, 1, 1, 2, 3]

# Source of referral
# 1=GP, 2=A&E, 3=bed bureau, 4=consultant clinic, 5=community mental health,
# 7=emergency admission, 8=self-referral, 9=other
REFSOURC_VALUES = [1, 1, 1, 1, 2, 3, 4, 5, 7, 8, 9]

# Service type: 1=consultant referral, 2=domiciliary, 3=telephone
SERVTYPE_VALUES = [1, 1, 1, 2, 3]

# Medical staff type: 1=consultant, 2=other medical, 3=nurse, 4=midwife, 5=AHP
STAFFTYP_VALUES = [1, 1, 1, 2, 3, 4, 5]

# Waiting calculation indicator: 0=not applicable, 1=started, 2=stopped
WAIT_IND_VALUES = [0, 1, 1, 1, 2]

# Ethnic category recorded at appointment
ETHNOS_VALUES = [
    "A", "B", "C", "D", "E", "F", "G",
    "H", "J", "K", "L", "M", "N", "P",
    "R", "S", "X", "Z",
]

# Derived patient ethnicity from all HES data
GEN_ETHNICITY_VALUES = [
    "White", "Black_Caribbean", "Black_African", "Black_Other",
    "Indian", "Pakistani", "Bangladeshi", "Other_Asian",
    "Chinese", "Mixed", "Other", "Unknown",
]

# Treatment and main specialty codes
SPEF_VALUES = [
    "100",  # General Surgery
    "110",  # Trauma and Orthopaedic Surgery
    "120",  # ENT
    "130",  # Ophthalmology
    "140",  # Oral Surgery
    "150",  # Neurosurgery
    "300",  # General Medicine
    "301",  # Gastroenterology
    "302",  # Endocrinology
    "303",  # Clinical Haematology
    "320",  # Cardiology
    "330",  # Dermatology
    "340",  # Respiratory Medicine
    "400",  # Neurology
    "410",  # Rheumatology
    "420",  # Paediatrics
    "430",  # Geriatric Medicine
    "500",  # Obstetrics
    "501",  # Gynaecology
]

# Operation status codes
OPERSTAT_VALUES = ["1", "2", "2", "3", "4", "8"]


# ============================================================
# DIAGNOSIS CODES (ICD-10; <5% of OP appointments per spec)
# ============================================================

ICD10_CODES = [
    "I10",   # Essential hypertension
    "E119",  # Type 2 diabetes without complications
    "J459",  # Asthma, unspecified
    "N189",  # Chronic kidney disease, unspecified
    "I500",  # Congestive heart failure
    "F329",  # Depressive episode, unspecified
    "K219",  # Gastro-oesophageal reflux without oesophagitis
    "M199",  # Osteoarthritis, unspecified
    "G439",  # Migraine, unspecified
    "J189",  # Pneumonia, unspecified
    "L409",  # Psoriasis, unspecified
    "G409",  # Epilepsy, unspecified
    "I639",  # Cerebral infarction, unspecified
    "C509",  # Malignant neoplasm of breast, unspecified
    "M545",  # Low back pain
]


# ============================================================
# OPCS-4 PROCEDURE CODES (5-15% of OP appointments per spec)
# ============================================================

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

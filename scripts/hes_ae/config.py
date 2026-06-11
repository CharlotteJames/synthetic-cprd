
# CONFIGURATION

N_ATTENDANCES = 5000

OUTPUT_DIR = "data/hes_ae/raw/"
CPRD_DIR = "data/cprd/raw/"


# LOOKUPS

# Attendance category: 1=first, 2=planned follow-up, 3=unplanned follow-up
AEATTENDCAT_VALUES = [1, 2, 3]

# Department type
AEDEPTTYPE_VALUES = ["01", "02", "03", "04"]

# Arrival mode: 1=ambulance, 2=other
AEARRIVALMODE_VALUES = [1, 2]

# Referral source
AEREFSOURCE_VALUES = ["01", "02", "03", "04", "05"]

# Incident location type
AEINCLOCTYPE_VALUES = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "99"]

# Attendance disposal
AEATTENDDISP_VALUES = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]

# Patient group (reason for attendance)
AEPATGROUP_VALUES = [11, 12, 13, 14, 15, 99]

# Ethnicity recorded at attendance (ethnos)
ETHNOS_VALUES = [
    "A", "B", "C", "D", "E", "F", "G",
    "H", "J", "K", "L", "M", "N", "P",
    "R", "S", "X", "Z",
]

# Derived ethnicity (gen_ethnicity) from all HES data
GEN_ETHNICITY_VALUES = [
    "White", "Black_Caribbean", "Black_African", "Black_Other",
    "Indian", "Pakistani", "Bangladeshi", "Other_Asian",
    "Chinese", "Mixed", "Other", "Unknown",
]

# Linkage quality (match_rank 1-5; lower is stronger)
MATCH_RANK_VALUES = [1, 1, 1, 1, 2, 2, 2, 3, 4, 5]

# Diagnosis coding scheme: 02=HES A&E, 01=ICD-10 (rare)
DIAGSCHEME_VALUES = ["02", "02", "02", "02", "02", "01"]


# A&E DIAGNOSIS CODES
# 6-character format: condition(n2) + sub-analysis(n1) +
#                     anatomical area(n2) + side(an1)
# diag2 = [0:2], diag3 = [0:3], diaga = [3:5], diags = [5]

AE_DIAG_CODES = [
    "01001L",  # Laceration, head/face, left
    "01001R",  # Laceration, head/face, right
    "01009N",  # Laceration, wrist
    "01010N",  # Laceration, hand/fingers
    "02001N",  # Contusion, head
    "02012N",  # Contusion, knee
    "02014N",  # Contusion, ankle
    "03009N",  # Sprain, wrist
    "03012N",  # Sprain, knee
    "03014N",  # Sprain, ankle
    "04006L",  # Fracture, shoulder/upper arm, left
    "04006R",  # Fracture, shoulder/upper arm, right
    "04009N",  # Fracture, wrist
    "04010N",  # Fracture, hand/fingers
    "04012N",  # Fracture, knee
    "04014N",  # Fracture, ankle
    "08003N",  # Soft tissue injury, chest
    "10001L",  # Eye injury, left
    "10001R",  # Eye injury, right
    "11003N",  # Burns, chest
    "14000N",  # Allergic/anaphylactic reaction
    "15001N",  # Head injury, head
    "18003N",  # Cardiac arrest, chest
    "19003N",  # Chest pain, chest
    "20003N",  # Dyspnoea, chest
    "25004N",  # Abdominal pain, abdomen
    "35000N",  # Psychiatric condition
    "40000N",  # Overdose/poisoning
]


# A&E INVESTIGATION CODES
# 6-character format: investigation(n2) + sub-analysis(up to an4)
# invest2 = [0:2]

AE_INVEST_CODES = [
    "010000",  # None
    "020000",  # Blood tests
    "030000",  # ECG
    "040000",  # X-ray
    "050000",  # CT scan
    "060000",  # Ultrasound
    "070000",  # Urine test
    "080000",  # Pregnancy test
    "090000",  # Wound swab
    "100000",  # Peak flow measurement
]


# A&E TREATMENT CODES
# 6-character format: treatment(n2) + sub-analysis(n1) + local(up to an3)
# treat2 = [0:2], treat3 = [0:3]

AE_TREAT_CODES = [
    "010000",  # None
    "020000",  # Advice and analgesia
    "030000",  # Dressing
    "040000",  # Wound closure/sutures
    "050000",  # Plaster of paris
    "060000",  # IV access and fluids
    "070000",  # Observation
    "080000",  # Local anaesthesia
    "090000",  # IV medication
    "100000",  # Catheterisation
]


# HEALTH RESOURCE GROUP CODES (A&E VB codes)

AE_HRG_CODES = [
    "VB01Z",  # Minor head injury
    "VB02Z",  # Head injury
    "VB03Z",  # Chest pain
    "VB04Z",  # Abdominal pain
    "VB05Z",  # Minor trauma
    "VB06Z",  # Major trauma
    "VB07Z",  # Cardiac/circulatory disorder
    "VB08Z",  # Mental health attendance
    "VB09Z",  # Other medical attendance
    "VB10Z",  # Respiratory disorder
]

AE_HRG_TRUST_CODES = ["VB1", "VB2", "VB3", "VB4", "VB5"]

AE_HRG_TRUST_VERSIONS = ["V12", "V13", "V14", "V15"]

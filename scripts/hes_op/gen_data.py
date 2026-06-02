
import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from config import *

random.seed(42)
np.random.seed(42)



# HELPERS


def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))



def format_date(dt):
    return dt.strftime("%Y/%m/%d")



def random_numeric_string(length):
    return "".join(random.choices("0123456789", k=length))



# LOAD CPRD PATIENTS

patient_df = pd.read_csv(CPRD_DIR + "Patient.csv")



# 1. PATIENT TABLE (hesop_patient)

sampled_patients = patient_df.sample(
    n=min(N_APPOINTMENTS, len(patient_df)),
    replace=True,
).drop_duplicates(subset="patid")

hesop_patient_rows = []

for _, patient in sampled_patients.iterrows():

    hesop_patient_rows.append(
        {
            "patid": patient["patid"],
            "pracid": patient["pracid"],
            "cprd_mpsid": random_numeric_string(10),
            "gen_ethnicity": random.choice(
                GEN_ETHNICITY_VALUES
            ),
        }
    )

hesop_patient_df = pd.DataFrame(hesop_patient_rows)

op_patids = hesop_patient_df["patid"].tolist()



# 2. APPOINTMENT TABLE (hesop_appointment)

hesop_appointment_rows = []

patid_attendkey_pairs = []

for _ in range(N_APPOINTMENTS):

    patid = random.choice(op_patids)

    attendkey = random_numeric_string(12)

    patid_attendkey_pairs.append((patid, attendkey))

    apptdate = random_date(
        datetime(2003, 4, 1),
        datetime(2025, 3, 31),
    )

    patient_row = patient_df[
        patient_df["patid"] == patid
    ]

    if len(patient_row) > 0:
        yob = int(patient_row.iloc[0]["yob"])
        apptage = max(0, apptdate.year - yob)
    else:
        apptage = random.randint(0, 90)

    waiting = random.randint(0, 365)

    reqdate = apptdate - timedelta(days=waiting)

    attended = random.choice(ATTENDED_VALUES)

    if attended in [7, 2]:
        dnadate = format_date(apptdate)
    else:
        dnadate = ""

    hesop_appointment_rows.append(
        {
            "patid": patid,
            "attendkey": attendkey,
            "ethnos": random.choice(ETHNOS_VALUES),
            "admincat": random.choice(ADMINCAT_VALUES),
            "apptdate": format_date(apptdate),
            "apptage": apptage,
            "atentype": random.choice(ATENTYPE_VALUES),
            "attended": attended,
            "dnadate": dnadate,
            "firstatt": random.choice(FIRSTATT_VALUES),
            "outcome": random.choice(OUTCOME_VALUES),
            "priority": random.choice(PRIORITY_VALUES),
            "refsourc": random.choice(REFSOURC_VALUES),
            "reqdate": format_date(reqdate),
            "servtype": random.choice(SERVTYPE_VALUES),
            "stafftyp": random.choice(STAFFTYP_VALUES),
            "wait_ind": random.choice(WAIT_IND_VALUES),
            "waiting": waiting,
        }
    )

hesop_appointment_df = pd.DataFrame(
    hesop_appointment_rows
)



# 3. PATIENT PATHWAY TABLE (hesop_patient_pathway)

hesop_patient_pathway_rows = []

for patid, attendkey in patid_attendkey_pairs:

    subdate = random_date(
        datetime(2003, 4, 1),
        datetime(2025, 3, 31),
    )

    hesop_patient_pathway_rows.append(
        {
            "patid": patid,
            "attendkey": attendkey,
            "subdate": format_date(subdate),
        }
    )

hesop_patient_pathway_df = pd.DataFrame(
    hesop_patient_pathway_rows
)



# 4. CLINICAL TABLE (hesop_clinical)
# ~8% of appointments have clinical/diagnosis data (per spec)

hesop_clinical_rows = []

clinical_pairs = random.sample(
    patid_attendkey_pairs,
    int(N_APPOINTMENTS * 0.08),
)

for patid, attendkey in clinical_pairs:

    n_diag = random.randint(1, 3)

    spef = random.choice(SPEF_VALUES)

    for i in range(1, n_diag + 1):

        icd = random.choice(ICD10_CODES)

        hesop_clinical_rows.append(
            {
                "patid": patid,
                "attendkey": attendkey,
                "diagnosis": icd,
                "icdx": icd,
                "icd": icd[:3],
                "diag_order": i,
                "tretspef": spef,
                "mainspef": spef,
            }
        )

hesop_clinical_df = pd.DataFrame(
    hesop_clinical_rows
)



# 5. OPERATIONS TABLE (hesop_operation)
# ~10% of appointments have operation data (per spec)

hesop_operation_rows = []

operation_pairs = random.sample(
    patid_attendkey_pairs,
    int(N_APPOINTMENTS * 0.10),
)

for patid, attendkey in operation_pairs:

    n_ops = random.randint(1, 3)

    spef = random.choice(SPEF_VALUES)

    for i in range(1, n_ops + 1):

        opcs = random.choice(OPCS_CODES)

        hesop_operation_rows.append(
            {
                "patid": patid,
                "attendkey": attendkey,
                "operation": opcs,
                "opcs": opcs,
                "opertn_order": i,
                "operstat": random.choice(OPERSTAT_VALUES),
                "tretspef": spef,
                "mainspef": spef,
            }
        )

hesop_operation_df = pd.DataFrame(
    hesop_operation_rows
)



# EXPORT

os.makedirs(OUTPUT_DIR, exist_ok=True)

hesop_patient_df.to_csv(
    f"{OUTPUT_DIR}/hesop_patient.csv",
    index=False,
)

hesop_appointment_df.to_csv(
    f"{OUTPUT_DIR}/hesop_appointment.csv",
    index=False,
)

hesop_patient_pathway_df.to_csv(
    f"{OUTPUT_DIR}/hesop_patient_pathway.csv",
    index=False,
)

hesop_clinical_df.to_csv(
    f"{OUTPUT_DIR}/hesop_clinical.csv",
    index=False,
)

hesop_operation_df.to_csv(
    f"{OUTPUT_DIR}/hesop_operation.csv",
    index=False,
)

print("HES OP synthetic data generated")


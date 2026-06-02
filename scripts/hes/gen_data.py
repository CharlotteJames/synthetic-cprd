
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
    return dt.strftime("%d/%m/%Y")



def random_numeric_string(length):
    return "".join(random.choices("0123456789", k=length))



def generate_patid(pracid):
    prefix_len = random.randint(3, 12)
    prefix = "".join(random.choices("0123456789", k=prefix_len))
    return f"{prefix}{str(pracid).zfill(5)}"



# PATIENTS

patient_df = pd.read_csv(CPRD_DIR + 'Patient.csv')

# hospital TABLE

hes_hospital_rows = []

epikeys = []

for _ in range(N_EPISODES):

    patient = patient_df.sample(1).iloc[0]

    epikey = random_numeric_string(12)

    epikeys.append(epikey)

    admidate = random_date(
        datetime(2015, 1, 1),
        datetime(2025, 1, 1),
    )

    disdate = admidate + timedelta(
        days=random.randint(0, 21)
    )

    hes_hospital_rows.append(
        {
            "patid": patient["patid"],
            "epikey": epikey,
            "admidate": format_date(admidate),
            "disdate": format_date(disdate),
            "epistart": format_date(admidate),
            "epiend": format_date(disdate),
            "admimeth": random.choice(
                ADMIMETH_VALUES
            ),
            "dismeth": random.choice(
                DISMETH_VALUES
            ),
            "sex": patient["gender"],
            "startage": max(
                0,
                admidate.year - patient["yob"],
            ),
            "classpat": random.choice(
                CLASSPAT_VALUES
            ),
            "admincat": random.choice(
                ADMINCAT_VALUES
            ),
            "epistat": random.choice(
                EPISTAT_VALUES
            ),
            "mainspef": random.choice(
                MAINSPEF_VALUES
            ),
            "tretspef": random.choice(
                TRETSPEF_VALUES
            ),
            "diag_01": random.choice(
                ICD10_CODES
            ),
            "operstat": random.choice(
                [0, 1]
            ),
            "spellid": random_numeric_string(10),
        }
    )

hes_hospital_df = pd.DataFrame(
    hes_hospital_rows
)
  

# HES DIAGNOSIS TABLE

hes_diagnosis_rows = []

for epikey in epikeys:

    n_diag = random.randint(1, 10)

    for i in range(1, n_diag + 1):

        hes_diagnosis_rows.append(
            {
                "epikey": epikey,
                "diag_order": i,
                "diagcode": random.choice(
                    ICD10_CODES
                ),
            }
        )

hes_diagnosis_df = pd.DataFrame(
    hes_diagnosis_rows
)


# HES PROCEDURE TABLE

hes_procedure_rows = []

for epikey in epikeys:

    n_proc = random.randint(0, 6)

    for i in range(1, n_proc + 1):

        hes_procedure_rows.append(
            {
                "epikey": epikey,
                "proc_order": i,
                "proccode": random.choice(
                    OPCS_CODES
                ),
                "procdate": format_date(
                    random_date(
                        datetime(2015, 1, 1),
                        datetime(2025, 1, 1),
                    )
                ),
            }
        )

hes_procedure_df = pd.DataFrame(
    hes_procedure_rows
)


# APC COST TABLE

apc_cost_rows = []

for epikey in epikeys:

    apc_cost_rows.append(
        {
            "epikey": epikey,
            "hrgcode": random.choice(HRG_CODES),
            "tariff": round(random.uniform(250, 15000), 2),
            "los": random.randint(0, 30),
        }
    )

apc_cost_df = pd.DataFrame(apc_cost_rows)


# HES CRITICAL CARE TABLE

hes_criticalcare_rows = []

for epikey in random.sample(
    epikeys,
    int(N_EPISODES * 0.12),
):

    hes_criticalcare_rows.append(
        {
            "epikey": epikey,
            "ccdays": random.randint(1, 20),
            "basicresp": random.randint(0, 10),
            "advancedresp": random.randint(0, 10),
            "basiccardio": random.randint(0, 10),
            "advancedcardio": random.randint(0, 10),
        }
    )

hes_criticalcare_df = pd.DataFrame(
    hes_criticalcare_rows
)

# HES MATERNITY TABLE

hes_maternity_rows = []

female_patients = patient_df[
    patient_df["gender"] == 2
]

for _ in range(250):

    patient = female_patients.sample(1).iloc[0]

    hes_maternity_rows.append(
        {
            "patid": patient["patid"],
            "epikey": random.choice(epikeys),
            "gestat": random.randint(28, 42),
            "birthweight": random.randint(
                1800,
                4500,
            ),
            "deliverymeth": random.choice(
                [1, 2, 3, 4, 5]
            ),
            "babystatus": random.choice(
                [1, 2]
            ),
        }
    )

hes_maternity_df = pd.DataFrame(
    hes_maternity_rows
)


# EXPORT

os.makedirs(OUTPUT_DIR, exist_ok=True)

patient_df.to_csv(
    f"{OUTPUT_DIR}/hes_patient.csv",
    index=False,
)

hes_hospital_df.to_csv(
    f"{OUTPUT_DIR}/hes_hospital.csv",
    index=False,
)

hes_diagnosis_df.to_csv(
    f"{OUTPUT_DIR}/hes_diagnosis.csv",
    index=False,
)

hes_procedure_df.to_csv(
    f"{OUTPUT_DIR}/hes_procedure.csv",
    index=False,
)

hes_criticalcare_df.to_csv(
    f"{OUTPUT_DIR}/hes_criticalcare.csv",
    index=False,
)

hes_maternity_df.to_csv(
    f"{OUTPUT_DIR}/hes_maternity.csv",
    index=False,
)

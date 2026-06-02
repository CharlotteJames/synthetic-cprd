
import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from config import *

random.seed(42)
np.random.seed(42)





def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))



def format_date(dt):
    return dt.strftime("%d/%m/%Y")



def random_numeric_string(length):
    return "".join(random.choices("0123456789", k=length))




patient_df = pd.read_csv(CPRD_DIR + "Patient.csv")




sampled_patients = patient_df.sample(
    n=min(N_ATTENDANCES, len(patient_df)),
    replace=True,
).drop_duplicates(subset="patid")

hesae_patient_rows = []

for _, patient in sampled_patients.iterrows():

    hesae_patient_rows.append(
        {
            "patid": patient["patid"],
            "pracid": patient["pracid"],
            "gen_ethnicity": random.choice(
                GEN_ETHNICITY_VALUES
            ),
            "cprd_mpsid": random_numeric_string(10),
        }
    )

hesae_patient_df = pd.DataFrame(hesae_patient_rows)

ae_patids = hesae_patient_df["patid"].tolist()




hesae_attendance_rows = []

aekeys = []

patid_aekey_pairs = []

for _ in range(N_ATTENDANCES):

    patid = random.choice(ae_patids)

    aekey = random_numeric_string(12)

    aekeys.append(aekey)

    patid_aekey_pairs.append((patid, aekey))

    arrivaldate = random_date(
        datetime(2007, 4, 1),
        datetime(2020, 3, 31),
    )

    initdur = random.randint(0, 240)

    tretdur = initdur + random.randint(0, 180)

    concldur = tretdur + random.randint(0, 60)

    depdur = concldur + random.randint(0, 30)

    hesae_attendance_rows.append(
        {
            "patid": patid,
            "aekey": aekey,
            "arrivaldate": format_date(arrivaldate),
            "aepatgroup": random.choice(
                AEPATGROUP_VALUES
            ),
            "aeattendcat": random.choice(
                AEATTENDCAT_VALUES
            ),
            "aearrivalmode": random.choice(
                AEARRIVALMODE_VALUES
            ),
            "aedepttype": random.choice(
                AEDEPTTYPE_VALUES
            ),
            "aerefsource": random.choice(
                AEREFSOURCE_VALUES
            ),
            "aeincloctype": random.choice(
                AEINCLOCTYPE_VALUES
            ),
            "aeattenddisp": random.choice(
                AEATTENDDISP_VALUES
            ),
            "initdur": initdur,
            "tretdur": tretdur,
            "concldur": concldur,
            "depdur": depdur,
            "ethnos": random.choice(
                ETHNOS_VALUES
            ),
        }
    )

hesae_attendance_df = pd.DataFrame(
    hesae_attendance_rows
)




hesae_diagnosis_rows = []

for patid, aekey in patid_aekey_pairs:

    n_diag = random.randint(1, 3)

    for i in range(1, n_diag + 1):

        diag = random.choice(AE_DIAG_CODES)

        hesae_diagnosis_rows.append(
            {
                "patid": patid,
                "aekey": aekey,
                "diag": diag,
                "diag2": diag[0:2],
                "diag3": diag[0:3],
                "diaga": diag[3:5],
                "diags": diag[5],
                "diagscheme": random.choice(
                    DIAGSCHEME_VALUES
                ),
                "diag_order": i,
            }
        )

hesae_diagnosis_df = pd.DataFrame(
    hesae_diagnosis_rows
)




hesae_investigation_rows = []

for patid, aekey in patid_aekey_pairs:

    n_invest = random.randint(0, 4)

    for i in range(1, n_invest + 1):

        invest = random.choice(AE_INVEST_CODES)

        hesae_investigation_rows.append(
            {
                "patid": patid,
                "aekey": aekey,
                "invest": invest,
                "invest2": invest[0:2],
                "invest_order": i,
            }
        )

hesae_investigation_df = pd.DataFrame(
    hesae_investigation_rows
)




hesae_treatment_rows = []

for patid, aekey in patid_aekey_pairs:

    n_treat = random.randint(1, 2)

    for i in range(1, n_treat + 1):

        treat = random.choice(AE_TREAT_CODES)

        hesae_treatment_rows.append(
            {
                "patid": patid,
                "aekey": aekey,
                "treat": treat,
                "treat2": treat[0:2],
                "treat3": treat[0:3],
                "treat_order": i,
            }
        )

hesae_treatment_df = pd.DataFrame(
    hesae_treatment_rows
)




hesae_hrg_rows = []

for patid, aekey in patid_aekey_pairs:

    hesae_hrg_rows.append(
        {
            "patid": patid,
            "aekey": aekey,
            "domproc": random.choice(
                ["", "", "", "01ZZZZ", "02ZZZZ", "03ZZZZ"]
            ),
            "hrgnhs": random.choice(
                AE_HRG_TRUST_CODES
            ),
            "hrgnhsvn": random.choice(
                AE_HRG_TRUST_VERSIONS
            ),
            "sushrg": random.choice(
                AE_HRG_CODES
            ),
            "sushrgvers": random.randint(1, 5),
        }
    )

hesae_hrg_df = pd.DataFrame(hesae_hrg_rows)




hesae_pathway_rows = []

pathway_pairs = random.sample(
    patid_aekey_pairs,
    int(N_ATTENDANCES * 0.15),
)

for patid, aekey in pathway_pairs:

    rttperstart = random_date(
        datetime(2007, 4, 1),
        datetime(2019, 1, 1),
    )

    rttperend = rttperstart + timedelta(
        days=random.randint(1, 126)
    )

    hesae_pathway_rows.append(
        {
            "patid": patid,
            "aekey": aekey,
            "rttperstart": format_date(rttperstart),
            "rttperend": format_date(rttperend),
        }
    )

hesae_pathway_df = pd.DataFrame(
    hesae_pathway_rows
)




os.makedirs(OUTPUT_DIR, exist_ok=True)

hesae_patient_df.to_csv(
    f"{OUTPUT_DIR}/hesae_patient.csv",
    index=False,
)

hesae_attendance_df.to_csv(
    f"{OUTPUT_DIR}/hesae_attendance.csv",
    index=False,
)

hesae_diagnosis_df.to_csv(
    f"{OUTPUT_DIR}/hesae_diagnosis.csv",
    index=False,
)

hesae_investigation_df.to_csv(
    f"{OUTPUT_DIR}/hesae_investigation.csv",
    index=False,
)

hesae_treatment_df.to_csv(
    f"{OUTPUT_DIR}/hesae_treatment.csv",
    index=False,
)

hesae_hrg_df.to_csv(
    f"{OUTPUT_DIR}/hesae_hrg.csv",
    index=False,
)

hesae_pathway_df.to_csv(
    f"{OUTPUT_DIR}/hesae_pathway.csv",
    index=False,
)

print("HES A&E synthetic data generated")


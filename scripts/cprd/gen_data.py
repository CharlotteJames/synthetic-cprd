

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
    if pd.isna(dt):
        return ""
    return dt.strftime("%d/%m/%Y")



def generate_numeric_text(min_len=6, max_len=19):
    length = random.randint(min_len, max_len)
    return "".join(random.choices("0123456789", k=length))



_patid_seq = {}

def generate_patid(pracid):
    _patid_seq[pracid] = _patid_seq.get(pracid, 0) + 1
    return f"{_patid_seq[pracid]}{str(pracid).zfill(5)}"



def generate_staffid(pracid):
    prefix_len = random.randint(1, 5)
    prefix = "".join(random.choices("0123456789", k=prefix_len))
    return f"{prefix}{str(pracid).zfill(5)}"



# 1. PRACTICE TABLE

practices = []

for i in range(N_PRACTICES):
    pracid = 20000 + i

    lcd = random_date(datetime(2023, 1, 1), datetime(2025, 1, 1))
    uts = random_date(datetime(2000, 1, 1), datetime(2015, 1, 1))

    practices.append(
        {
            "pracid": pracid,
            "lcd": format_date(lcd),
            "uts": format_date(uts),
            "region": random.choice(REGION_VALUES),
        }
    )

practice_df = pd.DataFrame(practices)


# 2. STAFF TABLE

staff_rows = []
staff_ids = []

for _ in range(N_STAFF):
    pracid = random.choice(practice_df["pracid"].tolist())
    staffid = generate_staffid(pracid)

    staff_ids.append(staffid)

    staff_rows.append(
        {
            "staffid": staffid,
            "pracid": pracid,
            "jobcatid": random.choice(JOBCAT_VALUES),
        }
    )

staff_df = pd.DataFrame(staff_rows)


# 3. PATIENT TABLE

patients = []
patient_ids = []

for _ in range(N_PATIENTS):
    pracid = random.choice(practice_df["pracid"].tolist())

    patid = generate_patid(pracid)
    patient_ids.append(patid)

    yob = random.randint(1920, 2024)

    regstart = random_date(datetime(2000, 1, 1), datetime(2023, 1, 1))

    if random.random() < 0.15:
        regend = random_date(regstart, datetime(2025, 1, 1))
    else:
        regend = pd.NaT

    if random.random() < 0.08:
        death_date = random_date(regstart, datetime(2025, 1, 1))
    else:
        death_date = pd.NaT

    candidate_staff = staff_df.loc[staff_df["pracid"] == pracid, "staffid"]

    if len(candidate_staff) > 0:
        usualgpstaffid = random.choice(candidate_staff.tolist())
    else:
        usualgpstaffid = None

    patients.append(
        {
            "patid": patid,
            "pracid": pracid,
            "usualgpstaffid": usualgpstaffid,
            "gender": random.choice(GENDER_VALUES),
            "yob": yob,
            "mob": random.randint(1, 12),
            "emis_ddate": format_date(death_date)
            if pd.notna(death_date)
            else "",
            "regstartdate": format_date(regstart),
            "patienttypeid": random.choice(PATIENT_TYPE_VALUES),
            "regenddate": format_date(regend)
            if pd.notna(regend)
            else "",
            "acceptable": random.choice([0, 1]),
            "cprd_ddate": format_date(death_date)
            if pd.notna(death_date)
            else "",
        }
    )

patient_df = pd.DataFrame(patients)


# 4. CONSULTATION TABLE

consultations = []
consultation_ids = []

for _ in range(N_CONSULTATIONS):
    patient = patient_df.sample(1).iloc[0]

    consid = generate_numeric_text(10, 19)
    consultation_ids.append(consid)

    consdate = random_date(datetime(2010, 1, 1), datetime(2025, 1, 1))
    enterdate = consdate + timedelta(days=random.randint(0, 7))

    candidate_staff = staff_df.loc[
        staff_df["pracid"] == patient["pracid"],
        "staffid",
    ]

    if len(candidate_staff) > 0:
        staffid = random.choice(candidate_staff.tolist())
    else:
        staffid = None

    consultations.append(
        {
            "patid": patient["patid"],
            "consid": consid,
            "pracid": patient["pracid"],
            "consdate": format_date(consdate),
            "enterdate": format_date(enterdate),
            "staffid": staffid,
            "conssourceid": str(random.choice(CONS_SOURCE_VALUES)),
            "cprdconstype": "",
            "consmedcodeid": random.choice(MEDCODE_POOL),
        }
    )

consultation_df = pd.DataFrame(consultations)


# 5. OBSERVATION TABLE

observations = []
observation_ids = []

for _ in range(N_OBSERVATIONS):
    patient = patient_df.sample(1).iloc[0]

    obsid = generate_numeric_text(10, 19)
    observation_ids.append(obsid)

    obsdate = random_date(datetime(2010, 1, 1), datetime(2025, 1, 1))
    enterdate = obsdate + timedelta(days=random.randint(0, 3))

    patient_consults = consultation_df[
        consultation_df["patid"] == patient["patid"]
    ]

    if len(patient_consults) > 0 and random.random() < 0.85:
        consid = patient_consults.sample(1).iloc[0]["consid"]
    else:
        consid = ""

    candidate_staff = staff_df.loc[
        staff_df["pracid"] == patient["pracid"],
        "staffid",
    ]

    if len(candidate_staff) > 0:
        staffid = random.choice(candidate_staff.tolist())
    else:
        staffid = None

    value = round(np.random.normal(100, 20), 3)

    if random.random() < 0.1 and len(observation_ids) > 1:
        parentobsid = random.choice(observation_ids[:-1])
    else:
        parentobsid = ""

    observations.append(
        {
            "patid": patient["patid"],
            "consid": consid,
            "pracid": patient["pracid"],
            "obsid": obsid,
            "obsdate": format_date(obsdate),
            "enterdate": format_date(enterdate),
            "staffid": staffid,
            "parentobsid": parentobsid,
            "medcodeid": random.choice(MEDCODE_POOL),
            "value": value,
            "numunitid": random.choice(NUMUNIT_VALUES),
            "obstypeid": random.choice(OBSTYPE_VALUES),
            "numrangelow": round(value - random.uniform(5, 15), 3),
            "numrangehigh": round(value + random.uniform(5, 15), 3),
            "probobsid": "",
        }
    )

observation_df = pd.DataFrame(observations)


# 6. REFERRAL TABLE

referrals = []

ref_obs = observation_df.sample(N_REFERRALS)

for _, row in ref_obs.iterrows():
    referrals.append(
        {
            "patid": row["patid"],
            "obsid": row["obsid"],
            "pracid": row["pracid"],
            "refsourceorgid": None,
            "reftargetorgid": None,
            "refurgencyid": random.choice(REFURGENCY_VALUES),
            "refservicetypeid": random.choice(REFSERVICETYPE_VALUES),
            "refmodeid": random.choice(REFMODE_VALUES),
        }
    )

referral_df = pd.DataFrame(referrals)


# 7. PROBLEM TABLE

problems = []

problem_obs = observation_df.sample(N_PROBLEMS)

for _, row in problem_obs.iterrows():
    prob_start = random_date(datetime(2010, 1, 1), datetime(2023, 1, 1))
    lastrev = random_date(prob_start, datetime(2025, 1, 1))
    candidate_staff = staff_df.loc[staff_df["pracid"] == row["pracid"], "staffid"]
    lastrevstaffid = random.choice(candidate_staff.tolist()) if len(candidate_staff) > 0 else None

    problems.append(
        {
            "patid": row["patid"],
            "obsid": row["obsid"],
            "pracid": row["pracid"],
            "parentprobobsid": "",
            "probenddate": format_date(random_date(prob_start, datetime(2025, 1, 1)))
                if random.random() < 0.3 else "",
            "expduration": random.randint(1, 365),
            "lastrevdate": format_date(lastrev),
            "lastrevstaffid": lastrevstaffid,
            "parentprobrelid": random.choice(PARENTPROBREL_VALUES),
            "probstatusid": random.choice(PROBSTATUS_VALUES),
            "signid": random.choice(SIGN_VALUES),
        }
    )

problem_df = pd.DataFrame(problems)


# 8. DRUG ISSUE TABLE

drug_issues = []

for _ in range(N_DRUG_ISSUES):
    patient = patient_df.sample(1).iloc[0]

    issue_date = random_date(datetime(2010, 1, 1), datetime(2025, 1, 1))

    issueid = generate_numeric_text(10, 19)

    enter_date = issue_date + timedelta(days=random.randint(0, 3))
    candidate_staff = staff_df.loc[staff_df["pracid"] == patient["pracid"], "staffid"]
    staffid = random.choice(candidate_staff.tolist()) if len(candidate_staff) > 0 else None

    drug_issues.append(
        {
            "patid": patient["patid"],
            "issueid": issueid,
            "pracid": patient["pracid"],
            "probobsid": "",
            "drugrecid": None,
            "issuedate": format_date(issue_date),
            "enterdate": format_date(enter_date),
            "staffid": staffid,
            "prodcodeid": random.choice(PRODCODE_POOL),
            "dosageid": str(random.randint(1, 1000)),
            "quantity": round(random.uniform(1, 90), 2),
            "quantunitid": random.choice(QUANTUNIT_VALUES),
            "duration": random.randint(1, 90),
            "estnhscost": round(random.uniform(0.5, 50.0), 2),
        }
    )


drug_issue_df = pd.DataFrame(drug_issues)

# 9. MEDICAL DICTIONARY TABLE

medical_dictionary_rows = []

for medcodeid, term, snomedctconceptid in MEDICAL_DICTIONARY_TERMS:

    medical_dictionary_rows.append(
        {
            "medcodeid": medcodeid,
            "term": term,
            "originalreadcode": "",
            "cleansedreadcode": "",
            "snomedctconceptid": snomedctconceptid,
            "snomedctdescriptionid": generate_numeric_text(15, 18),
            "release": None,
            "emiscodecategoryid": random.randint(1, 20),
        }
    )

medical_dictionary_df = pd.DataFrame(
    medical_dictionary_rows
)


# 10. PRODUCT DICTIONARY TABLE

product_dictionary_rows = []

for prodcodeid, termfromemis, dmdid in PRODUCT_DICTIONARY_TERMS:

    product_dictionary_rows.append(
        {
            "prodcodeid": prodcodeid,
            "dmdid": dmdid,
            "termfromemis": termfromemis,
            "productname": termfromemis,
            "formulation": random.choice(["Tablet", "Capsule", "Solution", "Inhaler"]),
            "routeofadministration": random.choice(["Oral", "Topical", "Inhaled", "Intravenous"]),
            "drugsubstancename": termfromemis,
            "substancestrength": random.choice(["5mg", "10mg", "20mg", "50mg", "100mg", "500mg", "100mcg", "200mcg"]),
            "bnfchapter": f"{random.randint(1, 15)}.{random.randint(1, 9)}",
            "release": None,
        }
    )

product_dictionary_df = pd.DataFrame(
    product_dictionary_rows
)

# EXPORT FILES

import os

os.makedirs(OUTPUT_DIR, exist_ok=True)

practice_df.to_csv(
    f"{OUTPUT_DIR}/Practice.csv",
    sep=",",
    index=False,
)

staff_df.to_csv(
    f"{OUTPUT_DIR}/Staff.csv",
    sep=",",
    index=False,
)

patient_df.to_csv(
    f"{OUTPUT_DIR}/Patient.csv",
    sep=",",
    index=False,
)

consultation_df.to_csv(
    f"{OUTPUT_DIR}/Consultation.csv",
    sep=",",
    index=False,
)

observation_df.to_csv(
    f"{OUTPUT_DIR}/Observation.csv",
    sep=",",
    index=False,
)

referral_df.to_csv(
    f"{OUTPUT_DIR}/Referral.csv",
    sep=",",
    index=False,
)

problem_df.to_csv(
    f"{OUTPUT_DIR}/Problem.csv",
    sep=",",
    index=False,
)


drug_issue_df.to_csv(
    f"{OUTPUT_DIR}/DrugIssue.csv",
    sep=",",
    index=False,
)

medical_dictionary_df.to_csv(
    f"{OUTPUT_DIR}/MedicalDictionary.csv",
    sep=",",
    index=False,
)

product_dictionary_df.to_csv(
    f"{OUTPUT_DIR}/ProductDictionary.csv",
    sep=",",
    index=False,
)
print("Synthetic CPRD Aurum data generated successfully")
print(f"Files written to: {OUTPUT_DIR}")

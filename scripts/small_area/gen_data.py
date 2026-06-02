
import os
import random

import numpy as np
import pandas as pd
from config import *

random.seed(42)
np.random.seed(42)





def rank_to_quintile(rank):
    return min(5, max(1, int(np.ceil(rank * 5))))



def rank_to_decile(rank):
    return min(10, max(1, int(np.ceil(rank * 10))))



def rank_to_twentile(rank):
    return min(20, max(1, int(np.ceil(rank * 20))))



def correlated_rank(base_rank, noise_scale):
    return float(np.clip(base_rank + np.random.normal(0, noise_scale), 0, 1))



def quantiles(rank):
    """Return (quintile, decile, twentile) from a rank in [0, 1]."""
    return rank_to_quintile(rank), rank_to_decile(rank), rank_to_twentile(rank)




patient_df = pd.read_csv(CPRD_DIR + "Patient.csv", dtype=str)

patids = patient_df["patid"].tolist()
pracids = patient_df["pracid"].tolist()

n = len(patids)

# Base composite deprivation rank for each patient (uniform in [0,1])
# 1 = least deprived, so rank=0 → quintile=1, rank=1 → quintile=5
base_ranks = np.random.uniform(0, 1, size=n)




imdcomposite_rows = []

for i in range(n):

    q5, q10, q20 = quantiles(base_ranks[i])

    imdcomposite_rows.append(
        {
            "patid": patids[i],
            "pracid": pracids[i],
            "e2019_imd_5": q5,
            "e2019_imd_10": q10,
            "e2019_imd_20": q20,
        }
    )

patient_imdcomposite_df = pd.DataFrame(imdcomposite_rows)




IMD_DOMAINS = [
    "income",
    "employment",
    "education",
    "health",
    "crime",
    "access",
    "living_environment",
    "housing",
    "outdoor_environment",
]

imddomains_rows = []

for i in range(n):

    row = {
        "patid": patids[i],
        "pracid": pracids[i],
    }

    for domain in IMD_DOMAINS:

        domain_rank = correlated_rank(
            base_ranks[i], DOMAIN_NOISE_SCALE
        )

        q5, q10, q20 = quantiles(domain_rank)

        row[f"e2019_{domain}_5"] = q5
        row[f"e2019_{domain}_10"] = q10
        row[f"e2019_{domain}_20"] = q20

    imddomains_rows.append(row)

patient_imddomains_df = pd.DataFrame(imddomains_rows)




townsend_rows = []

for i in range(n):

    townsend_rank = correlated_rank(
        base_ranks[i], DOMAIN_NOISE_SCALE
    )

    q5, q10, q20 = quantiles(townsend_rank)

    townsend_rows.append(
        {
            "patid": patids[i],
            "pracid": pracids[i],
            "e2011_townsend_5": q5,
            "e2011_townsend_10": q10,
            "e2011_townsend_20": q20,
        }
    )

patient_townsend_df = pd.DataFrame(townsend_rows)




carstairs_rows = []

for i in range(n):

    carstairs_rank = correlated_rank(
        base_ranks[i], DOMAIN_NOISE_SCALE
    )

    q5, q10, q20 = quantiles(carstairs_rank)

    carstairs_rows.append(
        {
            "patid": patids[i],
            "pracid": pracids[i],
            "e2011_carstairs_5": q5,
            "e2011_carstairs_10": q10,
            "e2011_carstairs_20": q20,
        }
    )

patient_carstairs_df = pd.DataFrame(carstairs_rows)




urbanrural_rows = []

for i in range(n):

    urban = 1 if np.random.random() < URBAN_PROBABILITY else 2

    urbanrural_rows.append(
        {
            "patid": patids[i],
            "pracid": pracids[i],
            "e2011_urbanrural": urban,
        }
    )

patient_urbanrural_df = pd.DataFrame(urbanrural_rows)




os.makedirs(OUTPUT_DIR, exist_ok=True)

patient_imdcomposite_df.to_csv(
    f"{OUTPUT_DIR}/patient_imdcomposite.csv",
    index=False,
)

patient_imddomains_df.to_csv(
    f"{OUTPUT_DIR}/patient_imddomains.csv",
    index=False,
)

patient_townsend_df.to_csv(
    f"{OUTPUT_DIR}/patient_townsend.csv",
    index=False,
)

patient_carstairs_df.to_csv(
    f"{OUTPUT_DIR}/patient_carstairs.csv",
    index=False,
)

patient_urbanrural_df.to_csv(
    f"{OUTPUT_DIR}/patient_urbanrural.csv",
    index=False,
)

print(f"Small area data generated for {n} patients")

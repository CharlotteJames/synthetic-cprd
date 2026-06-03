import os
import sqlite3

DATABASES = [
    "../data/cprd/cprd.db",
    "../data/hes_apc/hes_apc.db",
    "../data/hes_ae/hes_ae.db",
    "../data/hes_op/hes_op.db",
    "../data/small_area/small_area.db",
]

OUTPUT_DB = "data/synthetic_cprd.db"


def main():
    if os.path.exists(OUTPUT_DB):
        os.remove(OUTPUT_DB)

    out_con = sqlite3.connect(OUTPUT_DB)

    for db_path in DATABASES:
        if not os.path.exists(db_path):
            print(f"Skipping {db_path} (not found)")
            continue

        alias = os.path.splitext(os.path.basename(db_path))[0]
        out_con.execute(f"ATTACH DATABASE '{db_path}' AS src")

        tables = out_con.execute(
            "SELECT name FROM src.sqlite_master WHERE type='table'"
        ).fetchall()

        for (table,) in tables:
            print(f"  {alias}.{table}")
            out_con.execute(f"CREATE TABLE IF NOT EXISTS [{table}] AS SELECT * FROM src.[{table}]")

        out_con.execute("DETACH DATABASE src")
        out_con.commit()

    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_Patient_patid            ON Patient(patid)",
        "CREATE INDEX IF NOT EXISTS idx_Observation_patid        ON Observation(patid)",
        "CREATE INDEX IF NOT EXISTS idx_Observation_medcodeid    ON Observation(medcodeid)",
        "CREATE INDEX IF NOT EXISTS idx_DrugIssue_patid          ON DrugIssue(patid)",
        "CREATE INDEX IF NOT EXISTS idx_DrugIssue_prodcodeid     ON DrugIssue(prodcodeid)",
        "CREATE INDEX IF NOT EXISTS idx_hes_hospital_patid       ON hes_hospital(patid)",
        "CREATE INDEX IF NOT EXISTS idx_hes_hospital_epikey      ON hes_hospital(epikey)",
        "CREATE INDEX IF NOT EXISTS idx_hes_diagnosis_epikey     ON hes_diagnosis(epikey)",
        "CREATE INDEX IF NOT EXISTS idx_hes_diagnosis_diagcode   ON hes_diagnosis(diagcode)",
        "CREATE INDEX IF NOT EXISTS idx_hes_procedure_epikey     ON hes_procedure(epikey)",
        "CREATE INDEX IF NOT EXISTS idx_hesae_attendance_patid   ON hesae_attendance(patid)",
        "CREATE INDEX IF NOT EXISTS idx_hesae_diagnosis_patid    ON hesae_diagnosis(patid)",
    ]
    for ddl in indexes:
        out_con.execute(ddl)
    out_con.commit()

    out_con.close()
    print(f"\nUnified database written to {OUTPUT_DB}")


if __name__ == "__main__":
    main()

"""
Combines all synthetic CPRD/HES/small-area SQLite databases into a single
unified database at data/synthetic_cprd.db, ready for use with CPRDBackend.

Must be run from the synthetic-cprd repository root.
Databases are copied in order; tables from later databases silently overwrite
earlier ones if names clash (none currently do).
"""

import os
import sqlite3

DATABASES = [
    "data/cprd/cprd.db",
    "data/hes_apc/hes_apc.db",
    "data/hes_ae/hes_ae.db",
    "data/hes_op/hes_op.db",
    "data/small_area/small_area.db",
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

    out_con.close()
    print(f"\nUnified database written to {OUTPUT_DB}")


if __name__ == "__main__":
    main()

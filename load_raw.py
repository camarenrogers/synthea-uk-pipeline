import duckdb
from pathlib import Path

CSV_DIR = Path("/Users/camarenrogers/synthea/output/csv")
DB_PATH = "synthea.duckdb"

# Diagnostic: confirm the folder and files exist BEFORE loading
print("Looking in:", CSV_DIR)
print("Folder exists:", CSV_DIR.exists())
csv_files = sorted(CSV_DIR.glob("*.csv"))
print("CSV files found:", len(csv_files))

con = duckdb.connect(DB_PATH)
con.execute("CREATE SCHEMA IF NOT EXISTS raw;")

for csv_file in csv_files:
    table = csv_file.stem
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.{table} AS
        SELECT * FROM read_csv_auto('{csv_file}', header=true);
    """)
    count = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
    print(f"Loaded raw.{table:15} {count:>6} rows")

con.close()
print("\nDone. Warehouse written to", DB_PATH)
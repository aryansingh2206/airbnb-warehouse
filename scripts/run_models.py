import duckdb
from pathlib import Path

con = duckdb.connect("warehouse.db")

sql_dir = Path("models/sql")

for sql_file in sql_dir.glob("*.sql"):
    print("Running:", sql_file.name)
    con.execute(sql_file.read_text())

print("All models built.")

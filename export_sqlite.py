import sqlite3
import pandas as pd

# ✅ Connect to SQLite database
sqlite_conn = sqlite3.connect("divine.db")
cursor = sqlite_conn.cursor()

# ✅ Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# ✅ Export each table as a JSON file
for table in tables:
    table_name = table[0]

    try:
        # Wrap table names in brackets to avoid SQL reserved keyword issues
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', sqlite_conn)

        # Save as JSON file
        df.to_json(f"{table_name}.json", orient="records", indent=4)
        print(f"✅ Exported {table_name} to {table_name}.json")
    except Exception as e:
        print(f"❌ Failed to export {table_name}: {e}")

sqlite_conn.close()

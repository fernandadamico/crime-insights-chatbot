import pandas as pd
import sqlite3
import os

csv_path = "data/crimes_chicago.csv"
df = pd.read_csv(csv_path)

db_path = "data/crimes.db"
conn = sqlite3.connect(db_path)

df.to_sql("crimes", conn, if_exists="replace", index=False)

conn.close()

print(f"SQLite database created at: {os.path.abspath(db_path)}")
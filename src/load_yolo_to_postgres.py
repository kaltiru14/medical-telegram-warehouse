import pandas as pd
import psycopg2

# --------------------------
# DATABASE CONFIG
# --------------------------
DB_CONFIG = {
    "host": "localhost",
    "dbname": "medical_telegram",   # from profiles.yml
    "user": "postgres",
    "password": "postgres123",
    "port": 5432
}

CSV_PATH = "data/processed/yolo_detections_classified.csv"

# --------------------------
# LOAD CSV
# --------------------------
df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows from CSV")

# --------------------------
# CONNECT TO POSTGRES
# --------------------------
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# --------------------------
# ENSURE SCHEMA EXISTS
# --------------------------
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
""")

# --------------------------
# CREATE TABLE IF NOT EXISTS
# --------------------------
cur.execute("""
    CREATE TABLE IF NOT EXISTS raw.yolo_detections (
        image_name TEXT,
        detected_class TEXT,
        confidence_score FLOAT,
        image_category TEXT
    );
""")

conn.commit()

# --------------------------
# INSERT DATA
# --------------------------
insert_sql = """
    INSERT INTO raw.yolo_detections (
        image_name,
        detected_class,
        confidence_score,
        image_category
    )
    VALUES (%s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cur.execute(
        insert_sql,
        (
            row["image_name"],
            row["detected_class"],
            row["confidence_score"],
            row["image_category"]
        )
    )

conn.commit()

cur.close()
conn.close()

print("✅ YOLO detections successfully loaded into raw.yolo_detections")

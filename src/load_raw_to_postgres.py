import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "medical_telegram")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")

# -------------------------------------------------
# Paths
# -------------------------------------------------
RAW_DATA_PATH = Path("data/raw/telegram_messages")

# -------------------------------------------------
# Connect to PostgreSQL
# -------------------------------------------------
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

# -------------------------------------------------
# Create schema and table if not exists
# -------------------------------------------------
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN,
    image_path TEXT,
    views INT,
    forwards INT
)
""")
conn.commit()

# -------------------------------------------------
# Load JSON files
# -------------------------------------------------
for file_path in RAW_DATA_PATH.glob("*.json"):
    print(f"Processing {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

        for msg in messages:
            # Insert into table
            cur.execute("""
                INSERT INTO raw.telegram_messages (
                    message_id,
                    channel_name,
                    message_date,
                    message_text,
                    has_media,
                    image_path,
                    views,
                    forwards
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (message_id) DO NOTHING
            """, (
                msg.get("message_id"),
                msg.get("channel_name"),
                msg.get("message_date"),
                msg.get("message_text"),
                msg.get("has_media"),
                msg.get("image_path"),
                msg.get("views"),
                msg.get("forwards")
            ))

conn.commit()
cur.close()
conn.close()
print("All messages loaded successfully!")

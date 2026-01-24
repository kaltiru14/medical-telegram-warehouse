import pandas as pd
import psycopg2

# --------------------------
# DB connection
# --------------------------
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'medical_telegram',  # your DB name
    'user': 'postgres',
    'password': 'postgres123',
    'port': 5432
}

conn = psycopg2.connect(**DB_CONFIG)

# --------------------------
# Load YOLO fact table
# --------------------------
query = """
SELECT f.message_id, f.channel_key, f.date_key, f.detected_class,
       f.confidence_score, f.image_category, m.view_count
FROM marts.fct_image_detections f
JOIN marts.fct_messages m
  ON f.message_id = m.message_id
"""
df = pd.read_sql(query, conn)
conn.close()

# --------------------------
# Analysis 1: Average views by image_category
# --------------------------
avg_views = df.groupby('image_category')['view_count'].mean().sort_values(ascending=False)
print("Average views by image category:\n", avg_views)

# --------------------------
# Analysis 2: Visual content per channel
# --------------------------
visual_df = df[df['image_category'] != 'other']  # only messages with images
channel_visual = visual_df.groupby('channel_key')['message_id'].count().sort_values(ascending=False)
print("\nNumber of visual posts per channel:\n", channel_visual)

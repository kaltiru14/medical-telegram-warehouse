# src/yolo_detect.py

import os
from glob import glob
import pandas as pd
from ultralytics import YOLO

# --------------------------
# CONFIG
# --------------------------
IMAGE_FOLDER = r"data/raw/images"
OUTPUT_CSV = r"data/processed/yolo_detections_classified.csv"
MODEL_PATH = "yolov8n.pt"

# --------------------------
# LOAD YOLO MODEL
# --------------------------
model = YOLO(MODEL_PATH)

# --------------------------
# HELPER: CLASSIFY IMAGE
# --------------------------
def classify_image(df_group):
    """Classify an image based on detected objects"""
    # Ignore None
    objects = df_group['detected_class'].dropna().tolist()

    if 'person' in objects and any(obj in objects for obj in ['bottle', 'container']):
        category = 'promotional'
    elif any(obj in objects for obj in ['bottle', 'container']):
        category = 'product_display'
    elif 'person' in objects:
        category = 'lifestyle'
    else:
        category = 'other'

    df_group['image_category'] = category
    return df_group

# --------------------------
# SCAN IMAGES
# --------------------------
image_paths = glob(os.path.join(IMAGE_FOLDER, "*", "*.jpg"))

all_detections = []

for img_path in image_paths:
    try:
        results = model(img_path)
        for result in results:
            boxes = result.boxes
            if boxes is None or len(boxes) == 0:
                # No detections
                all_detections.append({
                    'image_name': os.path.basename(img_path),
                    'detected_class': None,
                    'confidence_score': 0.0
                })
            else:
                # Corrected: confidence for each detection
                for cls, conf in zip(boxes.cls, boxes.conf):
                    detected_class = model.names[int(cls)]
                    confidence_score = float(conf.item())
                    all_detections.append({
                        'image_name': os.path.basename(img_path),
                        'detected_class': detected_class,
                        'confidence_score': confidence_score
                    })
        print(f"Processed: {img_path}")
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

# --------------------------
# SAVE CSV WITH CLASSIFICATION
# --------------------------
df = pd.DataFrame(all_detections)
df = df.groupby("image_name").apply(classify_image).reset_index(drop=True)

# ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)

print(f"YOLO detections saved to {OUTPUT_CSV}")

{{ config(materialized='view') }}

select
    image_name,
    detected_class,
    confidence_score,
    image_category
from {{ source('raw', 'yolo_detections') }}

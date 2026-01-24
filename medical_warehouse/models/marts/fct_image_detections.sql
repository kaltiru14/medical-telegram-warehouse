-- models/marts/fct_image_detections.sql
-- Fact table integrating YOLO image detections with messages

WITH yolo AS (
    SELECT
        image_name,
        detected_class,
        confidence_score,
        image_category
    FROM raw.yolo_detections
),

messages AS (
    SELECT
        message_id,
        channel_key,
        date_key,
        image_name
    FROM fct_messages
)

SELECT
    m.message_id,
    m.channel_key,
    m.date_key,
    y.detected_class,
    y.confidence_score,
    y.image_category
FROM messages m
LEFT JOIN yolo y
    ON m.image_name = y.image_name
;

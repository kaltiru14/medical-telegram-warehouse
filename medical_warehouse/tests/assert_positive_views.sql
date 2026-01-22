-- This test ensures all view counts are non-negative
SELECT *
FROM {{ ref('stg_telegram_messages') }}
WHERE views < 0

-- This test ensures no messages have a date in the future
SELECT *
FROM {{ ref('stg_telegram_messages') }}
WHERE message_date > CURRENT_DATE

select
    m.message_id,
    c.channel_key,
    d.date_key,
    m.message_text,
    m.message_length,
    m.views as view_count,
    m.forwards as forward_count,
    m.has_image
from {{ ref('stg_telegram_messages') }} m
join {{ ref('dim_channels') }} c
    on m.channel_name = c.channel_name
join {{ ref('dim_dates') }} d
    on date_trunc('day', m.message_date) = d.full_date

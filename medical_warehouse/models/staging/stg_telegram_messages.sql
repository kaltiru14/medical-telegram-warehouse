with raw as (

    select *
    from raw.telegram_messages

)

select
    message_id,
    channel_name,
    message_date::timestamp as message_date,
    message_text,
    has_media,
    image_path,
    views::int as views,
    forwards::int as forwards,
    char_length(message_text) as message_length,
    case when has_media then 1 else 0 end as has_image
from raw
where message_text is not null

"""
Telegram Scraper for Ethiopian Medical Channels

NOTE:
This scraper is for reproducibility and documentation purposes.
Production data may come from shared datasets; this script demonstrates
the correct extraction logic and data lake structure using Telethon.
"""

import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# -------------------------------------------------
# Channel Configuration
# Keys must match folder names
# -------------------------------------------------
CHANNELS = {
    "CheMed": "chemed",
    "Doctors_Online": "DoctorsOnline",
    "Lobelia_pharmacy_and_cosmetics": "lobelia4cosmetics",
    "Medical_Information-_ጤና_መረጃ": "medical_information",
    "Tikvah__Pharma": "tikvahpharma"
}

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DATA_PATH = Path("data/raw")
IMAGE_PATH = BASE_DATA_PATH / "images"
MESSAGE_PATH = BASE_DATA_PATH / "telegram_messages"
LOG_PATH = Path("logs")

# -------------------------------------------------
# Create required directories
# -------------------------------------------------
IMAGE_PATH.mkdir(parents=True, exist_ok=True)
MESSAGE_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(exist_ok=True)

# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------
logging.basicConfig(
    filename=LOG_PATH / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def serialize_message(message, channel_name, image_file=None):
    return {
        "message_id": message.id,
        "channel_name": channel_name,
        "message_date": message.date.isoformat() if message.date else None,
        "message_text": message.text,
        "has_media": bool(message.media),
        "image_path": image_file,
        "views": message.views,
        "forwards": message.forwards
    }

# -------------------------------------------------
# Scraper Function
# -------------------------------------------------
async def scrape_channel(client, channel_name, channel_username):
    # Timezone-aware UTC datetime
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily_path = MESSAGE_PATH / today
    daily_path.mkdir(parents=True, exist_ok=True)

    channel_image_dir = IMAGE_PATH / channel_name
    channel_image_dir.mkdir(parents=True, exist_ok=True)

    messages_data = []

    logging.info(f"Starting scrape for channel: {channel_name}")

    try:
        async for message in client.iter_messages(channel_username, limit=500):
            image_file = None

            # Download image if message contains a photo
            if isinstance(message.media, MessageMediaPhoto):
                image_file = channel_image_dir / f"{message.id}.jpg"
                # await client.download_media(message.photo, image_file)  # Uncomment if you want to download

            msg_record = serialize_message(
                message,
                channel_name,
                str(image_file) if image_file else None
            )
            messages_data.append(msg_record)

        # Save JSON file
        output_file = daily_path / f"{channel_name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

        logging.info(
            f"Completed scrape for {channel_name}. Messages collected: {len(messages_data)}"
        )

    except Exception as e:
        logging.error(f"Error scraping {channel_name}: {str(e)}")

# -------------------------------------------------
# Entry Point
# -------------------------------------------------
async def main():
    async with TelegramClient("telegram_session", API_ID, API_HASH) as client:
        for channel_name, channel_username in CHANNELS.items():
            await scrape_channel(client, channel_name, channel_username)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

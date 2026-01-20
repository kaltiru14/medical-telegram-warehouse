# medical-telegram-warehouse# Task 1 – Data Scraping and Collection (Extract & Load)

## Overview

This task demonstrates a **reproducible data scraping pipeline** for Ethiopian medical Telegram channels. The objective is to extract **messages and images**, structure them in a **data lake**, and document the workflow for Task 2 transformations.

## Channels

The scraper is configured for the following channels:

| Channel Name | Telegram Username |
|--------------|-----------------|
| CheMed | `chemed` |
| Doctors_Online | `DoctorsOnline` |
| Lobelia_pharmacy_and_cosmetics | `lobelia4cosmetics` |
| Medical_Information-_ጤና_መረጃ | `medical_information` |
| Tikvah__Pharma | `tikvahpharma` |

---

## Data Lake Structure

Messages and images are organized as follows:



data/raw/
├── telegram_messages/YYYY-MM-DD/{channel_name}.json
└── images/{channel_name}/{message_id}.jpg


### Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```
2. Add .env with your Telegram API credentials:

```bash 
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```
3. Run the scraper:
```bash
python src/scraper.py
```
## Notes
- The scraper is designed to be idempotent. It can be run multiple times without overwriting previous data (creates new folders per date).
- Images download is optional if the media already exists.

## Deliverables
- src/scraper.py – working scraper script
- Raw JSON files in data/raw/telegram_messages/YYYY-MM-DD/
- Downloaded images organized by channel in data/raw/images/
- Log file in logs/scraper.log

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
Task 2 – Data Modeling and Transformation (Transform)
=====================================================

Objective
---------

Transform raw, messy data into a clean, structured data warehouse using **dbt** and **dimensional modeling**.

This task ensures:

*   Raw data is cleaned and standardized.
    
*   A **star schema** is created for analytics.
    
*   Data quality is enforced using **dbt tests**.
    
*   The system is modular, maintainable, and scalable.
    

1\. Load Raw Data to PostgreSQL
-------------------------------

*   Wrote a Python script load\_raw\_to\_postgres.py to:
    
    *   Read JSON files from the data lake (data/raw/telegram\_messages).
        
    *   Load them into the raw schema in PostgreSQL.
        
    *   Create the table raw.telegram\_messages with all scraped fields.
    *   Verified data was successfully loaded into PostgreSQL.

2\. Initialize dbt Project
-------------------------------

*   Installed dbt:
```bash 
pip install dbt-postgres 
```
*   Initialized the project:
```bash
dbt init medical_warehouse
```
* Configured profiles.yml to connect to PostgreSQL (database: medical_telegram, schema: staging).
*   Created the standard dbt project structure.

3\. Staging Models
-------------------------------
Created staging models to clean and standardize raw data in models/staging/:
* Casted types (timestamp, int, boolean).
* Filtered invalid records (message_text IS NOT NULL).
* Added calculated fields:
    * message_length – character length of message.
    * has_image – flag for messages with media.

4\. Dimensional Modeling – Star Schema
-------------------------------
### Dimension Tables (models/marts/):
1\. dim_channels – Telegram channel information
* channel_key (surrogate key)
* channel_name, channel_type
* first_post_date last_post_date
* total_posts, avg_views

2\. dim_dates – Date dimension for time-based analysis
* date_key
* full_date, day_of_week, week_of_year, month, quarter, year
* is_weekend
### Fact Table:
fct_messages – One row per message
* message_id
* channel_key (FK to dim_channels)
* date_key (FK to dim_dates)
* message_text, message_length
* views, forwards
* has_image

4\. dbt Tests
---------------------------------------
### Standard dbt tests implemented:
*   Unique and Not Null for primary keys and critical columns.
*   Relationships tests for foreign keys

All standard tests passed successfully:
```bash
dbt test
```
### Custom Data Test:
1. assert_no_future_messages.sql – Ensures no messages have future dates:
```sql 
select *
from {{ ref('stg_telegram_messages') }}
where message_date > CURRENT_DATE
```
6\. Documentation
-------------------------------
*    Generated dbt documentation:
```bash
dbt docs generate
dbt docs serve
```
* Added descriptions to all models and columns in schema.yml.
*   Documentation available at: http://localhost:8080.

7\. Summary
-------------------------------
- Raw data loaded into PostgreSQL.
- Staging models created to clean and standardize data.
- Star schema designed with dimension and fact tables.
- dbt tests (standard + custom) validate data quality.
- Documentation generated for models and fields.
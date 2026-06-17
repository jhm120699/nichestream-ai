# NicheStream AI Scraper Service

This directory contains the programmatic data ingestion pipeline for NicheStream AI.

## Files
- `scraper.py`: The main Python script that fetches trending software/SaaS products from Indie Hackers via their Algolia API and saves them to the shared team database.
- `requirements.txt`: Python dependencies.

## Usage
To run the scraper:
```bash
/home/team/shared/nichestream-ai/venv/bin/python3 scraper.py
```

## How it works
1. It queries the Indie Hackers Algolia index for products matching specific verticals (productivity, marketing, programming, design, finance).
2. It extracts metadata including name, tagline, description, and website URL.
3. It maps `_tags` to product features.
4. It saves the data to the `products`, `product_features`, and `product_pros` tables using the `team-db` CLI.
5. It is idempotent: it checks if a product already exists before inserting.

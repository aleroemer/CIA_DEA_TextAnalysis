# UCSB Presidency Project - Reagan Nicaragua Discourse Scraper

## Research Question
Analyzing President Reagan's public discourse on Nicaragua during the 1980s, specifically examining the balance between counternarcotics and counterinsurgency rhetoric.

## Project Overview
This project scrapes speeches and documents from the UCSB American Presidency Project database to build a corpus for text analysis research on CIA and DEA operations in Central America.

## Search Parameters
- **Keywords**: "Nicaragua"
- **President**: Ronald Reagan (ID: 200296)
- **Total Results**: 447 documents
- **Source**: https://www.presidency.ucsb.edu/

## Project Structure
```
ucsb_scraping/
├── scripts/                    # Scraping scripts (run in order)
│   ├── 01_explore_html.py     # HTML structure exploration
│   ├── 02_scrape_search_results.py  # Extract search results metadata
│   ├── 03_scrape_documents.py       # Download full document texts
│   └── 04_validate_data.py          # Quality control checks
├── data/
│   ├── raw_texts/             # Individual .txt files (one per document)
│   └── metadata.csv           # Metadata for all documents
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## File Naming Convention
Documents are saved with the format: `YYYY-MM-DD_reagan_nicaragua_XXX.txt`

Example: `1982-11-30_reagan_nicaragua_001.txt`

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run scripts in numerical order:

```bash
# Step 1: Explore HTML structure
python scripts/01_explore_html.py

# Step 2: Scrape search results and create metadata CSV
python scripts/02_scrape_search_results.py

# Step 3: Download full text of all documents
python scripts/03_scrape_documents.py

# Step 4: Validate data collection
python scripts/04_validate_data.py
```

## Metadata Fields
The metadata.csv file contains:
- `filename`: Name of the .txt file
- `title`: Document title
- `date`: Publication date (YYYY-MM-DD format)
- `president`: President name
- `url`: Source URL
- `category`: Document type/category
- `preview_text`: Brief excerpt from search results

## Research Context
Part of a larger project examining CIA and DEA operations in Mexico and Central America during the 1980s, focusing on how these agencies managed conflicting mandates of counterinsurgency vs. counternarcotics.

## Academic Use
This data collection is for academic research purposes. The UCSB American Presidency Project is a publicly accessible archive maintained for scholarly use.

## Author
Programming for the Humanist - Midterm Project
University of Chicago

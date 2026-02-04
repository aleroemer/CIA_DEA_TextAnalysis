"""
Step 1: HTML Structure Exploration for UCSB Presidency Project

This script explores the HTML structure of the UCSB search results page
to identify the CSS selectors we need for scraping document metadata.

Purpose: Understanding the website structure before building the scraper
Author: Programming for the Humanist - Midterm Project
"""

import requests
from bs4 import BeautifulSoup
from pprint import pprint

# =============================================================================
# CONFIGURATION
# =============================================================================

# URL for the first page of search results
# Search parameters: Nicaragua + Reagan + specific document categories
SEARCH_URL = "https://www.presidency.ucsb.edu/advanced-search?field-keywords=Nicaragua&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=200296&category2%5B%5D=406&category2%5B%5D=58&category2%5B%5D=69&category2%5B%5D=8&category2%5B%5D=82&category2%5B%5D=84&category2%5B%5D=59&category2%5B%5D=45&category2%5B%5D=63&items_per_page=25"

# =============================================================================
# FETCH PAGE
# =============================================================================

print("=" * 80)
print("UCSB Presidency Project - HTML Structure Exploration")
print("=" * 80)
print(f"\nFetching: {SEARCH_URL}\n")

# Make HTTP request to get the page
# The 'headers' parameter makes our request look like it's coming from a browser
# This helps avoid being blocked by the server
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

response = requests.get(SEARCH_URL, headers=headers)

# Check if the request was successful (status code 200 means OK)
if response.status_code == 200:
    print(f"✓ Successfully fetched page (Status: {response.status_code})")
else:
    print(f"✗ Failed to fetch page (Status: {response.status_code})")
    exit(1)

# =============================================================================
# PARSE HTML
# =============================================================================

# Parse the HTML content using BeautifulSoup
# 'lxml' is a fast HTML parser
soup = BeautifulSoup(response.content, 'lxml')

print("\n" + "=" * 80)
print("ANALYZING HTML STRUCTURE")
print("=" * 80)

# =============================================================================
# 1. FIND TOTAL NUMBER OF RESULTS
# =============================================================================

print("\n[1] Total Results Count")
print("-" * 80)

# Look for text that indicates total number of results
# The page usually displays something like "Showing 1-25 of 447 results"
results_info = soup.find('h3', class_='results-count')
if results_info:
    print(f"Results info found: {results_info.get_text(strip=True)}")
else:
    print("Could not find results count")

# =============================================================================
# 2. FIND ALL SEARCH RESULT ROWS
# =============================================================================

print("\n[2] Extracting Search Results")
print("-" * 80)

# Find all <tr> elements that contain search results
# Strategy: Find rows that have the specific td cells we need (date, president, title)
all_rows = soup.find_all('tr')

# Filter to only rows that have our required cells
result_rows = []
for row in all_rows:
    # Check if this row has the cells we need
    has_date = row.find('td', class_='views-field-field-docs-start-date-time-value')
    has_title = row.find('td', class_='views-field-title')
    if has_date and has_title:
        result_rows.append(row)

all_rows = result_rows

print(f"Found {len(all_rows)} search result rows\n")

if all_rows:
    # Examine the first 3 results in detail
    for i, row in enumerate(all_rows[:3]):
        print(f"\n--- Result {i+1} ---")

        # Extract date
        date_cell = row.find('td', class_='views-field-field-docs-start-date-time-value')
        if date_cell:
            date = date_cell.get_text(strip=True)
            print(f"Date: {date}")

        # Extract president
        president_cell = row.find('td', class_='views-field-field-docs-person')
        if president_cell:
            president = president_cell.get_text(strip=True)
            print(f"President: {president}")

        # Extract title and URL
        title_cell = row.find('td', class_='views-field-title')
        if title_cell:
            link = title_cell.find('a')
            if link:
                title = link.get_text(strip=True)
                url = link.get('href')
                # Make URL absolute
                if url and not url.startswith('http'):
                    url = 'https://www.presidency.ucsb.edu' + url
                print(f"Title: {title}")
                print(f"URL: {url}")

            # Extract preview text (the snippet showing keyword in context)
            # Remove the link text to get just the preview
            preview = title_cell.get_text(strip=True)
            preview = preview.replace(title, '').strip()
            if preview:
                print(f"Preview: {preview[:100]}...")

        print("-" * 80)

    print(f"\n✓ Successfully extracted {len(all_rows)} results from this page")
else:
    print("No search result rows found!")

# =============================================================================
# 3. PAGINATION INFORMATION
# =============================================================================

print("\n[3] Pagination Structure")
print("-" * 80)

# Find pagination elements
pagination = soup.find('nav', class_='pager')
if not pagination:
    pagination = soup.find('ul', class_='pagination')

if pagination:
    print("Pagination found!")

    # Look for "next" button
    next_button = pagination.find('a', rel='next')
    if next_button:
        next_url = next_button.get('href')
        if next_url and not next_url.startswith('http'):
            next_url = 'https://www.presidency.ucsb.edu' + next_url
        print(f"Next page URL: {next_url}")

    # Look for page numbers
    page_links = pagination.find_all('a')
    print(f"Total pagination links found: {len(page_links)}")

else:
    print("Could not find pagination elements")

# =============================================================================
# 4. SUMMARY OF CSS SELECTORS TO USE
# =============================================================================

print("\n" + "=" * 80)
print("SUMMARY: CSS SELECTORS FOR SCRAPING")
print("=" * 80)

selectors = {
    'Results container': 'tr.views-row or div.views-row',
    'Title & Link': 'a (first link in result)',
    'Date': 'td.views-field-field-docs-start-date-time-value',
    'President': 'td.views-field-field-docs-person',
    'Next page': 'a[rel="next"]',
}

for element, selector in selectors.items():
    print(f"{element:20s}: {selector}")

print("\n" + "=" * 80)
print("Exploration complete! Ready to build the scraper.")
print("=" * 80)

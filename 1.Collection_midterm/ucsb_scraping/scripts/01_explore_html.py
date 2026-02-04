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
# 2. EXAMINE ONE SEARCH RESULT ITEM
# =============================================================================

print("\n[2] Individual Search Result Structure")
print("-" * 80)

# Find all search result items
# Each result is typically in a <tr> (table row) or <div> with a specific class
results = soup.find_all('tr', class_='views-row')

if results:
    print(f"Found {len(results)} search results on this page\n")

    # Examine the first result in detail
    first_result = results[0]
    print("Examining first result:")
    print("-" * 40)

    # Extract document title and link
    title_tag = first_result.find('a')
    if title_tag:
        title = title_tag.get_text(strip=True)
        url = title_tag.get('href')
        # If URL is relative, make it absolute
        if url and not url.startswith('http'):
            url = 'https://www.presidency.ucsb.edu' + url
        print(f"Title: {title}")
        print(f"URL: {url}")

    # Extract date
    date_tag = first_result.find('td', class_='views-field-field-docs-start-date-time-value')
    if date_tag:
        date = date_tag.get_text(strip=True)
        print(f"Date: {date}")

    # Extract president name
    president_tag = first_result.find('td', class_='views-field-field-docs-person')
    if president_tag:
        president = president_tag.get_text(strip=True)
        print(f"President: {president}")

    # Show the raw HTML of first result for reference
    print("\nRaw HTML of first result (first 500 chars):")
    print("-" * 40)
    print(str(first_result)[:500] + "...")

else:
    print("Could not find search results. The HTML structure might be different.")
    print("Let's look for other possible containers...")

    # Alternative: look for results in a different structure
    alt_results = soup.find_all('div', class_='views-row')
    if alt_results:
        print(f"Found {len(alt_results)} results in alternative structure")

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

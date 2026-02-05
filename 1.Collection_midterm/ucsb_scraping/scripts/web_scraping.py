import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import os

# The URL I want to scrape
url = "https://www.presidency.ucsb.edu/advanced-search?field-keywords=Nicaragua&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=200296&category2%5B%5D=406&category2%5B%5D=58&category2%5B%5D=69&category2%5B%5D=8&category2%5B%5D=82&category2%5B%5D=84&category2%5B%5D=59&category2%5B%5D=45&category2%5B%5D=63&items_per_page=25"

 # Fetch the web page
response = requests.get(url)

with open("ucsb_search.html", "w", encoding="utf-8") as f:
    f.write(response.text)

# read from the saved file
with open("ucsb_search.html", "r", encoding="utf-8") as html_file:
    html_content = html_file.read()

# Parse html content
soup = BeautifulSoup(html_content, "html.parser")

# Create directory to save Reagan Nicaragua speeches
os.makedirs("reagan_Nicaragua", exist_ok = True)

# Get all rows
all_rows = soup.find_all('tr')

# Create empty list to store result rows
result_rows = []

# Loop through and filter
for row in all_rows:
    date_cell = row.find('td', class_='views-field-field-docs-start-date-time-value')
    title_cell = row.find('td', class_='views-field-title')
    if date_cell and title_cell:
        result_rows.append(row)  
print(f"Found {len(result_rows)} search results")


# Create empty list to store all documents 
documents = []

# Loop through each result row
for row in result_rows:
    # extract dates
    date_cell = row.find('td', class_='views-field-field-docs-start-date-time-value')
    date = date_cell.text.strip() 
    # extract titles and links
    title_cell = row.find('td', class_='views-field-title')
    link_tag = title_cell.find('a') 
    title = link_tag.text.strip()
    url_path = link_tag["href"] 

    #build full URL
    full_url = "https://www.presidency.ucsb.edu" + url_path

    #store in directory 
    doc = {
        'date': date, 
        'title': title, 
        'url': full_url
    }
    documents.append(doc)

# Print first 3 to check
print(f"\nExtracted {len(documents)} documents\n")
for i in range(3):
    print(f"{i+1}. {documents[i]['date']} - {documents[i]['title'][:50]}...")

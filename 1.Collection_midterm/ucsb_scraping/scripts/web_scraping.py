import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import os
import time


# The URL I want to scrape
base_url = "https://www.presidency.ucsb.edu/advanced-search?field-keywords=Nicaragua&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=200296&items_per_page=25"


# ========== Function for scraping website metadata =====================
# == Title, President, Date

def scraping_page(url): 
    # Fetch page
    response = requests.get(url)
    print(f"DEBUG: Fetched {len(response.text)} characters")
    print(f"DEBUG: Status {response.status_code}")
    print(f"DEBUG: URL: {url}")  # Check what URL we're actually fetching


    #create html object
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
        president_cell = row.find('td', class_='views-field-field-docs-person')
        if date_cell and title_cell and president_cell:
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
        # extract president name
        president_cell = row.find('td', class_ ='views-field-field-docs-person')
        president = president_cell.text.strip() 

        #build full URL
        full_url = "https://www.presidency.ucsb.edu" + url_path

        #store in directory 
        doc = {
            'date': date, 
            'title': title, 
            'url': full_url,
            'president': president  
        }
        documents.append(doc)
    
    return(documents)

    # Print first 3 to check
    #print(f"\nExtracted {len(documents)} documents\n")
    #for i in range(min(3, len(documents))):
    #    print(f"{i+1}. {documents[i]['date']} - {documents[i]['title'][:50]}...")


# Looping over all search =================
all_documents = []

for page_num in range(20): 
    if page_num == 0:
        url = base_url
    else: 
        url = base_url + f"&page={page_num}"

    print(f"Scraping page {page_num}...")
    
    #call function
    page_docs = scraping_page(url) 
    all_documents.extend(page_docs)

    # Wait between requests
    time.sleep(2)

print(f"Total: {len(all_documents)} documents") # add to list

# Get text within each link                                                       
print("\n" + "="*80)               
print("SAMPLE OF COLLECTED METADATA")
print("="*80)

for i in range(-3, 0):
    doc = all_documents[i]
    print(f"\nDate: {doc['date']}")
    print(f"Title: {doc['title']}")
    print(f"President: {doc['president']}")

# Convert to pandas Dataframe
df = pd.DataFrame(all_documents)
os.makedirs('data', exist_ok=True)
df.to_csv('data/metadata.csv', index=False, encoding='utf-8')


import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# Load metadata
df = pd.read_csv('data/metadata.csv')
print(f"Loaded {len(df)} documents\n")

# Create directory for text files
os.makedirs('data/raw_texts', exist_ok=True)

# Loop through all documents
for index, row in df.iterrows():
    print(f"[{index+1}/{len(df)}] {row['title'][:50]}...")  
    filename = row['filename']
    url = row['url']
    title = row['title'][:50]  # Truncate for display
    
    # Fetch page
    response = requests.get(url)
    
    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find content
    content_div = soup.find('div', class_='field-docs-content')
    document_text = content_div.get_text(strip=True, separator='\n') 
    
    # Save to file
    filepath = f'data/raw_texts/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(document_text)

    # wait between requests
    time.sleep(2)

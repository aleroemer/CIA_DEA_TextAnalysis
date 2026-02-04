import requests 
from bs4 import BeautifulSoup
import pandas as pd 

# The URL I want to scrape
url = "https://www.presidency.ucsb.edu/advanced-search?field-keywords=Nicaragua&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=200296&category2%5B%5D=406&category2%5B%5D=58&category2%5B%5D=69&category2%5B%5D=8&category2%5B%5D=82&category2%5B%5D=84&category2%5B%5D=59&category2%5B%5D=45&category2%5B%5D=63&items_per_page=25"

 # Fetch the web page
print("Fetching the page...")
response = requests.get(url)
print(f"Status code: {response.status_code}")
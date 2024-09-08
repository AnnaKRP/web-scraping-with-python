from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np

# Functions to extract author, title, and price
def get_author(soup):
    try:
        author = soup.find("div", attrs={"class": "author"}).text.strip()
    except AttributeError:
        author = "Unknown Author"
    return author

def get_title(soup):
    try:
        title = soup.find("span", attrs={"class": "base"}).text.strip()
    except AttributeError:
        title = "Unknown Title"
    return title

def get_price(soup):
    try:
        price = soup.find("span", attrs={"class": "price"}).text.strip()
    except AttributeError:
        price = "Unknown Price"
    return price

# URL to a website
URL = "https://www.books.ie/bestsellers"

# Headers for the HTTP request
HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', 
            'Accept-Language': 'en-US,en;q=0.5'})

# Make the HTTP request
webpage = requests.get(URL, headers=HEADERS)
print("Status - " + str(webpage.status_code))
print("Type of the content - " + str(type(webpage.content)))

# Soup object containing all data
soup = BeautifulSoup(webpage.content, "html.parser")

# Find all the product links
links = soup.find_all("a", attrs={"class": "product-item-link"})
print("Total links on the page - " + str(len(links)) + "\n")

# Store links in the list
links_list = [link.get('href') for link in links]

# Dictionary to store the data
d = {"author": [], "title": [], "price": []}

# Iterate through the links and collect data
for link in links_list:
    new_webpage = requests.get(link, headers=HEADERS)
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    d['author'].append(get_author(new_soup))
    d['title'].append(get_title(new_soup))
    d['price'].append(get_price(new_soup))

# Create DataFrame and clean data
books_df = pd.DataFrame.from_dict(d)
books_df.rename(columns={"author": "AUTHOR", "title": "TITLE", "price": "PRICE"}, inplace=True)

# Clean the DataFrame
books_df['TITLE'].replace('', np.nan, inplace=True)
books_df = books_df.dropna(subset=['TITLE'])

# Save data to CSV
books_df.to_csv('books.csv', header=True, index=False)

print("Data scraping and saving completed.")

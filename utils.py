import uuid
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from bs4 import BeautifulSoup
import requests


# Function to add  data source URLs to the database, avoiding duplicates
def add_url(url, name):
    # Check if the URL already exists
    existing_source = session.query(DataSource).filter_by(url=url).first()
    if existing_source is None:
        new_source = DataSource(url=url, name=name)
        session.add(new_source)
        session.commit()
        print(f"Added URL: {url}")
    else:
        print(f"URL already exists: {url}")

def add_urls_from_excel(file_path, url_column=None, name_column=None):
    # Read Excel file
    df = pd.read_excel(file_path)

    # Verify URL and name columns exist
    if url_column not in df.columns or name_column not in df.columns:
        raise ValueError("Please specify valid column names for URL and name.")

    # Add each URL and name to the database
    for _, row in df[[url_column, name_column]].dropna().iterrows():
        add_url(row[url_column], row[name_column])



# Function to scrape and store data from a given URL and source ID
def scrape_and_store_data(source_id, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a successful response

        # Parse HTML with BeautifulSoup (adjust as needed)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Extract all paragraphs (adjust this logic as per website structure)
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        scraped_data = ' '.join(paragraphs[:10])  # Limit to the first 10 paragraphs for brevity
        
        # Store the scraped data in the WebsiteData table
        website_data = WebsiteData(source_id=source_id, data=scraped_data)
        session.add(website_data)
        session.commit()
        print(f"Data scraped and stored for source ID {source_id}")

    except requests.RequestException as e:
        print(f"Failed to scrape {url}: {e}")

# Function to iterate through all data sources and scrape data where possible
def scrape_all_sources():
    # Query all entries in the DataSource table
    data_sources = session.query(DataSource).all()

    for source in data_sources:
        # Scrape data from each URL in DataSource and store in WebsiteData
        print(f"Scraping data from {source.url}")
        scrape_and_store_data(source.id, source.url)
import uuid
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from bs4 import BeautifulSoup
import requests
import pandas as pd

engine = create_engine('sqlite:///company_data.db')
# Setup session
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define DataSource model
class DataSource(Base):
    __tablename__ = 'datasources'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)

# WebsiteData Table
class WebsiteData(Base):
    __tablename__ = 'website_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String, ForeignKey('datasources.id'), nullable=False)
    data = Column(Text, nullable=True)  # Store scraped data

    # Relationship with DataSource
    source = relationship("DataSource", back_populates="data_entries")

# Link relationship in DataSource for querying related data
DataSource.data_entries = relationship("WebsiteData", back_populates="source")

# Create the table
Base.metadata.create_all(engine)



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
def scrape_all_sources(number=10):
    # Query all entries in the DataSource table
    data_sources = session.query(DataSource).all()

    for source in data_sources:
        # Scrape data from each URL in DataSource and store in WebsiteData
        print(f"Scraping data from {source.url}")
        scrape_and_store_data(source.id, source.url)
# DayRise Data Engineering
This project is designed to automate data extraction, storage, and access for Day rise's  multiple data sources stored in an Excel file. The system is a lightweight ETL (Extract, Transform, Load) pipeline and web scraping utility, built to load data sources from an Excel file, assign unique identifiers, scrape data from specified websites, and store it in a structured SQL database.

## Project Overview
### Goals
**Data Management**: Import and store data source URLs from an Excel file with unique identifiers and names. This is to track all data sources and avoid duplication in the future.

**Data Extraction**: Scrape content from specified websites to collect information where possible. For websites from which scarping is possible, a simple scraping logging on how this can be done ois provided. This is logic demonstration only on how the database will be handled and does not handle the specifinc scraping needs for each website.

**Data Accessibility**: Organize the data in a relational database for easy access, with URLs, source names, and scraped data for analysis or further processing.

## Tech Stack
1. Python: For data processing, database interactions, and web scraping.
2. SQLAlchemy: To manage SQLite database interactions.
3. SQLite: Chosen as a lightweight database solution to simplify development and testing.
4. BeautifulSoup: For parsing HTML data from web pages in a flexible manner.

# Project Structure
## Database Design
The database is organized in two tables:
1. DataSource: Stores the unique ID, URL, and name of each data source (website) extracted from the Excel file.
2. WebsiteData: Stores the scraped data with a reference to the DataSource table via source_id.

The DataSource table acts as a central reference for all data sources, while WebsiteData captures relevant scraped content for each URL, enabling clear and structured access to each website’s data.

## Files and Folders
**001_Data_Exploration.ipynb**: Contains the initial exploration of the data to understand what it contains.

**utils.py**
1. Defines the DataSource and WebsiteData models and their relationships.
2. Contains the main ETL logic, including functions to load URLs from Excel, assign unique IDs, perform scraping, and store data in the database.

**002_Database_engineering.ipynb** : This executes all the logic created in the utils file.

**company_data.db** : SQLite database where all data is stored.

## Installation and Setup
Clone the Repository:

```
git clone https://github.com/PatriciaNekesa/DayRise.git
```
Install Dependencies:
The main dependencies include SQLAlchemy for database management, requests for HTTP requests, and BeautifulSoup for parsing HTML content.

Prepare Excel File: Place your Excel file (e.g., Dayrize_Automation_Database.xlsx) in the project directory.

Run the ETL Process by running the **002_Database_engineering.ipynb**: Execute the main notebook to import data sources, scrape websites, and store the data.

### Code Overview
#### Key Functions
**add_urls_from_excel**: Reads URLs and website names from the Excel file, assigns unique IDs using UUIDs, and stores them in the DataSource table.
**scrape_and_store_data**: Takes a URL and ID, sends an HTTP request to the URL, and parses the HTML content (e.g., paragraphs). The content is then saved in the WebsiteData table.
**scrape_all_sources**: A loop function that iterates over all data sources, scraping each one and adding data to the database if it’s accessible.

### Challenges and Solutions
1. Data Uniqueness: Ensuring each URL has a unique ID. Solution: UUIDs provide robust unique identifiers.
2. Scrapability of Websites : Not all websites allow scraping. Solution: The script skips URLs that are inaccessible or return errors, with error handling and logging for review.

### Future Enhancements
1. Data Extraction Logic : Update scraping logic to handle all data soruces access logic. 
2. Scraping Schedule: Implement a scheduling mechanism to periodically scrape and update data.
3. Data Lake Integration : In larger setups, integrate with a data lake for scalable storage and processing.
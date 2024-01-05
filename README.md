# Website Text Scraper

This repository contains a Scrapy project named `website_bodytext_scraper` designed to scrape the body text from a list of websites. The list of websites is provided via a CSV file, and the scraped data is saved in a specified output format.

## Directory Structure

```
website_bodytext_scraper/
│
├── data/                       # Directory containing input and output data
│   ├── inputs.csv              # Primary input file with list of URLs to scrape
│   └── output.csv              # Example output file with scraped data
│
├── spiders/                    # Directory containing Scrapy spiders
│   ├── bodytext_spider.py      # Spider to scrape body text from websites
│   └── check_urls_spider.py    # Spider to check the status of URLs
│
├── items.py                    # Scrapy items definition
├── middlewares.py              # Scrapy middlewares
├── pipelines.py                # Scrapy item pipelines
├── settings.py                 # Scrapy project settings
└── scrapy.cfg                  # Scrapy configuration file
```

## Setup

1. **Clone the Repository**:
   ```
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Testing URLs before scraping
   - Update the `data/inputs.csv` file with the list of URLs you want to scrape. Each URL should be on a new line.
   - From the root directory, run the following command:
     ```
     scrapy crawl bodytext
     ```
   - The scraped data will be saved to the specified output location (e.g., `data/output.csv`).

### Running the bodytext scraper
   - Ensure you have a CSV file with URLs under the 'WbstAddrssTxt' column.
   - From the root directory, run the following command:
     ```
     scrapy runspider website_bodytext_scraper/spiders/check_urls_spider.py -o results.csv
     ```
   - The results will be saved to `results.csv` with details about each URL's status and duplicates.
   - Check the output file (e.g., `data/output.csv` or `results.csv`) to see the scraped body text or URL check results from each URL.


### In development: Page traversal
- A script is in development to traverse through all pages found in the website's navbar to save the content from them too

### Cleanup utilities
 **Delete All `__pycache__` Folders**:
   - To remove all `__pycache__` directories from the repository, run the `delete_pycache.sh` script:
     ```
     ./delete_pycache.sh
     ```

## Customization

- To modify the output format or location, adjust the `FEEDS` setting in `settings.py`.
- To add more spiders or modify the existing spider, navigate to the `spiders/` directory.

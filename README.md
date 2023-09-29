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
│   └── bodytext_spider.py      # Spider to scrape body text from websites
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

1. **Input**:
   - Update the `data/inputs.csv` file with the list of URLs you want to scrape. Each URL should be on a new line.

2. **Run the Spider**:
   - From the root directory, run the following command:
     ```
     scrapy crawl bodytext
     ```
   - The scraped data will be saved to the specified output location (e.g., `data/output.csv`).

3. **Review the Results**:
   - Check the output file (e.g., `data/output.csv`) to see the scraped body text from each URL.

## Customization

- To modify the output format or location, adjust the `FEEDS` setting in `settings.py`.
- To add more spiders or modify the existing spider, navigate to the `spiders/` directory.

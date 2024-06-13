# Website Text Scraper

This repository contains a Scrapy project named `website_bodytext_scraper` designed to scrape the body text from a list of websites. It works by accepting a list of websites is provided through a CSV file, scraping the body text of each site's home page and associated sub-pages, and saves the data in a specified output format. It's designed to provide the user with the raw body text of a website's homepage and associated subpages, which can be used as inputs for AI applications, among other uses.


## Directory Structure

```
.
├── README.md
├── inputs.csv
├── requirements.txt
├── scrapy.cfg
├── test.json
└── website_bodytext_scraper
    ├── data
    │   └── url_check_output
    ├── example
    │   └── example_inputs.csv
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── __init__.py
        ├── bodytext_crawl_spider.py
        ├── check_urls_spider.py
        └── utils.py

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

Two steps must be performed for best results. First, the list of URLs provided is checked to ensure a successful scrape can be performed on the website by checking for a 200 HTTP status code, and rendering a report on the responses for all URLs tried. This step renders a new list of websites with a high chance of success. In the second step, this new list is used to perform the scrape and process the data into a final CSV. 

### 1. Testing URLs before scraping

   - Update the `inputs.csv` file at the root level with the list of URLs you want to scrape. Each URL should be on a new line, and the header must not be changed from "url".
   - From the root directory, run the following command:
     ```
     scrapy crawl check_urls
     ```
   - The spider outputs two files:
      - website_bodytext_scraper/data/url_check_output/results.csv: This contains a full report of all URLs tried and their results 
      - website_bodytext_scraper/data/url_check_output/bodytext_inputs.csv: A clean list of all the successful connections formatted to be ingersted by the bodytext scraper. This file will be automatically used by the scarper, no action is required to configure it.
      

### 2. Running the bodytext scraper
   - Ensure you have run the preceding step and a `data/url_check_output/bodytext_inputs.csv` has appeared and contains data
   - From the root directory, run the following command:
     ```
     scrapy crawl bodytext_crawl
     ```
   - The results will be saved to `bodytext_results.csv` with the page's body text as a text blob in the 'body_text' field

## Example

To test out the scraper before using it for your project, a sample CSV of URLs is included. It's deliberately messy to mimic an imperfect data extraction process, to demonstrate the scraper's ability to check and clean all domains before scraping the websites themselves.

To try it out:
- Copy the contexts of `website_bodytext_scraper/example/example_inputs.csv` into `website_bodytext_scraper/inputs.csv`. 
- Run `scrapy crawl check_urls`
- In `website_bodytext_scraper/data/url_check_output`, two new CSVs should appear:
   - 'results.csv' contains a full report of the status of all URLs in the input file
   - 'bodytext_inputs.csv' is a clean list of all successfully pinged URLs, normalized to a standard structure. 
- Now run `scrapy crawl bodytext`
- A bodytext_results.csv file will appear at the root level with the results of the scrape


## Development

### Customization

- To modify the output format or location, adjust the `FEEDS` setting in `settings.py`.
- To add more or modify existing spiders, navigate to the `spiders/` directory.

### Future Development

We would love to hear your thoughts on how to improve this repo! Contact ___@givingtuesday.org with your ideas.

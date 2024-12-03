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

### UPDATE: run_spider.py

The scraper is currently being updated to use run_spider.py as an entrypoint to make using it on different environments easier. An environment must be used in the command, such as:

`SCRAPY_PROJECT=local python run_spider.py`

The Stripe spider is currently deployed to an EC2 instance and is configured to run every 6 hours. The settings are configured in two places:
* A custom EC2 settings file where a timeout param is set to 5 hours 55 minutes
* A cron job on the EC2 instance where the spider is restarted every 6 hours

**Custom EC2 settings**: /website_bodytext_scraper/website_bodytext_scraper/settings/ec2.py
* Inherits all default settings from "base" settings file
* Inputs and ouputs are set here 
	* Inputs come from the form990_data folder on the instance
	* Output goes to and S3 directory
		* Note: it is recommended to start a new directory for each dedicated run so all CSVs generated for that run are stored together
* Log settings are set to "DEBUG" for full visibility and exported to a given path
* The spider timeout is configured by enabling the extenstion (by setting to 500) and setting the `CLOSESPIDER_TIMEOUT` param to the number of seconds before timing out
	* This triggers a graceful shutdown of the spider os the output can be periodically exported 
* Note that it is not required to configure AWS credentials here as they are inherently passed to the EC2 instance and periodically update
* Note that for testing, there is a different settings file called test.py that is configured for small test runs 

**Cron job**: crontab -e
* The cron job currently configured on the machine is:
`0 */2 * * * cd /home/ubuntu/website_bodytext_scraper && SCRAPY_PROJECT=ec2 venv/bin/python run_spider.py >> /home/ubuntu/cron.log 2>&1 `
* This triggers the Stripe spider every 2 hours using the ec2 settings, and outputs to cron.log

**Logs**
There are two kinds of logs to monitor when the EC2 instance is running:
* `/website_bodytext_scraper/exports/logs/logs.txt` : All output from the spider at the DEBUG level
* `cron.log`: For any output from triggering run_spider, which when successfully run produces a timestamp of the last run triggered, otherwise shows the error

**Importance of http_cache**
* It is very important to keep the http-cache subdirectory under the hidden .scrapy folder in the website_bodytext_scraper directory, as this contains copies of all the web pages scraped so the scraper can easily be re-run if changes are made 
* The storage of the EC2 instance is optimized to hold this, but storage on the machine should be periodically monitored to ensure it doesn't run out of space

----------------------------------------------------

###  DEPRECATED: Proceed with caution

_The following instructions may be out of date, the latest documentation is for the EC2 instance config above_


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

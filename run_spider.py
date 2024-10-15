from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from website_bodytext_scraper.spiders.detect_stripe import DetectStripeSpider
import asyncio
import nest_asyncio
import sys
import logging
import os

# location = 'databricks'
location = 'local'

local_params = {
   'input_path': 'website_bodytext_scraper/data/oct_11_run/bodytext_inputs_test.csv',
   'output_path': 'website_bodytext_scraper/dev_exports/TEST'
}

db_params = {
   'input_path': '/Volumes/sandbox_britt/web_scraper/exports/bodytext_inputs_test.csv',
   'output_path': '/Volumes/sandbox_britt/web_scraper/exports/Oct_15/'
}

# TODO: Specify import & export locations
def run_crawler(input_path, output_directory):
  # Define output directory as passed from arg or default
  if output_directory:
      output_path = os.path.join(output_directory, 'stripe_%(time)s.csv')
  else:
       output_path= 'website_bodytext_scraper/dev_exports/stripe_%(time)s.csv'
  
  # Add FEEDS to project settings
  settings = get_project_settings()
  settings.set('FEEDS', {
        output_path: {
            'format': 'csv',
            'overwrite': True,
        }
    })
  
  # Set up and run rpocess
  process = CrawlerProcess(settings)
  process.crawl(DetectStripeSpider, 
      input_path=input_path
  )
  process.start()

if __name__ == "__main__":
    if location == 'databricks':
        # DB-specific settings
        logger = spark._jvm.org.apache.log4j
        logging.getLogger("py4j").setLevel(logging.ERROR)
        nest_asyncio.apply()
        
        # Run spider
        asyncio.run(run_crawler(
           input_path=db_params['input_path'],
           output_directory=db_params['output_path']
        ))
    elif location == 'local':
       run_crawler(
           input_path=local_params['input_path'],
           output_directory=local_params['output_path']
        )
    else:
       print('No location found, please specify Databricks or local')
       sys.exit(1)
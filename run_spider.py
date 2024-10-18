from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from website_bodytext_scraper.spiders.detect_stripe import DetectStripeSpider
import asyncio
import nest_asyncio
import sys
import logging
import os


# TODO: Specify import & export locations
def run_crawler():
  settings = get_project_settings() 

  # Define output directory as passed from arg or default
  output_directory = settings.get('OUTPUT_PATH')
  output_path = os.path.join(output_directory, 'stripe_%(batch_time)s.csv')

  # Add FEEDS to project settings
  settings.set('FEEDS', {
        output_path: {
            'format': 'csv',
            'overwrite': True,
        }
    })
  
  # Set up and run rpocess
  process = CrawlerProcess(settings)
  process.crawl(DetectStripeSpider, 
      input_path=settings.get('INPUT_PATH')
  )
  process.start()

if __name__ == "__main__":
    # if location == 'databricks':
    #     # DB-specific settings
    #     logger = spark._jvm.org.apache.log4j
    #     logging.getLogger("py4j").setLevel(logging.ERROR)
    #     nest_asyncio.apply()
        
    #     # Run spider
    #     asyncio.run(run_crawler(
    #        input_path=db_params['input_path'],
    #        output_directory=db_params['output_path']
    #     ))
      run_crawler()
    # else:
    #    print('No location found, please specify Databricks or local')
    #    sys.exit(1)
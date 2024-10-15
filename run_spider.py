from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from website_bodytext_scraper.spiders.detect_stripe import DetectStripeSpider
import asyncio
import nest_asyncio
import sys
import logging

# location = 'databricks'
location = 'local'

# TODO: Specify import & export locations
def run_crawler():
  process = CrawlerProcess(get_project_settings())
  process.crawl(DetectStripeSpider)
  process.start()

if __name__ == "__main__":
    if location == 'databricks':
        logger = spark._jvm.org.apache.log4j
        logging.getLogger("py4j").setLevel(logging.ERROR)
        nest_asyncio.apply()
        asyncio.run(run_crawler())
    elif location == 'local':
       run_crawler()
    else:
       print('No location found, please specify Databricks or local')
       sys.exit(1)
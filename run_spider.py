from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from website_bodytext_scraper.spiders.detect_stripe import DetectStripeSpider
import os
import time

# TODO: Specify import & export locations
def run_crawler():
  settings = get_project_settings() 

  # Output timestamp
  timestamp = time.strftime('%l:%M%p %Z on %b %d, %Y')
  print(f'Job triggered at: {timestamp}')

  # Define output directory as passed from arg or default
  output_directory = settings.get('OUTPUT_PATH')
  output_path = os.path.join(output_directory, 'stripe_%(time)s.csv')

  # Add FEEDS to project settings
  settings.set('FEEDS', {
        output_path: {
            'format': 'csv',
            # NOTE: S3 supports overwrites only, cannot append
            'overwrite': True,
            # 'overwrite': False,
        }
    })
  
  # Set up and run process
  process = CrawlerProcess(settings)
  process.crawl(DetectStripeSpider, 
      input_path=settings.get('INPUT_PATH')
  )
  process.start()

if __name__ == "__main__":
  run_crawler()

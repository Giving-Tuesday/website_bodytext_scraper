import os
from .base import *

# Custom settings
SCRAPER_ENV='test'

# Inputs & outputs
INPUT_PATH = 'website_bodytext_scraper/data/ec2/oct_28_test_set.csv'
# pwd for output_path is website_bodytext_scraper/, specify next level from there
# OUTPUT_PATH = 'exports/test_oct_28'
# Testing S3
OUTPUT_PATH = 's3://non-profit-web-scraping-dev/tests/oct_28/'


# Log level
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'exports/logs/test_logs_oct28.txt'

# AWS CREDENTIALS: NOTE: Not required if running on EC2!
#AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
#AWS_SECRET_ACCESS_KEY =  os.environ['AWS_SECRET_ACCESS_KEY']
#AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']

# Configuring closeSpider
EXTENSIONS = {
   'scrapy.extensions.closespider.CloseSpider': 500,
}
CLOSESPIDER_TIMEOUT = 1 # Starting with 1 second

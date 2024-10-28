import os
from .base import *

# Custom settings
SCRAPER_ENV='ec2'

# Inputs & outputs
INPUT_PATH = '/home/ubuntu/form990_data/full_list/bodytext_inputs.csv'
OUTPUT_PATH = 's3://non-profit-web-scraping-dev/tests/oct_28/'

# Log level
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'exports/logs/logs.txt'

# AWS CREDENTIALS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY =  os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']

# Configuring closeSpider
EXTENSIONS = {
   'scrapy.extensions.closespider.CloseSpider': 500,
}
CLOSESPIDER_TIMEOUT = 1 # Starting with 1 second

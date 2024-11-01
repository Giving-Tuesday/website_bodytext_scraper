import os
from .base import *

# Custom settings
SCRAPER_ENV='ec2'

# Inputs & outputs
INPUT_PATH = '/home/ubuntu/form990_data/full_list/bodytext_inputs.csv'
OUTPUT_PATH = 's3://non-profit-web-scraping-dev/runs/oct_31_2024/'

# Log level
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'exports/logs/logs.txt'

# Configuring closeSpider
EXTENSIONS = {
   'scrapy.extensions.closespider.CloseSpider': 500,
}
CLOSESPIDER_TIMEOUT = 21300 # 5 hours 55 mins (5 mins before cron reset)

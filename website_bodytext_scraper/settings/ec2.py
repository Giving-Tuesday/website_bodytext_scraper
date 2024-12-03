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
# Enabling persistent jobs queue for scheduler
JOBDIR = 'crawls/run_spider-ec2'

# Configuring memory usage extension and memory debugger extensions
MEMDEBUG_ENABLED = True
MEMDEBUG_NOTIFY = ['sana@givingtuesday.org']

MEMUSAGE_ENABLED = True
MEMUSAGE_NOTIFY_MAIL = ['sana@givingtuesday.org']
MEMUSAGE_WARNING_MB = 4000
MEMUSAGE_LIMIT_MB = 5000

# Configuring closeSpider
EXTENSIONS = {
   'scrapy.extensions.closespider.CloseSpider': 500,
}
CLOSESPIDER_TIMEOUT = 110 * 60 # 1 hour 50 mins (10 mins before cron reset)

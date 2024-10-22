import os
from .base import *

# Custom settings
SCRAPER_ENV='test'

# Inputs & outputs
INPUT_PATH = 'website_bodytext_scraper/data/oct_11_run/bodytext_inputs_test.csv'
OUTPUT_PATH = 's3://non-profit-web-scraping-dev/tests/oct_22_run/%(batch_time)s'

# Batching outputs
# NOTE: filename MUST contain `%(batch_time)s` or `%(batch_id)d` to export correctly
FEED_EXPORT_BATCH_ITEM_COUNT = 100

# Log level
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'exports/logs/test_logs.txt'

# AWS CREDENTIALS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY =  os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']

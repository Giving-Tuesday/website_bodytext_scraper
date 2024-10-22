import os
from .base import *

# Custom settings
SCRAPER_ENV='test'

# Inputs & outputs
INPUT_PATH = 'website_bodytext_scraper/data/oct_11_run/bodytext_inputs_test.csv'
OUTPUT_PATH = 's3://non-profit-web-scraping-dev/tests/TEST.csv'

# Log level
LOG_LEVEL = 'DEBUG'
# LOG_FORMAT = '%(levelname)s: %(message)s'
# LOG_FILE = 'exports/logs/test_logs.txt'

# AWS CREDENTIALS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY =  os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']

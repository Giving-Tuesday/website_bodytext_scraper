import os
from .base import *

# Custom settings
SCRAPER_ENV='local'
INPUT_PATH = '/home/ubuntu/website_bodytext_scraper/website_bodytext_scraper/data/oct_21_run/bodytext_inputs.csv'
OUTPUT_PATH = 'exports'

# TODO: Configure S3 settings
# TODO: Potentially migrate here: # IS_OUTPUT_EMPTY = not os.path.exists(
#     OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0


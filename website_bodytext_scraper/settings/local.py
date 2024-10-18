import os
from .base import *

# Custom settings
SCRAPER_ENV='local'
INPUT_PATH = 'website_bodytext_scraper/data/oct_11_run/bodytext_inputs_test.csv'
OUTPUT_PATH = 'website_bodytext_scraper/dev_exports/TEST'

# TODO: Configure S3 settings
# TODO: Potentially migrate here: # IS_OUTPUT_EMPTY = not os.path.exists(
#     OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0


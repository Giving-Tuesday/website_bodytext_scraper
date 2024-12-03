import os
from .base import *

# Custom settings
SCRAPER_ENV='local'

# Inputs & outputs
INPUT_PATH = 'website_bodytext_scraper/data/oct_11_run/bodytext_inputs_test.csv'
OUTPUT_PATH = 'exports'

# Log level
LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(levelname)s: %(message)s'
LOG_FILE = 'exports/logs/logs.txt'

# TODO: Configure S3 settings
# TODO: Potentially migrate here: # IS_OUTPUT_EMPTY = not os.path.exists(
#     OUTPUT_FILE) or os.path.getsize(OUTPUT_FILE) == 0


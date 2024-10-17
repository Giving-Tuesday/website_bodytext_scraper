# utils.py
import csv
import re
import validators


def load_urls_from_csv(file_path: str, column_index: int) -> list:
    """
    Load URLs from a CSV file.

    Reads URLs from the specified column of the CSV file, skipping the header row.
    """
    urls = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            urls.append(row[column_index])

    return urls


def extract_domain(url: str) -> str:
    """
    Extract domain from a URL.

    Converts URL to lowercase, adds 'http://' if missing, and extracts the domain.
    """
    if '://' not in url:
        url = 'http://' + url
    match = re.search(r'(?<=://)(www\d?\.)?(.*?)(?=/|$)', url.lower())
    if match:
        domain = match.group(2)
        return domain
    return None


def clean_url(urls: list) -> tuple:
    """
    Clean URLs and separate valid domains from invalid ones.

    Validates and extracts domains from a list of URLs, classifying them as valid or invalid.
    """
    cleaned_domains = []
    invalid_records = []

    for url in urls:
        if isinstance(url, str):
            domain = extract_domain(url)
            if domain and validators.domain(url):
                cleaned_domains.append(domain)
            else:
                invalid_records.append(url)
        else:
            invalid_records.append(url)

    return cleaned_domains, invalid_records


def add_http(url: str) -> str:
    """
    Ensure URL starts with 'http://'.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url.lower()
    return url


from datetime import datetime
import os 
from zoneinfo import ZoneInfo

scraper_run_dir = '/Volumes/sandbox_britt/web_scraper/exports'

def create_file():
    timestamp = datetime.now(tz=ZoneInfo('Canada/Eastern')).strftime("%Y%m%d_%H%M%S")
    # timestamp = 'Sep 19'
    run_dir = os.path.join(scraper_run_dir, f'scraper_run_{timestamp}')
    os.makedirs(run_dir, exist_ok=True)
    file_path = os.path.join(run_dir, 'test.txt')

    with open(file_path, 'w') as f:
        f.write('testing')

def generate_directory(export_dir, filename):
    timestamp = datetime.now(tz=ZoneInfo('Canada/Eastern')).strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(export_dir, f'scraper_run_{timestamp}')
    os.makedirs(run_dir, exist_ok=True)
    dir = os.path.join(run_dir, filename)
    print(f"⚠️ {dir}")

    return dir
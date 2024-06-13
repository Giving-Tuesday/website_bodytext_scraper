# utils.py
import csv
from urllib.parse import urlparse, urlunparse
import validators
import re

def load_urls_from_csv(file_path, column_index):
    urls = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            urls.append(row[column_index])
    
    return urls

def extract_domain(url):
    if '://' not in url:
        url = 'http://' + url
    match = re.search(r'(?<=://)(www\d?\.)?(.*?)(?=/|$)', url.lower())
    if match:
        domain = match.group(2)
        return domain
    return None

def clean_url(urls):
     # Lists to store cleaned domains and invalid records
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


def add_http(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url.lower()
    return url



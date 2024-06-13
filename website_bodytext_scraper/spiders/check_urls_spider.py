import scrapy
import csv
import os
import pandas as pd
from urllib.parse import urlparse
from collections import Counter
from .utils import load_urls_from_csv, clean_url, add_http
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from scrapy.exceptions import IgnoreRequest

class CheckURLsSpider(scrapy.Spider):
    name = 'check_urls'
    handle_httpstatus_all = True
    output_dir = 'website_bodytext_scraper/data/url_check_output' 

    def __init__(self, input_file=None, *args, **kwargs):
        super(CheckURLsSpider, self).__init__(*args, **kwargs)
        # Set up start_urls
        self.file_path = 'inputs.csv'
        self.column_index = 0 # Selects the first column of the CSV

        # Set up counters
        self.urls_checked = 0
        # self.duplicate_domains = []
        self.urls_checked = 0
        self.live_sites = 0

        # # Set up analysis results CSV params
        self.results_csv_path = os.path.join(self.output_dir, 'results.csv')
        self.results_csv_file = open(self.results_csv_path, 'w', newline='')
        self.results_csv_writer = csv.writer(self.results_csv_file)
        self.results_csv_writer.writerow(['url', 'http_status','reason'])
        
         # Set up bodytext input CSV params
        self.bodytext_csv_path = os.path.join(self.output_dir, 'bodytext_inputs.csv')
        self.bodytext_csv_file = open(self.bodytext_csv_path, 'w', newline='')
        self.bodytext_csv_writer = csv.writer(self.bodytext_csv_file)
        self.bodytext_csv_writer.writerow(['url'])


    def process_urls(self, input_csv):
        urls = load_urls_from_csv(input_csv, column_index=0)
        cleaned_domains, _ = clean_url(urls)

        return cleaned_domains

    def start_requests(self):
        allowed_domains = self.process_urls(self.file_path)
        urls = [add_http(domain) if isinstance(domain, str) else domain for domain in allowed_domains]

        for url in urls:
            self.urls_checked += 1
            yield scrapy.Request(url, method='HEAD', callback=self.parse_head, errback=self.parse_error)

        
    def parse_head(self, response):
        is_live = response.status == 200,

        if is_live:
            self.live_sites +=1
            self.bodytext_csv_writer.writerow([response.url])

        self.results_csv_writer.writerow([
            response.url, 
            response.status, 
            'Successful connection'
        ])

    def parse_error(self, failure):
        # log all failures
        # self.logger.error(repr(failure))

        url = failure.request.url
        if failure.check(HttpError):
            response = failure.value.response
            http_status = response.status
            reason = 'HTTP error'
            self.logger.error(f'HTTP error on {response.url}: {response.status}')
        elif failure.check(DNSLookupError):
            http_status = 'N/A'
            reason = 'DNS lookup error'
            self.logger.error(f'DNS lookup error on {failure.request.url}')
        elif failure.check(TimeoutError, TCPTimedOutError):
            http_status = 'N/A'
            reason = 'Timeout error'
            self.logger.error(f'Timeout error on {failure.request.url}')
        elif failure.check(IgnoreRequest):
            http_status = 'N/A'
            reason = 'Forbidden by robots.txt'
            self.logger.info(f'Request ignored on {url} due to robots.txt')
        else:
            http_status = 'N/A'
            reason = repr(failure)
            self.logger.error(f'Non-HTTP error on {failure.request.url}: {repr(failure)}')

        self.results_csv_writer.writerow([url, http_status, reason])


    def closed(self, reason):
        self.results_csv_file.close()
        self.bodytext_csv_file.close()
        self.log_summary_stats()

    def log_summary_stats(self):
        live_site_rate = (self.live_sites / self.urls_checked) * 100 if self.urls_checked > 0 else 0

        self.logger.info(f'Websites scraped: {self.urls_checked}')
        self.logger.info(f'Live site rate: {live_site_rate:.2f}%')
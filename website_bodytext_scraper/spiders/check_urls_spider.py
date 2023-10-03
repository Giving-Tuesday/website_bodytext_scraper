import scrapy
import pandas as pd
from urllib.parse import urlparse, urlunparse
from collections import Counter

class CheckURLsSpider(scrapy.Spider):
    name = 'check_urls'

    handle_httpstatus_list = [404, 500, 403, 400, 408, 429, 502, 503, 504, 522, 524]  # Add any other status you want to handle
    
    @staticmethod
    def extract_domain(url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    @staticmethod
    def find_duplicate_domains(urls):
        domains = [CheckURLsSpider.extract_domain(url) for url in urls]
        domain_counts = Counter(domains)
        duplicate_domains = [domain for domain, count in domain_counts.items() if count > 1]
        return duplicate_domains

    @staticmethod
    def clean_url(url, default_scheme='http', add_www=True):
        if 'https//' in url:
            url = url.replace('https//', 'https://')
        elif 'http//' in url:
            url = url.replace('http//', 'http://')
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme if parsed_url.scheme else default_scheme
        netloc = parsed_url.netloc or parsed_url.path
        path = ''
        if not parsed_url.netloc and add_www and '.' in netloc and not netloc.startswith('www.'):
            netloc = 'www.' + netloc
        netloc = netloc.lower()
        cleaned_url = urlunparse((scheme, netloc, path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        return cleaned_url
    
    def start_requests(self):
        input_file = '/Users/brittany/repos/gt-scraper/website_bodytext_scraper/website_bodytext_scraper/data/test_urls.csv'
        df = pd.read_csv(input_file)
        sample_urls = df['WbstAddrssTxt'].tolist()
        cleaned_urls = [self.clean_url(url) for url in sample_urls]
        self.duplicate_domains = self.find_duplicate_domains(cleaned_urls)
        for url in cleaned_urls:  
            yield scrapy.Request(url, method='HEAD', callback=self.parse_head, errback=self.parse_error)
        
    def parse_head(self, response):
        yield {
            'url': response.url,
            'is_live': response.status == 200,
            'is_duplicate': response.url in self.duplicate_domains,
            'http_status': response.status
        }

    def parse_error(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        
        # Getting the URL from the failure request
        url_failed = failure.request.url
        
        yield {
            'url': url_failed,
            'is_live': False,
            'is_duplicate': url_failed in self.duplicate_domains,
            'http_status': 'Error/Failed'
        }
import scrapy
import csv 
import pandas as pd
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from .utils import load_urls_from_csv, extract_domain
from urllib.parse import urlparse


class BodyTextCrawlSpider(CrawlSpider):
    name = 'bodytext_crawl'
    start_urls = []  

    rules = (
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(BodyTextCrawlSpider, self).__init__(*args, **kwargs)
        self.file_path = 'website_bodytext_scraper/data/url_check_output/bodytext_inputs.csv'
        self.column_index = 0

    def start_requests(self):
        urls = load_urls_from_csv(self.file_path, self.column_index)
        allowed_domains = [extract_domain(url) for url in urls]
  
        # Log the URLs being used
        logging.info(f"Using debug URLs: {urls}")

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_start_page, errback=self.parse_error) 

    def parse_start_page(self, response):
        links = LinkExtractor().extract_links(response)
        # allowed_domains = ['www.vrpa.org']
        allowed_domains = urlparse(response.url).netloc
        allowed_links = [link for link in links if urlparse(link.url).netloc in allowed_domains]

        logging.info(f"Found {len(allowed_links)} allowed links out of {len(links)} total links")

        for link in allowed_links:
            self.logger.info(f"Link: {link.url}")
            yield scrapy.Request(
                link.url, 
                callback=self.parse_page)
        
        # yield from self.parse_page(response)

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Remove script and style tags
        for script in soup(["script", "style"]):  
            script.extract()
        body_text = ' '.join(soup.stripped_strings)
        
        # Extra check to catch missed new lines
        if '\n' in body_text:
            body_text = body_text.replace('\n', ' ')

        domain = response.url.split("/")[2]

        yield {
            'url': domain,
            'page_traversed': str(response.url),
            'body_text': body_text
        }

    def parse_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(repr(failure))
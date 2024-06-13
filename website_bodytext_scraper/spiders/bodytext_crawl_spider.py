from urllib.parse import urlparse
import logging

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from bs4 import BeautifulSoup

from .utils import load_urls_from_csv, extract_domain


class BodyTextCrawlSpider(CrawlSpider):
    name = 'bodytext_crawl'
    start_urls = []

    rules = (
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = 'website_bodytext_scraper/data/url_check_output/bodytext_inputs.csv'
        self.column_index = 0

    def start_requests(self):
        """
        Generate initial requests for the spider.

        Loads URLs from a CSV file, extracts allowed domains, logs the URLs,
        and initiates requests for each URL.
        """
        urls = load_urls_from_csv(self.file_path, self.column_index)
        allowed_domains = [extract_domain(url) for url in urls]

        # Log the URLs being used
        logging.info("Using debug URLs: %d", urls)

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_start_page, errback=self.parse_error)

    def parse_start_page(self, response):
        """
        Extract and filter links from the start page.

        Extracts all links using LinkExtractor, filters them based on allowed domains,
        logs the number of allowed links, and initiates requests for each allowed link.

        """
        links = LinkExtractor().extract_links(response)
        # allowed_domains = ['www.vrpa.org']
        allowed_domains = urlparse(response.url).netloc
        allowed_links = [
            link for link in links if urlparse(
                link.url).netloc in allowed_domains]

        logging.info(
            "Found %d allowed links out of %d total links",
            len(allowed_links),
            len(links))

        for link in allowed_links:
            self.logger.info(f"Link: {link.url}")
            yield scrapy.Request(
                link.url,
                callback=self.parse_page)

    def parse_page(self, response):
        """
        Removes script and style tags, processes body text, and extracts the domain.
        """
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

    def parse_error(self,failure):
        """
        Log request failure details.
        """
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(repr(failure))

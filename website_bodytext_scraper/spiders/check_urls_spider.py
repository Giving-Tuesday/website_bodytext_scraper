import csv
import os

import scrapy
from scrapy.exceptions import IgnoreRequest
from scrapy.spidermiddlewares.httperror import HttpError

from twisted.internet.error import DNSLookupError, TCPTimedOutError

from .utils import load_urls_from_csv, clean_url, add_http


class CheckURLsSpider(scrapy.Spider):
    name = 'check_urls'
    handle_httpstatus_all = True
    output_dir = 'website_bodytext_scraper/data/url_check_output'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = 'inputs.csv'
        self.urls_checked = 0
        self.urls_checked = 0
        self.live_sites = 0

        self.results_csv_path = os.path.join(self.output_dir, 'results.csv')
        self.results_csv_file = open(  # pylint: disable=consider-using-with,unspecified-encoding
            self.results_csv_path,
            'w',
            newline='')

        self.bodytext_csv_path = os.path.join(
            self.output_dir, 'bodytext_inputs.csv')
        self.bodytext_csv_file = open(  # pylint: disable=consider-using-with,unspecified-encoding
            self.bodytext_csv_path,
            'w',
            newline='')

    def process_urls(self, input_csv: str) -> list:
        """
        Loads URLs from the specified CSV, cleans them, and returns a list of cleaned domains.

        Args:
            input_csv (str): The path to the CSV file containing URLs.

        Returns:
            list: A list of cleaned domains.
        """
        urls = load_urls_from_csv(input_csv, column_index=0)
        cleaned_domains, _ = clean_url(urls)

        return cleaned_domains

    def start_requests(self) -> scrapy.http.Request:
        """
        Processes URLs from the file path, formats them, and generates HEAD requests.

        Returns:
            Generator[scrapy.http.Request]: A generator of Scrapy requests.
        """
        allowed_domains = self.process_urls(self.file_path)
        urls = [add_http(domain) if isinstance(domain, str)
                else domain for domain in allowed_domains]

        for url in urls:
            self.urls_checked += 1
            yield scrapy.Request(
                url,
                method='HEAD',
                callback=self.parse_head,
                errback=self.parse_error)

    def parse_head(self, response: scrapy.http.Response) -> None:
        """
        Logs the URL and status of live sites, and writes successful connections to CSV.

        Args:
            response (scrapy.http.Response): The response object from the HEAD request.

        Returns:
            None
        """
        is_live: bool = response.status == 200

        if is_live:
            self.live_sites += 1
            with open(self.bodytext_csv_path, 'a', newline='', encoding='utf-8') as bodytext_csv_file:
                bodytext_csv_writer = csv.writer(bodytext_csv_file)
                bodytext_csv_writer.writerow([response.url])

        with open(self.results_csv_path, 'a', newline='', encoding='utf-8') as results_csv_file:
            results_csv_writer = csv.writer(results_csv_file)
            results_csv_writer.writerow(
                [response.url, response.status, 'Successful connection'])

    def parse_error(
            self,
            failure: scrapy.spidermiddlewares.httperror.HttpError) -> None:
        """
        Handle and log various types of request failures.

        Args:
            failure (scrapy.spidermiddlewares.httperror.HttpError): The failure object containing details of the error.

        Returns:
            None
        """
        url: str = failure.request.url

        if failure.check(HttpError):
            response = failure.value.response
            http_status = response.status
            reason = 'HTTP error'
            self.logger.error(
                f'HTTP error on {response.url}: {response.status}')
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
            self.logger.error(
                f'Non-HTTP error on {failure.request.url}: {repr(failure)}')

        # self.results_csv_writer.writerow([url, http_status, reason])
        with open(self.results_csv_path, 'a', newline='', encoding='utf-8') as results_csv_file:
            results_csv_writer = csv.writer(results_csv_file)
            results_csv_writer.writerow([url, http_status, reason])

    def closed(self) -> None:
        """
        Closes the result and bodytext CSV files, and logs summary statistics.

        Args:
            reason (str): The reason the spider was closed.

        Returns:
            None
        """
        self.results_csv_file.close()
        self.bodytext_csv_file.close()
        self.log_summary_stats()

    def log_summary_stats(self) -> None:
        """
        Calculates and logs the percentage of live sites checked.

        Returns:
            None
        """
        live_site_rate: float = (
            self.live_sites / self.urls_checked) * 100 if self.urls_checked > 0 else 0

        self.logger.info(f'Websites scraped: {self.urls_checked}')
        self.logger.info(f'Live site rate: {live_site_rate:.2f}%')

    def parse(self, response: scrapy.http.Response) -> None:
        """
        Default parser for the spider.
        """

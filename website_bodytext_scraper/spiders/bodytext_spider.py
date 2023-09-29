import scrapy
from bs4 import BeautifulSoup
import csv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
inputs_csv_path = os.path.join(current_dir, '..', 'data', 'inputs.csv')


class BodyTextSpider(scrapy.Spider):
    name = 'bodytext'
    
    with open(inputs_csv_path, 'r') as file:
        reader = csv.DictReader(file)
        start_urls = [row['url'] for row in reader]

    def parse(self, response):
        """
        Parse the response using BeautifulSoup, extract and clean up the body text by 
        removing script and style tags, and then yield the scraped data.
        
        Args:
        - response: The response object from Scrapy.
        
        Yields:
        - A dictionary containing the URL and the cleaned body text.
        """
        soup = BeautifulSoup(response.text, 'lxml')
        
        for script in soup(["script", "style"]):  # Remove script and style tags
            script.extract()
        body_text = ' '.join(soup.stripped_strings)  # Get all the text, cleaned of extra spaces and newlines
        
        yield {
            'url': response.url,
            'body_text': body_text
        }

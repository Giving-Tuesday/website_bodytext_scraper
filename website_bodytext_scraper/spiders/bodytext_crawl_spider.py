import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup

class BodyTextCrawlSpider(CrawlSpider):
    name = 'bodytext_crawl'
    allowed_domains = ['https://www.greenpeace.org/canada/en']  
    start_urls = ['https://www.greenpeace.org/canada/en']  

    # Define rules for link extraction and callbacks
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """Extract and clean up the body text from the website."""
        soup = BeautifulSoup(response.text, 'lxml')
        
        for script in soup(["script", "style"]):  # Remove script and style tags
            script.extract()
        body_text = ' '.join(soup.stripped_strings)  # Get all the text, cleaned of extra spaces and newlines
        
        # Ensure no newlines in the body_text
        assert "\n" not in body_text, "Newlines detected in the body text!"

        # Return the scraped data
        yield {
            'url': response.url,
            'body_text': body_text
        }

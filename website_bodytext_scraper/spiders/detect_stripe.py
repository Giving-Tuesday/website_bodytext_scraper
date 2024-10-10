import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.spiders import Rule
from website_bodytext_scraper.spiders.utils import generate_directory
# from website_bodytext_scraper.spiders.constants import manual_donation_pages_urls
import logging
from twisted.internet.error import ConnectionRefusedError

manual_donation_pages_urls = [
    'https://www.abcap.net/donate.html',
    'https://abcinc.org/donate/',
    'https://www.paypal.com/paypalme/LifeCenterVenangoCo',
    'https://www.abetterinternet.org/donate/',
    'https://secure.qgiv.com/for/4adfu8',
    'https://able-inc.org/donate/',
    'https://secure.everyaction.com/7NqPPSxbgkWuJaBjNSV8PQ2',
    'https://aboutcare.org/donations/',
    'https://www.abgf.org/donate',
    'https://acapnj.org/give/',
    'https://www.paypal.com/donate/?hosted_button_id=D466PX9JA63DW',
    'https://acc-ef.org/foundation/donate/donate-now.html',
    'https://www.access-psychology.org/donate/',
    'https://www.paypal.com/donate?hosted_button_id=ZEZYGDYKVQ64G',
    'https://secure.anedot.com/michigan-center-of-accountability-for-republicans/donate',
    'https://secure.lglforms.com/form_engine/s/dSiQp1WQBE6HaviNjjVzMg',
    'https://donorbox.org/american-council-of-engineering-companies-of-arizona-pac?utm_medium=qrcode&utm_source=qrcode',
    'https://secure.anedot.com/michigan-center-of-accountability-for-republicans/donate',
    'https://aciint.org/giving/online-giving/',
    'https://acornclinic.org/donate/',
    'https://acpmp.org/get-involved/donate/',
    'https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=LLYGMECLBHDYE&source=url&ssrt=1727721996964'
]


class DetectStripeSpider(scrapy.Spider):
    name = "detect_stripe"
    rules = (
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    custom_settings = {
            'FEEDS': { 
                'website_bodytext_scraper/dev_exports/stripe_%(time)s.csv': { 
                    'format': 'csv',
                    'overwrite': True,
                    }
                },
            'FEED_EXPORT_FIELDS': ['url', 'success', 'stripe_detected','stripe_code','error_code'],
            # Toggling user a agent on 
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            # Toggling obey robots.txt
            # 'ROBOTSTXT_OBEY': False
            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def start_requests(self):
        """Start with URLs and rules dynamically set"""
        urls = manual_donation_pages_urls
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page, errback=self.parse_error)


    def parse(self, response):
        """
        Extract and filter links from the start page.

        Extracts all links using LinkExtractor, filters them based on allowed domains,
        logs the number of allowed links, and initiates requests for each allowed link.

        """

        links = LinkExtractor().extract_links(response)
        allowed_domains = urlparse(response.url).netloc
        allowed_links = [
            link for link in links if urlparse(
                link.url).netloc in allowed_domains]

        for link in allowed_links:
            self.logger.info(f"Link: {link.url}")
            yield scrapy.Request(
                link.url,
                callback=self.parse_page,
                errback=self.parse_error)
    
    def parse_page(self, response: scrapy.http.Response):
        selectors = [
            '.asp-stripe-form',
            '#wc-stripe-blocks-checkout-style-css',
            '#stripe-checkout-button-css',
            '#simpay-stripe_checkout-form-wrap-4013',
            '#simpay-checkout-form simpay-form-4013 simpay-checkout-form--stripe_checkout',
            '#simpay-btn simpay-payment-btn simpay-disabled stripe-button-el',
            '#simpay-stripe_checkout-form-wrap-4102',
            '#simpay-checkout-form simpay-form-4102 simpay-styled',
            '#simpay-checkout-form--stripe_checkout simpay-checkout-form--stripe_checkout-styled',
            '#simpay-btn simpay-payment-btn simpay-disabled stripe-button-el'
            #TODO: Add Stripe Elements code
        ]

        snippets = []
        for selector in selectors:
            scrape = response.css(selector).getall()
            snippets.extend(scrape)

        yield {
                "url": response.url,
                "success": True,
                "stripe_detected": True if snippets else False,
                "stripe_code": snippets,
                "error_code": None
            }
        
    def parse_error(self, failure: scrapy.spidermiddlewares.httperror.HttpError):
        url: str = failure.request.url
        
        # Custom handling for Twisted errors not handled automatically by Scrapy
        if failure.check(ConnectionRefusedError):
            reason = "ConnectionRefusedError: Connection was refused by other side"
        else:
            reason = repr(failure.value)  # Fallback to the full error representation

        yield {
                "url": url,
                "success": False,
                "stripe_detected": None,
                "stripe_code": None,
                "error_code": reason
        }
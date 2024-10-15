import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.spiders import Rule
from website_bodytext_scraper.spiders.utils import load_urls_from_csv
# from website_bodytext_scraper.spiders.constants import manual_donation_pages_urls
import logging
from twisted.internet.error import ConnectionRefusedError
from scrapy.spidermiddlewares.httperror import HttpError


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

initial_urls = [
    'https://www.abcap.net/',
    'https://abcinc.org/',
    'https://herlifecenter.com/',
    'https://www.abetterinternet.org/',
    'https://www.abide.org/',
    'https://able-inc.org/',
    'https://abolitionistlawcenter.org/',
    'https://aboutcare.org/',
    'https://acapnj.org/',
    'https://www.abundantlivingministries.org/', # Paypal
    'https://acc-ef.org',
    'https://www.access-psychology.org/',
    'https://www.accessabilitywi.org/',
    'https://accountablemichigan.com/', # Anedot
    'https://achievebrowncounty.org/',
    'https://www.acecaz.org/', # Donorbox
    'https://www.achildbecomes.org/',
    'https://aciint.org/',
    'https://acornclinic.org/',
    'https://acpmp.org/',
    'https://activemeditation.org/',
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
            'FEED_EXPORT_FIELDS': ['url', 'domain', 'success', 'stripe_detected','stripe_code','error_code','flags'],
            # Toggling user a agent on 
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            # Toggling obey robots.txt
            # 'ROBOTSTXT_OBEY': False
            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = 'website_bodytext_scraper/data/oct_11_run/bodytext_inputs_test.csv'
        self.column_index = 0
        
    def start_requests(self):
        """Start with URLs and rules dynamically set"""
        # urls = manual_donation_pages_urls
        # urls = initial_urls
        urls = load_urls_from_csv(self.file_path, self.column_index)
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_start_page, errback=self.parse_error)

    def parse_start_page(self, response):
        """
        Extract and filter links from the start page.

        Extracts all links using LinkExtractor, filters them based on allowed domains,
        logs the number of allowed links, and initiates requests for each allowed link.

        """

        links = LinkExtractor().extract_links(response)
        allowed_domain = urlparse(response.url).netloc
        allowed_links = [
            link for link in links if urlparse(link.url).netloc in allowed_domain
            ]

        # Determine if original response.url contains 3rd party links 
        # TODO: Ensure donorbox can be caught
        third_parties = ['donorbox.org', 'anedot.com', 'paypal.com']
        contains_third_party = False
        third_party_detected = None
        for link in links:
            for org in third_parties:
                if org in link.url:
                    contains_third_party = True
                    third_party_detected = org

        # Decide whether or not to launch scrape for ALL allowed links
        if contains_third_party:
            yield {
                    "url": link.url,
                    "domain": allowed_domain,
                    "success": True,
                    "stripe_detected": 'Unknown',  # Placeholder for more specific detection logic
                    "stripe_code": None,
                    "error_code": None,
                    "flags": f'Uses 3rd party: {third_party_detected}'
                }
        else:
            for link in allowed_links:
                yield scrapy.Request(
                    link.url,
                    callback=self.parse_page,
                    errback=self.parse_error,
                    meta={'domain': allowed_domain})
    
    def parse_page(self, response: scrapy.http.Response):
        domain = response.meta.get('domain')
        selectors = [
            '.asp-stripe-form',
            # '#wc-stripe-blocks-checkout-style-css', # Appears may not be Stripe-related
            # '#stripe-checkout-button-css', # Appears may not be Stripe-related
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
            "domain": domain,
            "success": True,
            "stripe_detected": True if snippets else False,
            "stripe_code": snippets,
            "error_code": None,
            "flags": None
        }
        
    def parse_error(self, failure: HttpError):
        url = failure.request.url
        domain = failure.request.meta.get('domain')

        # Custom handling for Twisted errors not handled automatically by Scrapy
        if failure.check(ConnectionRefusedError):
            reason = "ConnectionRefusedError: Connection was refused by other side"
        else:
            reason = repr(failure.value)  

        yield {
                "url": url,
                "domain": domain,
                "success": False,
                "stripe_detected": 'Unknown',
                "stripe_code": None,
                "error_code": reason,
                "flags": None
        }
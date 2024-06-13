# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BodyTextCrawlSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    page_traversed = scrapy.Field()
    body_text = scrapy.Field()

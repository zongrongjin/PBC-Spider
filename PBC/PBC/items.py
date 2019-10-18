# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PbcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    from_where = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    pdf_name = scrapy.Field()
    pdf_url = scrapy.Field()
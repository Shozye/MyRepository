# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZalandoproductssaleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    real_price = scrapy.Field()

    pass

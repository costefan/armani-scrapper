# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    category = scrapy.Field()
    sku = scrapy.Field()
    available = scrapy.Field()
    scanning_time = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    region = scrapy.Field()
    description = scrapy.Field()


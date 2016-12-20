# -*- coding: utf-8 -*-


import scrapy


class Jsitem(scrapy.Item):
    # amazon items
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()



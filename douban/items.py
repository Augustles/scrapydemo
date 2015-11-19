# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # amazon items
    top = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()

    # Item 对象是种简单的容器，保存了爬取到得数据
    # douban的items
    # title = scrapy.Field()
    # link = scrapy.Field()
    # rating = scrapy.Field()
    # rating_nums = scrapy.Field()
    # major = scrapy.Field()
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
    # entry_time = scrapy.Field()
    # Url = scrapy.Field()

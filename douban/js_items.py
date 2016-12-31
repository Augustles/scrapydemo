# -*- coding: utf-8 -*-


import scrapy


class Jsitem(scrapy.Item):
    # amazon items
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()

    def valid(self):
        # 必须有值的属性
        required_attrs = [
            'title',
            'url',
        ]
        for attr in required_attrs:
            if not self[attr]:
                return "%s required" % attr
        return ""



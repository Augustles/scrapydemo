# -*- coding: utf-8 -*-
import scrapy


class TestspiderSpider(scrapy.Spider):
    name = "testSpider"
    allowed_domains = ["douban.com"]
    start_urls = (
        'http://www.douban.com/',
    )

    def parse(self, response):
        pass

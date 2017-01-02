#!/usr/bin/env python
# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from datetime import datetime as dte
from scrapy.conf import settings
from douban.utils import md5

class Jianshu(scrapy.Spider):
    name = "jianshu"
    allowed_domains = []
    start_urls = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 1,
        },
        # "DOWNLOAD_DELAY": 0.15,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        'DOWNLOADER_MIDDLEWARES': {
            'douban.userAgent.JianshuHeader': 2,
        },
    }

    def start_requests(self):
        url = 'http://www.jianshu.com/'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        qs = soup.find('ul', attrs={'class': 'article-list thumbnails'}).find_all('li')
        self.logger.info('[scrapy] crawl %s items' %(len(qs)))
        for x in qs:
            try:
                title = x.h4.text
                url = 'http://www.jianshu.com' + x.h4.a['href']
                author = x.find('a', attrs={'class': 'author-name blue-link'}).text
                attrs = dict(
                        title=title,
                        url=url,
                        author=author,
                        source='jianshu',
                        )
                yield scrapy.Request(url, meta={'attrs': attrs}, callback=self.parse_content)
            except:
                pass

    def parse_content(self, response):
        soup = bs(response.body, 'lxml')
        attrs = response.meta['attrs']
        content = soup.find('div', attrs={'class': 'show-content'}).text
        attrs.update(content=content)
        yield Jsitem(**attrs)

#!/usr/bin/env python
# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from datetime import datetime as dte
from scrapy.conf import settings
from douban.utils import md5


class Daily_zhihu(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = []
    start_urls = []
    custom_settings = {
        'DNSCACHE_ENABLED': True,
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'douban.userAgent.JianshuHeader': 2,
        },
        'DOWNLOAD_DELAY': 0.75,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
    }


    def start_requests(self):
        url = 'http://daily.zhihu.com/'
        for x in xrange(1):
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        qs = soup.find('div', attrs={'class': 'main-content-wrap'}).find_all('div', attrs={'class': 'wrap'})
        self.logger.info('[scrapy] crawl %s items' %(len(qs)))
        for x in qs:
            try:
                url = 'http://daily.zhihu.com' + x.find('a').get('href', '')
                attrs = dict(
                        url=url,
                        source='daily_zhihu',
                        )
                yield scrapy.Request(url, meta={'attrs': attrs}, callback=self.parse_content)
            except:
                pass

    def parse_content(self, response):
        soup = bs(response.body, 'lxml')
        attrs = response.meta['attrs']
        title = soup.h1.text
        author = soup.find('span', attrs={'class': 'author'}).text
        content = soup.find('div', attrs={'class': 'content-inner'}).text
        attrs.update(
            author=author,
            content=content,
            title=title,
        )
        yield Jsitem(**attrs)

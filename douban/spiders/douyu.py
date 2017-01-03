#!/usr/bin/env python
# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from datetime import datetime as dte
from scrapy.conf import settings
from douban.utils import md5
from selenium import webdriver


class Douyu(scrapy.Spider):
    name = 'douyu'
    allowed_domains = []
    start_urls = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'douban.userAgent.JianshuHeader': 2,
        },
        'DOWNLOAD_DELAY': 0.75,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def get_page(self, url):
        dr = webdriver.PhantomJS()
        dr.get(url)
        soup = bs(dr.page_source, 'lxml')
        page = max([int(x.text) for x in soup.find('div', attrs={'class': 'tcd-page-code'}).find_all('a') if x.text.isdigit()])
        return page

    def start_requests(self):
        start = 'https://www.douyu.com/directory/all'
        page = self.get_page(start)
        for x in xrange(1, page+1):
            url = 'https://www.douyu.com/directory/all?page=%s&isAjax=1' %x
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        qs = soup.find_all('a', attrs={'data-rid': True})
        self.logger.info('[scrapy] crawl %s items' %(len(qs)))
        for x in qs:
            try:
                title = x.text
                url = 'https://www.douyu.com' + x.get('href', '')
                attrs = dict(
                    title=title,
                    url=url,
                    source='douyu',
                )
                yield Jsitem(**attrs)
            except:
                pass


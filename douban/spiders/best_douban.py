#!/usr/bin/env python
# encoding: utf-8

import scrapy
import hashlib
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from scrapy.conf import settings
from douban.utils import md5


class BestDb(scrapy.Spider):
    name = 'best_db'
    allowed_domains = []
    start_urls = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 300,
        },
        'DOWNLOAD_DELAY': 0.75,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
    }


    def start_requests(self):
        for x in xrange(0, 101, 20):
            url = 'https://movie.douban.com/review/best/?start=%s' %x
            print url
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        qs = soup.find('div', attrs={'class': 'review-list chart'}).find_all('h3', attrs={'class': 'title'})
        self.logger.info('[scrapy] crawl %s items' %(len(qs)))
        for x in qs:
            try:
                url = x.find('a').get('href', '')
                title = x.text
                attrs = dict(
                        title=title,
                        url=url,
                        source='best_db'
                        )
                yield scrapy.Request(url, meta={'attrs': attrs}, callback=self.parse_content)
            except:
                pass

    def parse_content(self, response):
        soup = bs(response.body, 'lxml')
        attrs = response.meta['attrs']
        author = soup.find('span', attrs={'property': 'v:reviewer'}).text
        content = soup.find('div', attrs={'id': 'link-report'}).text
        attrs.update(author=author, content=content)
        yield Jsitem(**attrs)


    def get_md5(self, msg):
        md5 = hashlib.md5(msg.encode('utf-8')).hexdigest()
        return md5



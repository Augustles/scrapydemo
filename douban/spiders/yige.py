#!/usr/bin/env python
# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup as bs
import re
from douban.js_items import Jsitem
from datetime import datetime as dte
from scrapy.conf import settings
import requests

class One(scrapy.Spider):
    name = 'one'
    allowed_domains = []
    start_urls = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 300,
        },
        'DOWNLOAD_DELAY': 1.75,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def get_urls(self, url):
        urls = set()
        while True:
            r = requests.get(url)
            soup = bs(r.content, 'lxml')
            ret = soup.find('div', attrs={'class': 'list-footer'}).find_all('td')
            if len(ret) < 3:
                break
            for x in ret:
                text = x.a.text
                if re.match(r'\d+', text):
                    url = 'http://m.wufazhuce.com/article?page=%s' %(re.match(r'\d+', text).group(0))
                    print url
                    urls.add(url)

        return urls


    def start_requests(self):
        url = 'http://m.wufazhuce.com/article?page=1'
        # yield scrapy.Request(url, callback=self.parse)
        urls = self.get_urls(url)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        qs = soup.find('div', attrs={'role': 'main'}).find_all('div', attrs={'class': 'item-text link-div'})
        self.logger.info('[scrapy] crawl %s items' %(len(qs)))
        for x in qs:
            try:
                pre = x.find('p', attrs={'class': 'text-title'}).text
                url = x.find('a').get('href', '')
                title = pre.split()[0]
                author = pre.split()[1].encode('utf-8').split('／')[-1].decode('utf-8')
                attrs = dict(
                        title=title,
                        url=url,
                        author=author,
                        source='one',
                        )
                yield scrapy.Request(url, meta={'attrs': attrs}, callback=self.parse_content)
            except:
                pass

    def parse_content(self, response):
        soup = bs(response.body, 'lxml')
        attrs = response.meta['attrs']
        content = soup.find('div', attrs={'class': 'text-content'}).text
        attrs.update(content=content)
        yield Jsitem(**attrs)

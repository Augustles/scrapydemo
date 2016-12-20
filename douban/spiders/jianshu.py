#!/usr/bin/env python
# encoding: utf-8

import scrapy
import json
import datetime
import urllib
import hashlib
from bs4 import BeautifulSoup as bs
import re
from douban.js_items import Jsitem
from datetime import datetime as dte
from scrapy.conf import settings
import scrapy
import requests


class Jianshu(scrapy.Spider):
    name = "jianshu"
    custom_settings = {
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 300,
        },
        # "DOWNLOAD_DELAY": 0.15,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def start_requests(self):
        url = 'http://www.jianshu.com/'
        yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        soup = bs(response.body, 'lxml')
        qs = soup.find('ul', attrs={'class': 'article-list thumbnails'}).find_all('li')
        for x in qs:
            try:
                title = x.h4.text
                url = 'http://www.jianshu.com' + x.h4.a['href']
                author = x.find('a', attrs={'class': 'author-name blue-link'}).text
                print title, author, url
                attrs = dict(
                        title=title,
                        url=url,
                        author=author,
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


    def get_md5(self, msg):
        md5 = hashlib.md5(msg.encode('utf-8')).hexdigest()
        return md5



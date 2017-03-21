#!/usr/bin/env python
# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from datetime import datetime as dte
from scrapy.conf import settings
from douban.utils import md5
from scrapy.shell import inspect_response
import json


class Daily_zhihu(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = []
    start_urls = []
    custom_settings = {
        'DNSCACHE_ENABLED': True,
        "ITEM_PIPELINES": {
            'douban.pipelines.JsonWriterPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'douban.userAgent.ZhihuHeader': 2,
        },
        'DOWNLOAD_DELAY': 0.75,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
    }


    def start_requests(self):
        # url = 'http://daily.zhihu.com/'
        for x in xrange(0, 120, 20):
            url = 'https://zhuanlan.zhihu.com/api/columns/yeka52/posts?limit=20&offset=%s' %(x)
            print url
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # soup = bs(response.body, 'lxml')
        # inspect_response(response, self)
        # qs = soup.find('div', attrs={'class': 'main-content-wrap'}).find_all('div', attrs={'class': 'wrap'})

        qs = json.loads(response.body)
        self.logger.info('[scrapy] crawl %s items url: %s' %(len(qs), response.url))
        for x in qs:
            try:
                # url = 'https://www.zhihu.com' + x['url']
                name = x['author']['name']
                title = x['title']
                content = x['content']
                content = bs(content, 'lxml')
                content = content.text.encode('utf-8')
                attrs = dict(
                    # url=url,
                    source='zhihu',
                    name=name,
                    title=title,
                    content=content,
                    )
                # print attrs
                with open('yeka52_demo.json', 'a+') as f:
                    f.write(json.dumps(attrs)+'\n')
                # yield Jsitem(**attrs)
                # yield scrapy.Request(url, meta={'attrs': attrs}, callback=self.parse_content)
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

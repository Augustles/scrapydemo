#!/usr/bin/env python
# encoding: utf-8

import scrapy
import hashlib
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from scrapy.conf import settings
from douban.utils import md5
import requests


class Movie_db(scrapy.Spider):
    name = 'movie_db'
    allowed_domains = []
    start_urls = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 300,
        },
        # 'DOWNLOAD_DELAY': 0.75,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }
    def from_doulist(self, url):
        r = requests.get(url)
        soup = bs(r.content, 'lxml')
        doulist = set([x.get('href', '') for x  in soup.find_all('a') if 'subject' in x.get('href', '')])
        return doulist

    def from_doulist_list(self, url):
        r = requests.get(url)
        soup = bs(r.content, 'lxml')
        print r.url
        page = soup.find('div', attrs={'class': 'paginator'}).find_all('a')[-2]
        ret = set()
        try:
            page = int(page.text)
        except:
            page = 0
        for x in xrange(page):
            tmp = '%s?start=%s&sort=seq&sub_type=' %(url, x*20)
            print tmp
            urls = self.from_doulist(tmp)
            ret = ret.union(urls)
        return ret

    def get_subject1(self, url):
        urls = set()
        r = requests.get(url)
        soup = bs(r.content, 'lxml')
        info = soup.find_all('a')
        for x in info:
            url = x.get('href', '')
            if 'subject' in url:
                urls.add(url)
            elif url == 'https://movie.douban.com/tag/':
                pass
            elif 'doulist' in url or 'tag' in url:
                print url
                doulist = self.from_doulist_list(url)
                urls = urls.union(doulist)
            else:
                pass
        return urls

    def get_subject(self, url):
        urls = set()
        r = requests.get(url)
        soup = bs(r.content, 'lxml')
        info = soup.find_all('a')
        for x in info:
            if 'tag' in x.get('href', ''):
                try:
                    url = 'https://movie.douban.com' + x.get('href', '')
                    print url
                    ret = self.from_doulist_list(url)
                    urls = urls.union(ret)
                except:
                    pass
        return urls

    def start_requests(self):
        # url = 'https://movie.douban.com/tag/1890s'
        # urls = self.from_doulist_list(url)
        # start = 'https://movie.douban.com/tag/'
        start = 'https://movie.douban.com/tag/%E6%97%A5%E6%9C%AC/'
        urls = self.from_doulist_list(start)
        print len(urls)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        try:
            title = soup.find('h1').text
            rate = soup.find('strong', attrs={'class': 'll rating_num'}).text
            url = response.url
            attrs = dict(
                title=title,
                url=url,
                author=rate,
                source='movie_db'
            )
            yield Jsitem(**attrs)
        except Exception as e:
            self.logger.info('[scrapy] movie error %s items' %(e))

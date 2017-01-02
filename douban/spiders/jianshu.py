#!/usr/bin/env python
# encoding: utf-8

import scrapy
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from datetime import datetime as dte
from scrapy.conf import settings
from douban.utils import md5
import requests
from time import sleep
from douban.proxy import get_redis

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

    def get_user(self, url):
        users = set()
        r = requests.get(url)
        soup = bs(r.content, 'lxml')
        for x in soup.find_all('h4'):
            url = 'http://www.jianshu.com' + x.a.get('href', '')
            print url
            users.add(url)
        return users

    def get_follow(self, url):
        users = set()
        r = requests.get(url)
        soup = bs(r.content, 'lxml')
        print r.url
        try:
            url = soup.find('li', attrs={'class': 'last'}).a.get('href', '')
            tmp = url.split('=')
            n = int(tmp[-1])
            tmp[-1] = '%d'
            url = '='.join(tmp)
        except:
            for x in soup.find_all('h4'):
                url = 'http://www.jianshu.com' + x.a.get('href', '')
                print url
                users.add(url)
            return users

        for x in range(1, n+1):
            tmp = 'http://www.jianshu.com' + url %x
            ret = self.get_user(tmp)
            users = users.union(ret)
        return users

    def get_post(self, url):
        urls = set()
        users = set()
        while True:
            r = requests.get(url)
            soup = bs(r.content, 'lxml')
            info = soup.find_all('a', attrs={'target': '_blank'})
            for x in info:
                tmp = 'http://www.jianshu.com' + x.get('href', '')
                if '/p/' in tmp and '#' not in tmp:
                    # urls.add(tmp)
                    pass
                elif '/users/' in tmp:
                    following = self.get_follow(tmp + '/following')
                    follower = self.get_follow(tmp + '/follower')
                    users = users.union(following)
                    users = users.union(follower)
            try:
                url = 'http://www.jianshu.com' + soup.find('div', attrs={'class': 'load-more'}).button.get('data-url', '')
            except:
                break
        rds = get_redis('default')
        try:
            ret = rds.smembers('user:jianshu:crawl')
            urls = urls - ret
            for x in urls:
                ret = rds.sadd('user:jianshu:crawl', x)
        except:
            pass
        return users

    def start_requests(self):
        url = 'http://www.jianshu.com/'
        # urls = self.get_post(url)
        url = 'http://www.jianshu.com/users/2a6a6a794e37/followers'
        users = self.get_post(url)
        print len(users)
        for x in users:
            yield scrapy.Request(x, callback=self.parse_user)
        # for x in urls:
            # tmp_url = 'http://www.jianshu.com%s' % x
            # print tmp_url
            # yield scrapy.Request(tmp_url, callback=self.parse_content)

    def parse_user(self, response):
        soup = bs(response.body, 'lxml')
        title = soup.h3.text
        content = soup.find('div', attrs={'class': 'people'}).text
        url = response.url
        attrs = dict(
            title=title,
            url=url,
            content=content,
            source='users_jianshu',
        )
        yield Jsitem(**attrs)

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
        title = soup.h1.text
        author = soup.find('a', attrs={'class': 'author-name'}).text
        url = response.url
        attrs = dict(
            title=title,
            url=url,
            author=author,
            source='jianshu'
        )
        yield Jsitem(**attrs)

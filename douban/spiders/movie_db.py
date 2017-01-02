#!/usr/bin/env python
# encoding: utf-8

import scrapy
import hashlib
from bs4 import BeautifulSoup as bs
from douban.js_items import Jsitem
from scrapy.conf import settings
from douban.utils import md5, is_url, gen_bids
from random import choice
import requests
from douban.proxy import get_redis


class Movie_db(scrapy.Spider):
    name = 'movie_db'
    headers = {
        'User-Agent': 'Baiduspider',
    }
    custom_settings = {
        "ITEM_PIPELINES": {
            'douban.pipeline.MongoDBPipeline': 1,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'douban.userAgent.DoubanHeader': 2,
        },
        'DOWNLOAD_DELAY': 0.15,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def from_doulist(self, url):
        try:
            headers = {
                'User-Agent': 'Baiduspider',
            }
            cookies = {
                'bid': choice(gen_bids()),
            }
            r = requests.get(url, headers=headers, cookies=cookies)
            soup = bs(r.content, 'lxml')
            doulist = set([x.get('href', '') for x  in soup.find_all('a') if 'subject' in x.get('href', '')])
            return doulist
        except Exception as e:
            self.logger.info('[scrapy] movie error %s items' %(e))

    def from_doulist_list(self, url):
        try:
            headers = {
                'User-Agent': 'Baiduspider',
            }
            cookies = {
                'bid': choice(gen_bids()),
            }
            r = requests.get(url, headers=headers, cookies=cookies)
            soup = bs(r.content, 'lxml')
            print r.url
            pre = soup.find('div', attrs={'class': 'paginator'}).find_all('a')[-2]
            ret = set()
            try:
                start = int(pre.get('href', '',).split('?')[-1].split('&')[0].split('=')[1])
                page = int(pre.text)
                n = start/(page-1)
            except:
                page = 0
                n = 0
            for x in xrange(page-1):
                tmp = '%s?start=%s&sort=seq&sub_type=' %(url, x*n)
                print tmp
                urls = self.from_doulist(tmp)
                ret = ret.union(urls)
            return ret
        except Exception as e:
            self.logger.info('[scrapy] movie error %s items' %(e))


    def get_subject(self, url):
        urls = set()
        headers = {
            'User-Agent': 'Baiduspider',
        }
        cookies = {
            'bid': choice(gen_bids()),
        }
        print cookies
        r = requests.get(url, headers=headers, cookies=cookies)
        soup = bs(r.content, 'lxml')
        print soup
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

        rds = get_redis('default')
        try:
            ret = rds.smembers('movie:douban:crawl')
            urls = urls - ret
            for x in urls:
                ret = rds.sadd('movie:douban:crawl', x)
        except:
            pass
        return urls

    def start_requests(self):
        # url = 'https://movie.douban.com/tag/1890s'
        # urls = self.from_doulist_list(url)
        # start = 'https://movie.douban.com/tag/'
        start = 'https://movie.douban.com/tag/?view=cloud'
        urls = self.get_subject(start)
        # start = 'https://movie.douban.com/tag/%E6%97%A5%E6%9C%AC/'
        # urls = self.from_doulist_list(start)
        # print len(urls)
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

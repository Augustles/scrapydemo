# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from douban.items import DoubanItem
from bs4 import BeautifulSoup as bs
import re


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    download_delay = 5
    DOWNLOAD_TIMEOUT = 30
    start_urls = []
    for x in range(1, 5):
        start_urls.append(
            'https://www.amazon.com/s/ref=sr_pg_{0}?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A1266092011%2Cn%3A172659%2Cp_36%3A0-199999%2Cp_n_feature_keywords_three_browse-bin%3A7688788011&page={1}&ie=UTF8'.format(x, x))

    def parse(self, response):
        # 自动识别编码
        soup = bs(response.body)
        all = soup.find('div', attrs={'id': re.compile(
            r"\w+Results"), 'class': True}).find_all('li',attrs={'id':True})
        # .find_all(
        #     'li', attrs={'id': re.compile(r"result\_\d+"), 'data-asin': True, 'class': True})
        item = DoubanItem()
        # page = response.url.split('pg_')[1][0]
        # print page
        for y in all:
            print y.get('id')
            # top = int(y.get('id').split('_')[-1]) + 1
            # url = y.find('a').get('href')
            # url = url[:url.find('ref=')]
            # prices = y.find('span', attrs={
            #                 'class': 'a-size-base a-color-price s-price a-text-bold'}).get_text()
            # # print prices
            # print top

            # print top, url
            # item['top'] = top
            # item['url'] = url
            # yield Request(url=item['url'], meta={'item': item}, callback=self.parse_item)
            # info = y.find(text=re.compile(r"id\=\"result\_\d+"))
            # info = y.extract()
            # info = info.find(text=re.compile(r"id\=\"result\_\d+"))
            # print info

    # def parse_item(self, response):
    #     item = response.meta['item']
    #     soup = bs(response.body)
    #     item['title'] = soup.h1.get_text()
    #     yield item

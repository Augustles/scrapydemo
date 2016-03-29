# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
# from zolbbs.items import ZolbbsItem
from bs4 import BeautifulSoup as bs
import chardet
import re
import math

class AmazonSpider(scrapy.Spider):
    name = "zolbbs"
    allowed_domains = ["zol.com.cn"]
    start_urls = []
    for x in xrange(2, 3):
        start_urls.append(
            'http://bbs.zol.com.cn/diybbs/p{0}.html#c'.format(x, x))


    def parse(self, response):
        try:
            soup = bs(response.body)
            # print response.request.url
            print soup.title
            print soup
            info = soup.find('table', attrs={'class':'list', 'id':'bookList'}).find_all('tr', attrs={'id':True})
            urls = []
            for i, x in enumerate(info):
                url = x.find('td', 'title').get('data-url')
                print i, url
                # urls.append('http://bbs.zol.com.cn' + url)
                # pages = x.find('td', attrs={'class':'reply'}).get_text()
                # m = re.search(r'[0-9]+', pages)
                # print m.group(0)
                # pages = int(m.group(0))/20.0
                # pages = math.ceil(pages)
                # pages = int(str(pages).split('.')[0])
                # print pages
            # if pages > 1:
            #     print pages
            #     for x in range(2, pages+1):
            #         print x
            #     url = 'http://bbs.zol.com.cn' + url[:-5] + '_{0}'.format(str(x)) + url[-5:]
            #     print url
            #     urls.append(url)
            #     yield Request(url=url,headers={'referer':url},callback=self.parse_item, dont_filter=False)


        except Exception, e:
            pass
        # print soup.title
        # all = soup.find('div', attrs={'id': re.compile(
        #     r"\w+Results"), 'class': True}).find_all('li', attrs={'id': True})
        # .find_all(
        #     'li', attrs={'id': re.compile(r"result\_\d+"), 'data-asin': True, 'class': True})
        # item = ZolbbsItem()

    # def parse_item(self, response):
    #     print response.request.headers.get('Referer', None)
    #     try:
    #         soup = bs(response.body, from_encoding=chardet.detect(
    #         response.body).get('encoding'))

    #         # print soup.title
    #         topictitle = soup.h1.get_text()
    #         topicuser = soup.find('p', attrs={'class':'name'}).get_text()
    #         topictime = soup.find('td', attrs={'class':'post-title clearfix'}).get_text()
    #         topicmain = soup.find('div', attrs={'id':'bookContent'}).get_text()
    #         print topictitle, topicuser, topictime, topicmain
    #         info = soup.find('div', attrs={'class':'wrapper'}).find_all('table', attrs={'class':'post-list  box-shadow replyList', 'data-id':True})

    #         for x in info:
    #             postuser = x.find('a', attrs={'class':'user-name'}).get_text()
    #             posttime = x.find('span', attrs={'class':'floor'}).get_text()
    #             postfloor = x.find('span', attrs={'class':'publish-time'}).get_text()
    #             postmain = x.find('td', attrs={'class':'post-main'}).get_text()
    #             print postuser, posttime, postfloor, postmain
    #     except Exception, e:
    #         pass


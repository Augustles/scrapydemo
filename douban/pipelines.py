# -*- coding: utf-8 -*-

import scrapy
from scrapy.pipelines.images import ImagesPipeline
# from scrapy.shell import inspect_response
from urlparse import unquote


class DoubanPipeline(ImagesPipeline):
    # get_media_requests函数下载

    def get_media_requests(self, item, spider):
        for url in item['image_urls']:  # file_urls
            yield scrapy.Request(url)

    # 修改lib/python2.7/site-packages/scrapy/pipelines/image.py
    # file_path文件名修改
    # 定制图片名称, 一般进行url编码
    # 网址后面加public/p2263672366.jpg#title
    def file_path(self, request, response=None, info=None):
        if '#' in request.url:
            image_guid = request.url.split('#')[-1]
            image_guid = unquote(image_guid).decode('utf') + '.jpg'
        else:
            image_guid = request.url.split('/')[-1]
        open("image_urls.txt", "a").write(image_guid + "\n")
        return 'full/%s' % (image_guid)

    # 过滤掉一些不符合的item
    # def process_item(self, item, spider):
    #     for word in self.words_to_filter:
    #         if word in unicode(item['description']).lower():
    #             raise DropItem("Contains forbidden word: %s" % word)
    #     else:
    #         return item

# import base64
import random
# Start your middleware class


class ProxyMiddleware(object):
    # overwrite process request

    def process_request(self, request, spider):
        ips = []
        with open('good_ip.txt', 'r') as f:
            for line in f:
                if line.strip():
                    ips.append(line.strip())

        ip = random.choice(ips)
        request.meta['proxy'] = "http://{0}".format(ip)
        print request.meta, request.headers

        # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass



# mysql数据库连接, 写入到mysql
# from scrapy import log
# from twisted.enterprise import adbapi
# from scrapy.http import Request
# from scrapy.exceptions import DropItem
# from scrapy.contrib.pipeline.images import ImagesPipeline
# import time
# import MySQLdb
# import MySQLdb.cursors
# import socket
# import select
# import sys
# import os
# import errno
# from hashlib import md5


# class MySQLStorePipeline(object):

#     def __init__(self):
#         self.dbpool = adbapi.ConnectionPool('MySQLdb',
#                                             db='scrapy',
#                                             user='root',
#                                             passwd='cxk517',
#                                             cursorclass=MySQLdb.cursors.DictCursor,
#                                             charset='utf8',
#                                             use_unicode=False
#                                             )

#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self._conditional_insert, item)
#         return item

#     def _conditional_insert(self, tx, item):
#         if item.get('title'):
#             linkmd5id = self._get_linkmd5id(item)
#             print linkmd5id, item['title']
#             tx.execute('insert ignore into douban (linkmd5id, title, link, image_urls) values (%s, %s, %s, %s)',
#                        (linkmd5id, item['title'], item['link'], item['image_urls']))

#     def _get_linkmd5id(self, item):
#         # 进行md5编码, 去重
#         return md5(item['link']).hexdigest()

# 保存json
# import json
# class JsonWriterPipeline(object):
#     def __init__(self):
#         self.file = open('items.jl', 'wb')
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "n"
#         self.file.write(line)
#         return item

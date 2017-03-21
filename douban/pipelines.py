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


# 根据url去重
# import os
# from scrapy.dupefilters import RFPDupeFilter


# class SeenURLFilter(RFPDupeFilter):
    # """A dupe filter that considers the URL"""

    # def __init__(self, path=None, debug=False):
        # self.urls_seen = set()
        # RFPDupeFilter.__init__(self, path)

    # def request_seen(self, request):
        # fp = self.request_fingerprint(request)
        # if fp in self.fingerprints:
            # self.fingerprints.add(fp)
            # return True
        # self.fingerprints.add(fp)
        # if self.file:
            # self.file.write(fp + os.linesep)

# # mongo已经爬去'out'字段为1
# class CustomFilter(RFPDupeFilter):

    # def __init__(self, path=None, other=None):
        # inmem = [it['url'] for it in MongoClient(settings['DBINFO']).nbbs.dsl.find({'out': 1})]
        # self.already_seen = set(inmem)
        # RFPDupeFilter.__init__(self, path, other)

    # def request_seen(self, request):
        # if request.url in self.already_seen:
            # return True
        # else:
            # pass

# # import base64
# import random
# # Start your middleware class

# # 布隆过滤, 对千万级别url有显著效果
# from pybloom import BloomFilter

# class BLOOMDupeFilter(BaseDupeFilter):
    # def __init__(self, path=None):
        # self.file = None
        # self.fingerprints = BloomFilter(capacity=1000000, error_rate=0.001)

    # @classmethod
    # def from_settings(cls, settings):
        # return cls(job_dir(settings))

    # def request_seen(self, request):
        # fp = request.url
        # if fp in self.fingerprints:
            # return True
        # self.fingerprints.add(fp)
        # return False

    # def close(self, reason):
        # self.fingerprints = None

# 代理组件
class ProxyMiddleware(object):
    # overwrite process request

    def process_request(self, request, spider):
        ips = []
        with open('ava_ip.txt', 'r') as f:
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


# mongo组件
import pymongo

# from scrapy import log
# from scrapy.conf import settings
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        self.server = 'localhost'
        self.port = 27017
        self.db = 'amazon'
        self.col = 'hello'
        connection = pymongo.MongoClient(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        err_msg = ''
        for field, data in item.items():
            if not data:
                pass
                # err_msg += 'Missing %s of poem from %sn' % (field, item['url'])
        if err_msg:
            raise DropItem(err_msg)
        self.collection.insert(dict(item))  # , upsert=True, safe=True
        item['topicurl'] = str(result)
        log.msg('Item %s written to MongoDB database %s/%s' % (result, self.db, self.col),
                level=log.DEBUG, spider=spider)
        return item


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
#                                             passwd='Cxk517',
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
import json
class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "n"
        self.file.write(line)
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagePipeline


class DoubanPipeline(ImagePipeline):
    # get_media_requests函数下载

    def get_media_requests(self, item, spider):
        for url in item['images_urls']:
            yield scrapy.Request(url)

    # 修改lib/python2.7/site-packages/scrapy/pipelines/image.py
    # file_path文件名修改
    # def file_path(self, request, item, response=None, info=None):
    #     open("image_urls.txt","a").write(request.url + "\n")
    #     image_guid = request.url.split('/')[-1]
    #     image_guid = item['image_name']
    #     return 'full/%s' % (image_guid)

    # 过滤掉一些不符合的item
    # def process_item(self, item, spider):
    #     for word in self.words_to_filter:
    #         if word in unicode(item['description']).lower():
    #             raise DropItem("Contains forbidden word: %s" % word)
    #     else:
    #         return item

# mysql数据库连接
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


# class MySQLStorePipeline(object):

#     def __init__(self):
#         self.dbpool = adbapi.ConnectionPool('MySQLdb',
#                                             db='test',
#                                             user='root',
#                                             passwd='root',
#                                             cursorclass=MySQLdb.cursors.DictCursor,
#                                             charset='utf8',
#                                             use_unicode=False
#                                             )

#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self._conditional_insert, item)
#         return item

#     def _conditional_insert(self, tx, item):
#         if item.get('title'):
#             for i in range(len(item['title'])):
#                 tx.execute(
#                     'insert into book values (%s, %s)', (item['title'][i], item['link'][i]))

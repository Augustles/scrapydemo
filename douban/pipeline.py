# coding=utf-8

import pymongo
from scrapy.exceptions import DropItem
from utils import md5
from datetime import datetime as dte


class MongoDBPipeline(object):

    def __init__(self):
        self.server = 'localhost'
        self.port = 27017
        self.db = 'web'
        self.col = 'jianshu'
        self.client = pymongo.MongoClient(self.server, self.port, connect=False)
        db = self.client[self.db]
        self.collection = db[self.col]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        err = item.valid()
        if err:
            spider.logger.error(err)
            return
        data = dict(item)
        data['update_datetime'] = dte.now()
        data['create_datetime'] = dte.now()
        if data['source'] in ['douyu',]:
            link_id = md5('%(url)s' %data)
        else:
            link_id = md5('%(title)s-%(url)s' %data)
        # print link_id
        data['link_id'] = link_id
        pk = {
            'link_id': link_id
        }
        self.collection.replace_one(pk, data, upsert=True)


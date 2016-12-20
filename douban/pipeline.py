# coding=utf-8

import pymongo
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        self.server = 'localhost'
        self.port = 27017
        self.db = 'web'
        self.col = 'jianshu'
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


# -*- coding: utf-8 -*-

# scrapy-redis实现分布式爬取
# pip install scrapy-redis

BOT_NAME = ['douban', ]

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

DOWNLOADER_MIDDLEWARES = {
    #  "douban.middleware.UserAgentMiddleware": 401,
    #  "douban.middleware.CookiesMiddleware": 402,
}
ITEM_PIPELINES = ["douban.pipelines.MongoDBPipleline"]

# 调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

REDIE_URL = None
# 指定master/slave主机地址,
# 这个地方slave会从master的host去读取需要爬取的队列
# master和slave的机子配置是不一样的
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

DOWNLOAD_DELAY = 2  # 间隔时间
# 添加队列
#  import redis
#  r = redis.Redis()
#  r.lpush('douban:start_urls', 'https://github.com/rolando/scrapy-redis')
#  # 删除键值
#  r.rpop('douban:start_urls')

#  COMMANDS_MODULE = 'douban.commands'
# LOG_LEVEL = 'INFO'  # 日志级别
# CONCURRENT_REQUESTS = 1
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1

# -*- coding: utf-8 -*-

# Scrapy settings for douban project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
import time
# scrapy crawl douban -s LOG_FILE=/tmp/dmoz.log
BOT_NAME = 'douban'

fn = time.strftime('%Y-%m-%d|%H:%M:%S',time.localtime(time.time())) + '.log'
LOG_FILE='/tmp/scrapy/logs/%s' %fn
# LOG_FORMAT= '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s'
SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'
# LOG_LEVEL = 'WARNING'
# 开启pipeimage组件
# ITEM_PIPELINES = {
    # # 'douban.pipelines.DoubanPipeline': 500,
    # # 'douban.pipelines.MySQLStorePipeline': 2, # mysql
    # # 'douban.pipelines.MongoDBPipeline': 501,  # mongo
    # # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1, # 默认image的pipe
    # # 'douban.pipelines.DuplicatesPipeline': 502,
# }
# 下载位置
# IMAGES_STORE = os.getcwd() + 'img'
# 爬取速率
# DOWNLOAD_DELAY = 1
# 宽度优先, 质量高
# SCHEDULER_ORDER = 'BFO'
# 最大并行请求数
# CONCURRENT_REQUESTS_PER_SPIDER = 3
# dns cache提高性能
# EXTENSIONS = {'scrapy.contrib.resolver.CachingResolver': 0, }
# DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # 'douban.userAgent.RandomUserAgentMiddleware': 2,  # 随机user-agent
    # # 'douban.pipelines.ProxyMiddleware': 3,  # 代理ip
# }
# douban.spiders为目录, userAgent是文件

# 去重组件
# DUPEFILTER_CLASS = 'douban.pipelines.SeenURLFilter'
# mongo设置
# MONGODB_HOST = 'localhost'
# MONGODB_PORT = '27017'
# MONGODB_DATABASE = 'amazon'
# MONGODB_COLLECTION = 'movie'

# 日志
# LOG_ENABLED = True
# LOG_ENCODING = 'utf-8'
# LOG_FILE = '/home/adminuser/scrapy.log'
# LOG_LEVEL = 'DEBUG'
# LOG_STDOUT = True
# scrapy 主要组件

# scrapy engine， 控制整个爬虫的运行，请求调度，spider调用，下载调用，信号事件触发
# spider（蜘蛛）, 用来解析页面的类，解析后创建新的请求，或者创建数据结果集合
# scheduler（调度器）， 负责管理请求（来自spider），存入队列，执行时返回给 scrapy引擎
# Downloader（下载器），抓取页面并返回结果给spider
# Item pipeline（item管道）， 处理网页中抽取的数据结果，进行清洗，校验，存储等操作
# Downloader middlewares（下载器中间件），下载器与spider之间的勾子，可以对请求和响应的数据进行操作
# extensions（扩展），在scrapy启动时初始化，提供增强的辅助功能

# USER_AGENT = 'douban (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# 网站ip限制, crawlera
# 防止ban
# DOWNLOAD_DELAY=3

# 禁止cookies,防止ban
# COOKIES_ENABLED=False
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'


# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'douban.middlewares.MyCustomSpiderMiddleware': 543,
#}


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'user'
DB_PASSWD = 'password'
DB_DB = 'database'

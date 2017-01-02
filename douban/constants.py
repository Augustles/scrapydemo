#!/usr/bin/env python
# encoding: utf-8
"""
配置
"""

# celery异步任务
CELERY_BROKER_URL = 'redis://localhost:6379/10'

# 日志配置
import os
import logging
# from logging.handlers import SysLogHandler
from logging import Formatter, StreamHandler, FileHandler

# logging模块输出格式
fmt = Formatter('[%(asctime)s] %(levelname)s: %(message)s')
proxy_log = logging.getLogger('proxy')
# 输出到文件
fhd = logging.FileHandler('logs/proxy.log')
fhd.setFormatter(fmt)
proxy_log.addHandler(fhd)
proxy_log.setLevel(logging.INFO)
# 输出到控制台
stdout_hd = logging.StreamHandler()
stdout_hd.setFormatter(fmt)
proxy_log.addHandler(stdout_hd)
proxy_log.setLevel(logging.INFO)

# user-agent
uas = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
]
# redis
REDIS_SERVER_INFO = {'host': '127.0.0.1', 'port': 6379, 'db': '0', 'password': 'nana'}
RK_PROXY_IP_ALL = "proxy:all"
RK_PROXY_IP_DB = "proxy:douban"
RK_PROXY_IP_TC = "proxy:tongcheng"
RK_PROXY_IP_SCQCP = "proxy:scqcp"

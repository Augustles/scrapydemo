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

proxy_log = logging.getLogger("proxy")

s = proxy_log.name
f = "logs/%s.log" % s
file_hd = FileHandler(os.path.join(os.getcwd(), f))
stdout_fhd = StreamHandler()
fmt = Formatter('[%(asctime)s] %(levelname)s: %(message)s')
stdout_fhd.setLevel(logging.INFO)
stdout_fhd.setFormatter(fmt)
file_hd.setLevel(logging.INFO)
file_hd.setFormatter(fmt)
proxy_log.addHandler(stdout_fhd)
proxy_log.addHandler(file_hd)

# redis
REDIS_SERVER_INFO = {'host': '127.0.0.1', 'port': 6379, 'db': '0', 'password': 'nana'}
RK_PROXY_IP_ALL = "proxy:all"
RK_PROXY_IP_TC = "proxy:tongcheng"
RK_PROXY_IP_SCQCP = "proxy:scqcp"

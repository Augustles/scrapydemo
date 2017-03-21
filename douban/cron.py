#!/usr/bin/env python
# -*- coding:utf-8 *-*
'''
计划任务配置
'''
import requests
import traceback
import time
import os

from constants import proxy_log
from apscheduler.scheduler import Scheduler
from datetime import datetime as dte


def check(run_in_local=False):
    """
    run_in_local 是否允许在local环境运行
    """
    def wrap(func):
        def sub_wrap(*args, **kwargs):
            res = None
            try:
                # if not run_in_local:
                #     proxy_log.info("[ignore] forbid run at debug mode")
                #     return None
                t1 = time.time()
                proxy_log.info("[start] %s %s %s", func.__name__, args, kwargs)
                # with app.app_context():
                res = func(*args, **kwargs)
                cost = time.time() - t1
                # cron_log.info("[succss] %s %s %s, return: %s, cost time: %s", func.__name__, args, kwargs, res, cost)
                if res:
                    proxy_log.info("[succss] %s %s %s, return: %s, cost time: %s", func.__name__, args, kwargs, res, cost)
                else:
                    proxy_log.info("[succss] %s %s %s, return: , cost time: %s", func.__name__, args, kwargs, cost)
            except:
                proxy_log.error("%s,%s,%s", traceback.format_exc(), args, kwargs)
            return res
        return sub_wrap
    return wrap

@check(run_in_local=False)
def crawl(crawl_source, crawl_kwargs={}):
    url_list = ['http://127.0.0.1:6800/schedule.json']
    data = {
          "project": "douban",
          "spider": crawl_source,
    }
    data.update(crawl_kwargs)

    for url in url_list:
        res = requests.post(url, data=data)
        proxy_log.info('srapyd return %s' %res.json())

@check(run_in_local=False)
def crawl_proxy_xici():
    from proxy import proxy_producer
    data = {}
    cnt = proxy_producer.crawl_from_xici()
    data["xici"] = cnt
    return data

@check(run_in_local=False)
def crawl_proxy_66ip():
    from proxy import proxy_producer
    data = {}
    cnt = proxy_producer.crawl_from_66ip()
    data["66ip"] = cnt
    return data

@check(run_in_local=False)
def crawl_proxy_ip181():
    from proxy import proxy_producer
    data = {}
    cnt = proxy_producer.crawl_from_ip181()
    data["ip181"] = cnt
    return data

@check(run_in_local=False)
def crawl_proxy_haodaili():
    from proxy import proxy_producer
    data = {}
    cnt = proxy_producer.crawl_from_haodaili()
    data["haodaili"] = cnt
    return data

@check(run_in_local=False)
def crawl_proxy_kxdaili():
    from proxy import proxy_producer
    data = {}
    cnt = proxy_producer.crawl_from_kxdaili()
    data["kxdaili"] = cnt
    return data

@check(run_in_local=False)
def check_proxy():
    from proxy import proxy_producer
    for ipstr in proxy_producer.all_proxy():
        if not proxy_producer.valid_proxy(ipstr):
            proxy_producer.remove_proxy(ipstr)
    return proxy_producer.proxy_size()

@check(run_in_local=False)
def check_consumer_proxy(name):
    from tasks import check_remove_proxy_ip
    from proxy import get_proxy
    consumer = get_proxy(name)
    for ipstr in consumer.all_proxy():
        check_remove_proxy_ip.delay(name, ipstr)
    return consumer.proxy_size()

@check(run_in_local=False)
def check_kill_phantomjs():
    # phantomjs没有成功退出
    cmd = "kill -9 `ps aux|grep phantomjs|awk '{print $2}'`"
    stats = os.system(cmd)
    if stats:
        return 'success kill PhantomJS'

def main():
    sched = Scheduler(daemonic=False)

    # sched.add_cron_job(bus_crawl, hour=17, minute=0, args=['hn96520'])
    # sched.add_cron_job(crawl, hour=2, args=['one'])
    # sched.add_cron_job(crawl, hour=3, args=['zhihu'])
    # sched.add_cron_job(crawl, hour=7, args=['best_db'])
    # sched.add_interval_job(crawl, minutes=60, args=['jianshu'])
    # 代理ip相关
    # sched.add_interval_job(crawl, minutes=60, args=['douyu'])
    # sched.add_interval_job(crawl, minutes=240, args=['jianshu'])
    # sched.add_interval_job(check_kill_phantomjs, minutes=360)
    sched.add_interval_job(crawl_proxy_haodaili, minutes=2)
    sched.add_interval_job(crawl_proxy_kxdaili, minutes=5)
    sched.add_interval_job(crawl_proxy_ip181, minutes=3)
    sched.add_interval_job(crawl_proxy_66ip, minutes=2)
    sched.add_interval_job(crawl_proxy_xici, minutes=1)

    # sched.add_interval_job(check_proxy, minutes=1)
    sched.add_interval_job(check_consumer_proxy, args=["mouser"], minutes=1)
    sched.add_interval_job(check_consumer_proxy, args=["mouser"], minutes=1)
    # sched.add_interval_job(check_consumer_proxy, args=["bus365"], minutes=1)


    #(补救措施) 定时刷新状态
    # sched.add_interval_job(refresh_order_status, minutes=4)

    # 其他
    # sched.add_cron_job(delete_source_riders, hour=22, minute=40)
    # sched.add_cron_job(clear_lines, hour=1, minute=0)
    # sched.add_cron_job(clear_redis_data, hour=5, minute=0)

    sched.start()

if __name__ == '__main__':
    proxy_log.info('start cron job ...')
    main()

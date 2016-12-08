#!/usr/bin/env python
# -*- coding:utf-8 *-*
'''
计划任务配置
'''
import requests
import traceback
import time

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
                proxy_log.info("[succss] %s %s %s, return: , cost time: %s", func.__name__, args, kwargs, cost)
            except:
                proxy_log.error("%s,%s,%s", traceback.format_exc(), args, kwargs)
            return res
        return sub_wrap
    return wrap

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

def main():
    sched = Scheduler(daemonic=False)

    # sched.add_cron_job(bus_crawl, hour=2, minute=10, args=['bus365'], kwargs={"crawl_kwargs":{"city": "赤峰市,巴林左旗,巴林右旗,通辽市,海拉尔,正蓝旗,集宁区"}})
    # # 河南
    # sched.add_cron_job(bus_crawl, hour=17, minute=0, args=['hn96520'])

    # 代理ip相关
    sched.add_interval_job(crawl_proxy_haodaili, minutes=3)
    sched.add_interval_job(crawl_proxy_kxdaili, minutes=5)
    # sched.add_interval_job(crawl_proxy_ip181, minutes=1)
    # sched.add_interval_job(crawl_proxy_samair, minutes=1)
    # sched.add_interval_job(crawl_proxy_66ip, minutes=1)
    # sched.add_interval_job(crawl_proxy_zdaye, minutes=1)
    # sched.add_interval_job(crawl_proxy_xici, minutes=1)

    # sched.add_interval_job(check_proxy, minutes=1)
    # sched.add_interval_job(check_consumer_proxy, args=["tongcheng"], minutes=1)
    # sched.add_interval_job(check_consumer_proxy, args=["bus365"], minutes=1)


    #(补救措施) 定时刷新状态
    # sched.add_interval_job(refresh_order_status, minutes=4)

    # 其他
    # sched.add_cron_job(delete_source_riders, hour=22, minute=40)
    # sched.add_cron_job(clear_lines, hour=1, minute=0)
    # sched.add_cron_job(clear_redis_data, hour=5, minute=0)

    sched.start()

if __name__ == '__main__':
    main()

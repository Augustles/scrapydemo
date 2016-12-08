# coding=utf-8
"""
异步任务
"""

from celery import Celery, platforms
platforms.C_FORCE_ROOT = True    # celery需要这样

CELERY_BROKER_URL = 'redis://localhost:6379/10'
celery = Celery(__name__, broker=CELERY_BROKER_URL)

@celery.task(bind=True, ignore_result=True)
def check_add_proxy_ip(self, proxy_name, ipstr):
    from proxy import get_proxy
    consumer = get_proxy(proxy_name)
    consumer.on_producer_add(ipstr)


@celery.task(bind=True)
def check_remove_proxy_ip(self, proxy_name, ipstr):
    from proxy import get_proxy
    consumer = get_proxy(proxy_name)
    if not consumer.valid_proxy(ipstr):
        consumer.remove_proxy(ipstr)
        return "removed"

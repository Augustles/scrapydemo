#!/usr/bin/env python
# encoding: utf-8
"""
代理ip管理

1.会有定时任务从互联网上抓代理ip下来,并保存在redis上的RK_ALL_RPOXY_IP上
2.会有定时任务检测RK_PROXY_IP_ALL上IP的可用性和速度, 不满足要求的会remove掉
3.个性化定制要求
"""

import requests
import json
import random
import urllib
import re
import time

from datetime import datetime as dte, timedelta
from bs4 import BeautifulSoup
from lxml import etree

from constants import *
import redis

_redis_pool_list = {}

def get_redis(name):
    if name not in _redis_pool_list:
        # info = current_app.config["REDIS_SETTIGNS"][name]
        info = REDIS_SERVER_INFO
        pool = redis.ConnectionPool(host=info["host"],
                                    port=info["port"],
                                    db=info["db"],
                                    # password=info['password'],
                                    socket_timeout=5)
        _redis_pool_list[name] = pool
    return redis.Redis(connection_pool=_redis_pool_list[name])


class ProxyProducer(object):

    def __init__(self):
        self.consumer_list= []

    def registe_consumer(self, consumer):
        if consumer in self.consumer_list:
            return
        self.consumer_list.append(consumer)

    def crawl_from_haodaili(self):
        print('...start crawl haodaili proxy...')
        add_cnt = 0
        for i in range(1, 15):
            url = "http://www.haoip.cc/guonei/%s" % i
            try:
                r = requests.get(url, timeout=10)
            except:
                continue
            soup = BeautifulSoup(r.content, "lxml")
            for s in soup.find('table').findAll('tr'):
                td_lst = s.findAll("td")
                ip, port = td_lst[0].text.strip(), td_lst[1].text.strip()
                ipstr = "%s:%s" % (ip, port)
                print(ipstr)
                if self.valid_proxy(ipstr):
                    self.add_proxy(ipstr)
                    add_cnt += 1
        return add_cnt

    def crawl_from_kxdaili(self):
        print('...start crawl kxdaili proxy...')
        url_tpl = "http://www.kxdaili.com/dailiip/%s/%s.html"
        add_cnt = 0
        for i in [1, 2]:
            for j in range(1, 6):
                url = url_tpl % (i, j)
                try:
                    r = requests.get(url, timeout=10, headers={"User-Agent": "Chrome"})
                except Exception, e:
                    continue
                soup = BeautifulSoup(r.content, "lxml")
                for s in soup.select(".table tr")[1:]:
                    td_lst = s.findAll("td")
                    ip, port = td_lst[0].text.strip(), td_lst[1].text.strip()
                    ipstr = "%s:%s" % (ip, port)
                    print(ipstr)
                    if self.valid_proxy(ipstr):
                        self.add_proxy(ipstr)
                        add_cnt += 1
        return add_cnt

    def crawl_from_ip181(self):
        print('...start crawl ip181 proxy...')
        url_tpl = "http://www.ip181.com/daili/%s.html"
        add_cnt = 0
        for i in range(1, 6):
            url = url_tpl % i
            try:
                r = requests.get(url, timeout=10, headers={"User-Agent": "Chrome"})
            except Exception, e:
                continue
            soup = BeautifulSoup(r.content, "lxml")
            for s in soup.select(".table tr")[1:]:
                td_lst = s.findAll("td")
                ip, port = td_lst[0].text.strip(), td_lst[1].text.strip()
                speed = float(td_lst[4].text.rstrip("秒").strip())
                if speed > 1:
                    continue
                ipstr = "%s:%s" % (ip, port)
                print(ipstr)
                if self.valid_proxy(ipstr):
                    self.add_proxy(ipstr)
                    add_cnt += 1
        return add_cnt

    def crawl_from_samair(self):
        print('...start crawl samair proxy...')
        add_cnt = 0
        for i in range(1, 10):
            url = "http://www.samair.ru/proxy-by-country/China-%02d.htm" % i
            from selenium import webdriver
            driver = webdriver.PhantomJS()
            driver.get(url)
            for trobj in driver.find_elements_by_tag_name("tr"):
                lst = re.findall(r"(\d+.\d+.\d+.\d+:\d+)", trobj.text)
                for ipstr in lst:
                    print(ipstr)
                    if self.valid_proxy(ipstr):
                        self.add_proxy(ipstr)
                        add_cnt += 1
        return add_cnt

    def crawl_from_66ip(self):
        print('...start crawl 66ip proxy...')
        proxy_lst = set()
        for i in [2,3,4]:
            url = "http://www.66ip.cn/nmtq.php?getnum=150&isp=0&anonymoustype=%s&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip" % i
            try:
                r = requests.get(url, timeout=6)
            except Exception:
                continue
            proxy_lst=proxy_lst.union(set(re.findall(r"(\d+.\d+.\d+.\d+:\d+)", r.content)))
        add_cnt = 0
        for ipstr in proxy_lst:
            if self.valid_proxy(ipstr):
                self.add_proxy(ipstr)
                add_cnt += 1
        return add_cnt

    def crawl_from_zdaye(self):
        print('...start crawl haodaili proxy...')
        url = "http://api.zdaye.com/?api=201606021405523962&sleep=5%C3%EB%C4%DA&gb=2&post=%D6%A7%B3%D6&ct=200"
        proxy_lst = set()
        r = requests.get(url, timeout=6)
        proxy_lst=proxy_lst.union(set(re.findall(r"(\d+.\d+.\d+.\d+:\d+)", r.content)))
        add_cnt = 0
        for ipstr in proxy_lst:
            if self.valid_proxy(ipstr):
                self.add_proxy(ipstr)
                add_cnt += 1
        return add_cnt

    def crawl_from_xici(self):
        print('...start crawl xici proxy...')
        add_cnt = 0
        for t in ["http://www.xicidaili.com/nn/%d", "http://www.xicidaili.com/nt/%d"]:
            for i in range(1, 10):
                url = t % i
                try:
                    r = requests.get(url, timeout=10, headers={"User-Agent": "Chrome"})
                except Exception:
                    continue
                sel = etree.HTML(r.content)
                for s in sel.xpath("//tr"):
                    try:
                        lst = s.xpath("td/text()")
                        ip, port = lst[0], lst[1]
                    except:
                        continue
                    ipstr = "%s:%s" % (ip, port)
                    print(ipstr)
                    if self.valid_proxy(ipstr):
                        self.add_proxy(ipstr)
                        add_cnt += 1
        return add_cnt

    def add_proxy(self, ipstr):
        """
        Args:
            - ipstr  eg: 127.0.0.1:88
        """
        rds = get_redis("default")
        add_cnt = rds.sadd(RK_PROXY_IP_ALL, ipstr)
        from tasks import check_add_proxy_ip
        if add_cnt:     # 新增的
            for c in self.consumer_list:
                # c.on_producer_add(ipstr)
                check_add_proxy_ip.delay(c.name, ipstr)
        return add_cnt

    def get_proxy(self):
        rds = get_redis("default")
        ipstr = rds.srandmember(RK_PROXY_IP_ALL)
        return ipstr

    def all_proxy(self):
        rds = get_redis("default")
        return rds.smembers(RK_PROXY_IP_ALL)

    def remove_proxy(self, ipstr):
        rds = get_redis("default")
        del_cnt = rds.srem(RK_PROXY_IP_ALL, ipstr)
        if del_cnt:
            for c in self.consumer_list:
                c.on_producer_remove(ipstr)
        return del_cnt

    def proxy_size(self):
        rds = get_redis("default")
        return rds.scard(RK_PROXY_IP_ALL)

    def valid_proxy(self, ipwithport):
        """
        PS: 能访问百度不一定可以访问其他网站,在具体使用时最好再验证一遍
        """
        try:
            r = requests.get("http://www.baidu.com",
                             proxies = {"http": "http://%s" % ipwithport},
                             timeout=1)
        except:
            return False
        if r.status_code != 200:
            return False
        if "百度一下" not in r.content:
            return False
        return True


class ProxyConsumer(object):

    def valid_proxy(self, ipstr):
        return True

    def on_producer_add(self, ipstr):
        if self.valid_proxy(ipstr):
            self.add_proxy(ipstr)

    def on_producer_remove(self, ipstr):
        self.remove_proxy(ipstr)

    def add_proxy(self, ipstr):
        rds = get_redis("default")
        add_cnt = rds.sadd(self.PROXY_KEY, ipstr)
        return add_cnt

    def remove_proxy(self, ipstr):
        rds = get_redis("default")
        del_cnt = rds.srem(self.PROXY_KEY, ipstr)
        return del_cnt

    def all_proxy(self):
        rds = get_redis("default")
        return rds.smembers(self.PROXY_KEY)

    def proxy_size(self):
        rds = get_redis("default")
        return rds.scard(self.PROXY_KEY)




class ScqcpProxyConsumer(ProxyConsumer):
    PROXY_KEY = RK_PROXY_IP_SCQCP
    name = "scqcp"

    def valid_proxy(self, ipstr):
        url = "http://scqcp.com/login/index.html"
        try:
            ua = random.choice(BROWSER_USER_AGENT)
            r = requests.get(url,
                             headers={"User-Agent": ua},
                             timeout=4,
                             proxies={"http": "http://%s" % ipstr})
            sel = etree.HTML(r.content)
            token = sel.xpath("//input[@id='csrfmiddlewaretoken1']/@value")[0]
            if token:
                return True
        except:
            return False
        return True


class TongChengProxyConsumer(ProxyConsumer):
    PROXY_KEY = RK_PROXY_IP_TC
    name = "tongcheng"

    def valid_proxy(self, ipstr):
        url = "http://www.ly.com/"
        try:
            ua = random.choice(BROWSER_USER_AGENT)
            r = requests.get(url,
                             headers={"User-Agent": ua},
                             timeout=2,
                             proxies={"http": "http://%s" % ipstr})
        except:
            return False
        if r.status_code != 200 or "同程旅游" not in r.content:
            return False
        return True


proxy_producer = ProxyProducer()

if "proxy_list" not in globals():
    proxy_list = {}

    proxy_list[ScqcpProxyConsumer.name] = ScqcpProxyConsumer()
    proxy_list[TongChengProxyConsumer.name] = TongChengProxyConsumer()

    for name, obj in proxy_list.items():
        proxy_producer.registe_consumer(obj)


def get_proxy(name):
    return proxy_list[name]

# coding: utf8

import requests
import lxml.html
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool
import time
import os


def strip(s):
    return s.strip() if s else ''


def save_ips(ips):
    with open("ip.txt", "a") as f:
        f.writelines(("%s\n" % i for i in ips if i))


def get_cn_proxy_list():
    print '=> get cn-proxy.com'
    r = requests.get("http://cn-proxy.com/")
    doc = lxml.html.fromstring(r.text)
    trs = doc.xpath("//table/tbody/tr")
    ips = []
    for tr in trs:
        items = tr.xpath("./td/text()")
        ip = "%s:%s" % (strip(items[0]), strip(items[1]))
        ips.append(ip)
    return ips


def get_kuaidaili_list():
    print '=> get kuaidaili.com/proxylist'
    # 取前10页
    ips = []
    for i in range(1, 11):
        url = "http://www.kuaidaili.com/proxylist/%s/" % i
        r = requests.get(url)
        doc = lxml.html.fromstring(r.text)
        trs = doc.xpath("//table/tbody/tr")
        for tr in trs:
            items = tr.xpath("./td/text()")
            ip = "%s:%s" % (strip(items[0]), strip(items[1]))
            ips.append(ip)
    return ips


def get_haodaili_guonei_list():
    print '=> get haodailiip.com/guonei'
    ips = []
    for i in range(1, 101):
        url = "http://www.haodailiip.com/guonei/%s" % i
        r = requests.get(url)
        doc = lxml.html.fromstring(r.text)
        trs = doc.xpath("//table[@class='proxy_table']/tr")
        for tr in trs[1:]:
            items = tr.xpath("./td/text()")
            ip = "%s:%s" % (strip(items[0]), strip(items[1]))
            ips.append(ip)
    return ips


def get_haodaili_guowai_list():
    print '=> get haodailiip.com/guoji'
    ips = []
    for i in range(1, 101):
        url = "http://www.haodailiip.com/guoji/%s" % i
        r = requests.get(url)
        doc = lxml.html.fromstring(r.text)
        trs = doc.xpath("//table[@class='proxy_table']/tr")
        for tr in trs[1:]:
            items = tr.xpath("./td/text()")
            ip = "%s:%s" % (strip(items[0]), strip(items[1]))
            ips.append(ip)
    return ips


def check_proxy(ip):
    proxies = {
        'http': ip.strip()
    }
    # print proxies
    try:
        r = requests.get("http://ip.chinaz.com/", proxies=proxies, timeout=5)
        if r:
            print 'Good! you proxy is', bs(r.content).find('span', attrs={'class': 'info3'}).strong.get_text()
            with open('good_ip.txt', 'a') as a:
                a.write(ip)
        else:
            print 'Error'
    except Exception:
        print 'Exception'

if __name__ == '__main__':
    # 保存代理ip
    st = time.time()
    # save_ips(get_cn_proxy_list())
    # save_ips(get_kuaidaili_list())
    save_ips(get_haodaili_guonei_list())
    # save_ips(get_haodaili_guowai_list())
    end = time.time()
    with open('ip.txt', 'r') as r:
        n = r.readlines()
    print '入库 => {0} 个ip, 花费 {1:.2f} mins'.format(len(n), (end - st) / 60)
    # 判断代理ip可用, 需要重新判读是否可用
    with open('good_ip.txt', 'r') as r:
        n1 = r.readlines()
    n.extend(n1)
    st = time.time()
    pool = Pool(12)
    pool.map_async(check_proxy, n).get()
    end = time.time()
    with open('ava_ip.txt', 'w') as w:
        with open('good_ip.txt', 'r') as r:
            content = r.readlines()
            content = list(set(content))
            w.writelines(content)
    print '可用ip => {0} 个, 花费 {1:.2f} mins'.format(len(n1), (end - st) / 60)

#!/usr/bin/env python
# encoding: utf-8

import scrapy
import json
import datetime
import urllib
import hashlib
from bs4 import BeautifulSoup as bs
import re
from manyue.items import ManyueItem
# from fabric.colors import green, red
# from cchardet import detect


from datetime import datetime as dte
from base import SpiderBase
from scrapy.conf import settings
from pymongo import MongoClient
# import ipdb


class Gzggzy(SpiderBase):
    name = "gzggzy"
    custom_settings = {
        "ITEM_PIPELINES": {
            'manyue.pipeline.MongoPipeline': 300,
        },
        "DOWNLOAD_DELAY": 0.15,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def start_requests(self):
        for x in xrange(1,520):
            url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/zfcglist.jsp?page=%s&siteId=1&channelId=456' %x
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        soup = bs(response.body, 'lxml')
        info = soup.find('table', attrs={'class': 'wsbs-table'}).find_all('tr')
        for x in info:
            try:
                url = 'http://www.gzggzy.cn' + x.find('a')['href']
                yield scrapy.Request(url, callback=self.parse_content, meta={'url': url})
            except:
                pass

    def get_md5(self, msg):
        md5 = hashlib.md5(msg.encode('utf-8')).hexdigest()
        return md5

    def parse_content(self, response):
        soup = bs(response.body, 'lxml')
        url = response.meta['url']
        info = soup.find('div', attrs={'class': 'xx-main'})
        title = soup.h1 or soup.find('div', attrs={'class':'xx-main'}).find_all('p')[3]
        # title = soup.find('a', attrs={'name': 'EBf6f2c0591e17488d8b417a1639eb78c3'}).text
        tmp = [re.compile(p + u'\d{4}年\d{1,2}月\d{1,2}日邀请之时起至\d{4}年\d{1,2}月\d{1,2}\日 \d{1,2}:\d{1,2}')
                   for p in [u'投标文件时间：', u'响应文件时间：']
                   ]
        regexes = [re.compile(p + u'\d{4}年\d{1,2}月\d{1,2}日公告之时起至\d{4}年\d{1,2}月\d{1,2}\日 \d{1,2}:\d{1,2}')
                   for p in [u'投标文件时间：', u'响应文件时间：']
                   ]
        regexes.extend(tmp)
        for regex in regexes:
            if regex.search(soup.text):
                pre_date = regex.findall(soup.text)[0]
                continue
        # if 'pre_date' not in globals.values():
        #     pre_date = ['','']
        try:
            pre_dates = re.findall(ur'\d{4}年\d{1,2}月\d{1,2}日',pre_date)
            zb_date = pre_dates[0]
            jz_date = pre_dates[1] + pre_date.split()[-1]
        except:
            zb_date = ''
            jz_date = ''
        # zb_date = soup.find('a', attrs={'name': 'EB243f613c0e4142348cb28322c82acac1'}) or soup.find('a', attrs={'name': 'EBd32d1b86baa04cbb97efa6d08efeb852'}) # 招标日期
        # jz_date = soup.find('a', attrs={'name': 'EB053b400bade94be288048635d81830c9'}) or soup.find('a', attrs={'name': 'EB6865143177f54b728c274a37854e92f5'}) # 截至日期
        # zbdl = # 招标代理机构
        try:
            zbgs = soup.find(text=re.compile(u'采购人名称：')).split(u'：')[1] # 项目招标公司名称
            zb_adress = soup.find(text=re.compile(u'地址：')).split(u'：')[1] # 投标地址
        except:
            zbgs = ''
            zb_adress = ''
        tel = soup.find(text=re.compile(u'联系电话：')).split(u'：')[-1]# 联系方式
        address = soup.find(text=re.compile(u'采购人地址：')).split(u'：')[1] # 地址
        name = soup.find(text=re.compile(u'联 系 人：')).split(u'：')[1].split()[0] # 联系人名称
        update_date = re.findall(ur'\d{4}年\d{1,2}月\d{1,2}日',soup.text)[-1]
        line_id = self.get_md5(url + update_date)
        content = info.text
        # print zb_date, jz_date, zbgs, zb_adress, tel, address, name
        attrs = dict(
            zb_date=zb_date,
            jz_date=jz_date,
            zbgs=zbgs,
            zb_adress=zb_adress,
            tel=tel,
            address=address,
            name=name,
            content=content,
            title=title.text,
            update_date=update_date,
            line_id=line_id,
            url=url,
        )
        yield ManyueItem(**attrs)

        # attrs = dict(
        #     s_province='河南',
        #     s_city_id="",
        #     s_city_name=s_city_name,
        #     s_sta_name=s_sta_name,
        #     s_city_code=get_pinyin_first_litter(s_city_name),
        #     s_sta_id='',
        #     d_city_name=d_city_name,
        #     d_city_id="",
        #     d_city_code=get_pinyin_first_litter(d_city_name),
        #     d_sta_id="",
        #     d_sta_name=d_city_name,
        #     drv_date=drv_date,
        #     drv_time=drv_time,
        #     drv_datetime=dte.strptime("%s %s" % (
        #         drv_date, drv_time), "%Y-%m-%d %H:%M"),
        #     distance=unicode(distance),
        #     vehicle_type=vehicle_type,
        #     seat_type="",
        #     bus_num=bus_num,
        #     full_price=float(full_price),
        #     half_price=float(full_price) / 2,
        #     fee=0.0,
        #     crawl_datetime=dte.now(),
        #     extra_info=extra,
        #     left_tickets=left_tickets,
        #     crawl_source="hn96520",
        #     shift_id="",
        # )


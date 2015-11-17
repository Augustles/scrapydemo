# encoding=utf-8

import scrapy
from douban.items import DoubanItem
from scrapy.http import Request
from bs4 import BeautifulSoup as bs  # 加载beautiful

# pip install beautifulsoup4
# import os

# scrapy crawl douban -o douban.json -t json 下载为douban.json
# scrapy crawl douban -o douban.csv csv格式
# scrapy genspider -t basic boboSpider 'douban.com' 生成一个basicspider
# 1. 调试 scrapy shell
# 2. scrapy parse --spider=MySpider -d 3 http://music.douban.com/chart
# 3. from scrapy.shell import inspect_response inspect_response(response)
# pip install pybloomfiltermmap 去重


class doubanSpider(scrapy.spiders.Spider):
    name = 'douban'  # 定义spider名字
    allowed_domains = ['douban.com', ]  # 允许爬取域名列表(可选)
    start_urls = []  # 开始爬取的列表
    download_delay = 1  # 爬取速度为1s,防止ban
    for y in xrange(0, 240, 25):
        start_urls.append(
            'http://www.douban.com/doulist/38849533/?start={0}&sort=seq&sub_type='.format(y))

    def parse(self, response):  # 解析返回的URL数据
        # 下载直接整理的图片
        # with open(pre+'/pic_links.txt','r') as f:
        #     for line in f:
        #         item = DoubanItem()
        #         item['image_urls'] = [line.strip()]
        #         item['images'] = line[line.rfind('/')+1:].strip()
        #         yield item

        # inspect_response(response, self) # 进入shell调试
        import chardet
        # 用beautifulsoup解析, 自动识别编码
        soup = bs(response.body, from_encoding=chardet.detect(
            response.body).get('encoding'))
        # print chardet.detect(response.body).get('encoding')
        # print soup
        import time
        for y in soup.find_all('div', attrs={'class': 'doulist-item'}):
            item = DoubanItem()
            item['title'] = y.find('div', attrs={'class': 'title'}).a.text
            item['link'] = y.find('div', attrs={'class': 'title'}).a['href']
            item['rating'] = y.find(
                'span', attrs={'class': 'rating_nums'}).text
            item['major'] = y.find('div', attrs={'class': 'abstract'}).text
            item['entry_time'] = time.strftime('%Y-%m-%d')
            # yield item # 生成器返回item传递到pipelines
            # 测试meta传递参数
            # Request(dont_filter=False) 未被复写(overridden)
            yield Request(url=item['link'], meta={'item': item}, callback=self.parse_item)

    def parse_item(self, response):  # parse_details
        item = response.meta['item']
        # print item['title']
        soup = bs(response.body)
        # print soup.title.text
        a = soup.find('img', attrs={'rel': 'v:image'})
        a = a['src'] + '#' + item['title'].strip()
        if 'thumb' in a:
            a = a.replace('thumb', 'photo')
        item['image_urls'] = [a]
        item['Url'] = response.url
        yield item

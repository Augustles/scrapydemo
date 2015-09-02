# encoding=utf-8

import scrapy
from douban.items import DoubanItem
from bs4 import BeautifulSoup  # 加载beautiful
# pip install beautifulsoup4
# import os
# scrapy crawl douban -o douban.json -t json 下载为douban.json 
# scrapy crawl douban -o douban.csv csv格式

class doubanSpider(scrapy.spiders.Spider):
    name = 'douban'  # 定义spider名字
    allowed_domains = ['douban.com', ]  # 允许爬取域名列表(可选)
    start_urls = []  # 开始爬取的列表
    for y in xrange(0, 240, 25):
        start_urls.append(
            'http://www.douban.com/doulist/38849533/?start={0}&sort=seq&sub_type='.format(y))
    # global pre
    # pre = os.getcwd()
    # with open(pre+'/pic_links.txt','r') as f:
    #     for line in f:
    #         print line
    #         start_urls.append(line.strip())

    def parse(self, response):  # 解析返回的URL数据
        # 下载直接整理的图片
        # with open(pre+'/pic_links.txt','r') as f:
        #     for line in f:
        #         item = DoubanItem()
        #         item['image_urls'] = [line.strip()]
        #         item['images'] = line[line.rfind('/')+1:].strip()
        #         yield item

        soup = BeautifulSoup(response.body)  # 用beautifulsoup解析
        print soup
        for y in soup.find_all('div', attrs={'class': 'doulist-item'}):
            item = DoubanItem()
            item['title'] = y.find('div', attrs={'class': 'title'}).a.text
            item['link'] = y.find('div', attrs={'class': 'title'}).a['href']
            item['rating'] = y.find(
                'span', attrs={'class': 'rating_nums'}).text
            item['major'] = y.find('div', attrs={'class': 'abstract'}).text
            yield item  # 生成器返回匹配到的项目

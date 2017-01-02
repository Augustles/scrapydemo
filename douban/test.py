# coding=utf-8

import requests

headers = {
    'User-Agent': 'Baiduspider',
}
cookie = {
    'bid': 'ZOYCQXKBBRGKEUNWHBFE',
}
url = 'https://movie.douban.com/review/best/?start=40'
r = requests.get(url, headers=headers, cookies=cookie)
print r.status_code, r.content
# from proxy import get_proxy, get_redis

# t = get_proxy('douban')
# info = get_redis('default')
# info = info.smembers('proxy:all')
# for x in info:
    # print t.valid_proxy(x)



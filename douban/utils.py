# coding=utf-8

import hashlib
import re

from random import randint

BID_LEN = 20
BID_LIST_LEN = 500

def gen_bids():
    bids = []
    for i in range(BID_LIST_LEN):
        bid = []
        for x in range(BID_LEN):
            bid.append(chr(randint(65, 90)))
        bids.append("".join(bid))
    return bids

def md5(msg):
    md5 = hashlib.md5(msg.encode('utf-8')).hexdigest()
    return md5

def is_url(char):
    if re.match(r'^(?:http)s?://[^\s]*', char):
        return True
    return False

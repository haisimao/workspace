# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import requests
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse

from settings import USER_AGENT_LIST


class RandUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers.setdefault(b'User-Agent', user_agent)


import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


# class RandIPROXY(object):
#     def process_request(self, request, spider):
#         request.meta["proxy"] = proxyServer
#
#         request.headers["Proxy-Authorization"] = proxyAuth


class RandIPROXY(object):

    def process_request(self, request, spider):
        proxy = requests.get(url="http://api.http.niumoip.com/v1/http/ip/get?p_id=192&s_id=1&u=VjVXNQ4!AGIBOwEvCUcBPg8gVmoCOgEQBFNXU1NV&number=1&port=1&type=2&map=1&pro=0&city=0&pb=1&mr=3&cs=1").text
        # for proxy in PROXY:
        request.meta['PROXY'] = 'http://{}'.format(proxy)

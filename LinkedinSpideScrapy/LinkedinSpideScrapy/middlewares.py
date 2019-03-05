# -*- coding: utf-8 -*-

from scrapy import signals

import datetime
import random
import time

import requests
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
from fake_useragent import UserAgent

ua = UserAgent()


class RandUserAgent(UserAgentMiddleware):

    # def process_request(self, request, spider):
    #     request.headers.setdefault(b'User-Agent', ua.chrome)
    def __init__(self, crawler):
        super(RandUserAgent, self).__init__()
        self.ua = UserAgent()
        # 从配置文件settings中读取RANDOM_UA_TYPE值，默认为random，可以在settings中自定义
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):  # 必须和内置的一致，这里必须这样写
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())


import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class RandIPROXY(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
        # 添加鉴权验证
        import json
        csrf_token = json.loads(spider.conn.random()).get('JSESSIONID')
        request.headers['csrf-token'] = csrf_token


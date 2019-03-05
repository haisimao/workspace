# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import redis
import random
import logging
import base64
import requests
import time
from .useragent import agents
from .cookies import CookieTool
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware


# 代理服务
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"


# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers['User_Agent'] = agent


class CookiesMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        # xiaoman
        self.rconn = redis.from_url(settings['REDIS_URL'], db=1, decode_responses=True)
        # weixin
        # self.rconn = redis.from_url(settings['REDIS_URL'], db=4, decode_responses=True)
        self.cookie_tool = CookieTool()
        self.cookie_tool.init_cookie(self.rconn, crawler.spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        redis_keys = self.rconn.keys()
        while len(redis_keys) > 0:
            key = random.choice(redis_keys)
            if "xiaoman:Cookies" in key:
            # if 'weixin:Cookies' in key:
                cookie = json.loads(self.rconn.get(key))
                request.cookies = cookie
                account_text = key.split(":Cookies:")[-1]
                request.meta["user"] = account_text.split("--")[0]
                request.meta["password"] = account_text.split("--")[1]
                break

    def process_response(self, request, response, spider):
        if json.loads(response.text)["code"] == -10005 or json.loads(response.text)["code"] == -10002:
            time.sleep(10)
            logging.warning(json.loads(response.text)["code"])
            logging.warning("身份信息已过期！")
            self.cookie_tool.update_cookie(self.rconn, spider.name, request.meta["user"], request.meta["password"])
            return request
        return response


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


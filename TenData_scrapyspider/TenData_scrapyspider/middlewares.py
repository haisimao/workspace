# -*- coding: utf-8 -*-
import json

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent

from db import RedisClient

ua = UserAgent()


class RandUserAgent(UserAgentMiddleware):

    def __init__(self, crawler):
        super(RandUserAgent, self).__init__()
        self.ua = UserAgent()
        # 从配置文件settings中读取RANDOM_UA_TYPE值，默认为random，可以在settings中自定义
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")
        self.conn = RedisClient('cookies', 'tendata')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):  # 必须和内置的一致，这里必须这样写
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())
        # 添加cookies
        locations = {'north_america-imports': '2016-01-01@2018-01-02'}
        cookies = json.loads(self.conn.random())
        cookies['north_america-imports'] = locations.get('north_america-imports')
        request.cookies = cookies


import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class RandIPROXY(object):
    def __init__(self):
        self.csrf_token_db = RedisClient('Csrf', 'Token')

    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
        # 添加cookies
        csrf_token = self.csrf_token_db.db.get('csrftoken')
        request.headers['X-CSRF-TOKEN'] = csrf_token




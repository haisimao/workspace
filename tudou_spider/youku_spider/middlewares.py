import datetime
import random
import time

import requests
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse

from youku_spider.settings import USER_AGENT_LIST


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


class RandIPROXY(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth


class SeleniumMiddleware(object):
    '''
    执行selenium下载
    '''
    def process_request(self, request, spider):
        '''
        下载网页, 只要返回HTTPResponse就不再执行其他下载中间件
        :param request: scrapy整合的全局参数
        :param spider: spiders里的爬虫对象
        :return:
        '''
        if spider.name == 'tudou':
            spider.browser.get(request.url)
            time.sleep(2)
            print('访问: {}'.format(request.url))
            return HtmlResponse(url=request.url,
                                body=spider.browser.page_source,
                                encoding='utf-8',
                                request=request)

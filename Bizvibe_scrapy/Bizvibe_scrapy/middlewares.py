# -*- coding: utf-8 -*-
import json
import random
import time

import requests

from Bizvibe_scrapy.settings import COOKIES_DICT
from Bizvibe_scrapy.useragent import agent_list
from scrapy.http import HtmlResponse
from scrapy.dupefilter import RFPDupeFilter
import scrapy.crawler



import base64

# 代理服务器
from Bizvibe_scrapy.utils_ import BizvibeException

proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class RandIPROXY(object):

    def process_request(self, request, spider):
        # request.meta["proxy"] = proxyServer
        # request.headers["Proxy-Authorization"] = proxyAuth
        # request.headers['User_Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        request.cookies = COOKIES_DICT
        agent = random.choice(agent_list)
        request.headers['User_Agent'] = agent


class DLMiddleware(object):
    '''
    执行自定义下载
    '''
    def process_request(self, request, spider):
        '''
        下载网页, 只要返回HTTPResponse就不再执行其他下载中间件
        :param request: scrapy整合的全局参数
        :param spider: spiders里的爬虫对象
        :return:
        '''
        if spider.name == 'bizvibe':
            agent = random.choice(agent_list)
            request.headers['User_Agent'] = agent
            data = request.meta.get('data')
            header = {'Host': 'www.bizvibe.com', 'User-Agent': agent, }
            resp = requests.post(spider.origin_url, data=data, headers=header, cookies=COOKIES_DICT, allow_redirects=False)
            return HtmlResponse(url=spider.origin_url,
                                        body=resp.text,
                                        encoding='utf-8',
                                        request=request)

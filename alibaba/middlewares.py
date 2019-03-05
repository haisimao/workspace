# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
import datetime

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from settings import COOKIES_DICT
from utils import create_proxy_auth_extension


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
        if spider.name == 'alibaba':
            last_time = datetime.datetime.now() + datetime.timedelta(hours=-2)
            if last_time > spider.COOKIES_SWITCH_TIME:
                spider.COOKIES_SWITCH_TIME = datetime.datetime.now()
                # 重置cookies
                spider.browser.delete_all_cookies()
                for i in COOKIES_DICT:
                    spider.browser.add_cookie(i)
                time.sleep(2)
                spider.browser.refresh()
            spider.browser.get(request.url)
            # 测试一下直接打开需登录的网页
            # 一定的时间后, 修改写死的cookies
            time.sleep(7)
            print('访问: {}'.format(request.url))
            return HtmlResponse(url=request.url,
                                body=spider.browser.page_source,
                                encoding='utf-8',
                                request=request)
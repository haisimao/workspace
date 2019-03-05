# -*- coding: utf-8 -*-
import json
import time

from scrapy.http import HtmlResponse

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Bizvibe_scrapy.settings import COOKIES_DICT, SEARCH_PAGE
from Bizvibe_scrapy.useragent import agents
from Bizvibe_scrapy.utils_ import BizvibeException


import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"

# proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


# class RandIPROXY(object):
#     def process_request(self, request, spider):
#         # request.meta["proxy"] = proxyServer
#         # request.headers["Proxy-Authorization"] = proxyAuth
#         # request.headers['User_Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
#         request.cookies = cookies


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
            if request.meta.get('spider_url') == 'detail':
                # 新打开一个标签页, 访问新网址, 跳到当前页, 获取数据, 关闭当前页面, 回到当前页
                try:
                    js = 'window.open("{}");'.format(request.url)
                    spider.browser.execute_script(js)
                    # 这是一个try语句
                    handles = spider.browser.window_handles

                    if len(handles) > 4:
                        spider.CloseExceptionSpider()
                        print('当前爬取页数', request.meta.get('page'))
                        raise BizvibeException('网络错误, 请重启')
                    for handle in handles:  # 切换窗口
                        if handle != spider.browser.current_window_handle:
                            spider.browser.switch_to_window(handle)
                            break
                    time.sleep(5)
                    # 设置隐式等待
                    # element = WebDriverWait(spider.browser, 10, 0.5).util(
                    #     EC.presence_of_element_located((By.ID, 'cp-category-list'))
                    # )
                    DW_page = spider.browser.page_source
                    DW_url = spider.browser.current_url
                    # spider.browser.close()  # 关闭当前窗口
                    spider.browser.execute_script("window.opener=null;window.open('','_self');window.close();")  # 关闭当前窗口
                    time.sleep(2)
                    spider.browser.switch_to_window(handles[0])  # 切换回查询窗口
                    # 删除查询窗口以外的窗口
                    if len(handles) > 4:
                        for handle in handles:  # 切换窗口
                            if handle != handles[0]:
                                spider.browser.switch_to_window(handle)
                                spider.browser.close()  # 关闭当前窗口
                    return HtmlResponse(url=DW_url,
                                    body=DW_page,
                                    encoding='utf-8',
                                    request=request)
                except:
                    spider.browser.execute_script("window.opener=null;window.open('','_self');window.close();")  # 关闭当前窗口
                    spider.browser.switch_to_window(handles[0])
                    self.process_request(request, spider)
                    if len(handles) > 4:
                        spider.CloseExceptionSpider()
                        print('当前爬取页数', request.meta.get('page'))
                        raise BizvibeException('网络错误, 请重启')
                    print('响应超时')
            else:
                page = request.meta.get('page')
                page_down = 'Page' + str(int(page)) + '-li-' + str(1)
                # 先将进度条滚到页底 再点击下一页, 拿到返回的页面
                time.sleep(3)
                spider.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                try:
                    next_page = spider.browser.find_element_by_xpath('//*[@id="results-area"]/div/span')
                    if next_page:
                        while True:
                            # 拿到下一页
                            next_page.click()
                            if spider.browser.find_element_by_id(page_down):
                                break
                            else:
                                continue
                except:
                    print('下载响应超时')
                    time.sleep(30)
                    # 设置对应的页面已加载记录,,在达到对应的页面之前不进行数据库写入
                    spider.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    self.process_request(request, spider)
                with open('D:\workspace\Bizvibe_Selenium_scrapy\Bizvibe_scrapy\page.json', 'r+') as f:
                    data = json.load(f)
                    search_page = data.get('page')
                if int(search_page) > (int(page) + 1):
                    page_source = '已下载页面'
                    return HtmlResponse(url=spider.browser.current_url,
                                        body=page_source,
                                        encoding='utf-8',
                                        request=request)
                else:
                    return HtmlResponse(url=spider.browser.current_url,
                                        body=spider.browser.page_source,
                                        encoding='utf-8',
                                        request=request)

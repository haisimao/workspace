import json
import re
import random
from scrapy import Spider, Request
from XiaomanCustoms.items import ForumItem


class WenXinSpider(Spider):
    name = 'weixin'
    start_url = 'https://mp.weixin.qq.com/'

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        token = re.findall(r'token=(\d+)', str(response.url))[0]
        varietys = ['和旺跨境电商', '跨境电商赢商荟', '跨境电商鹰熊汇', '万猫外贸之家', '外土司', '老杨聊跨境电商']
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        for variety in varietys:
            params = {
                'action': 'search_biz',
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'query': {}.format(variety),
                'begin': '0',
                'count': '5',
            }
            yield Request(url=search_url, body=params, callback=self.parse_search, meta={'token': token})

    def parse_search(self, response):
        token = response.meta['token']
        data = json.loads(response.text)
        fakeid = data['list'][0]['fakeid']
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        page = 0
        params = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': {}.format(sta(page)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9',
        }
        yield Request(url=appmsg_url, body=params, callback=self.parse_appmsg, meta={'token': token, 'page': page})

    def parse_appmsg(self, response):
        data = json.loads(response.text)
        app_msg_list = data['app_msg_list']
        for app_msg in app_msg_list:
            page_url = app_msg['link']
            yield Request(url=page_url, callback=self.parse_item)
        app_msg_cnt = data['app_msg_cnt']
        token = response.meta['token']
        page = response.meta['page']
        pages = int(int(app_msg_cnt) / 5)
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        if page <= pages:
            params = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': {}.format(sta(page + 1)),
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9',
            }
            yield Request(url=appmsg_url, body=params, callback=self.parse_appmsg, meta={'token': token, 'page': page})

    def parse_item(self, response):
        item = ForumItem()
        item['title'] = response.xpath['//*[@id="activity-name"]/text()'].extract()[0]
        item['url'] = response.url
        data= response.xpath['//*[@id="img-content"]//text()'].extract()
        text = ''
        for align in data:
            text += align
        item['text'] = text
        item['sound_code'] = response.xpath['//*[@id="img-content"]'].extract()[0]
        yield item

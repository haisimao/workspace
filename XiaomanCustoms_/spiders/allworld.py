import json
import re
import time
import os
import requests
from scrapy import Spider, Request
from XiaomanCustoms.items import InformationItem


class AllWorldSpider(Spider):
    name = 'allworld'
    start_url = 'https://bbs.fob5.com/forum-84-{}.html'

    def start_requests(self):
        os.mkdir("D:\环球贸易论坛_forum")
        for page in range(1, 140):
            url = self.start_url.format(str(page))
            yield Request(url, callback=self.parse_url, dont_filter=True)
        # urls = [self.start_url.format(str(page)) for page in range(1, 140)]
        # for url in urls:
        #     yield Request(url, callback=self.parse_url)
        # yield from [Request(url, callback=self.parse) for url in urls]

    def parse_url(self, response):
        urls = response.xpath('//*[contains(@id, normalthread_)]/tr/th/a[3]/@href').re('https://bbs.fob5.com/thread-\d+-1-\d+.html')
        for url in urls:
            yield Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        item = InformationItem()
        item['title'] = response.xpath('//*[@id="thread_subject"]/text()').extract()[0]
        item['category'] = 'B2B'
        thumbnail = response.xpath('//*[@class="t_f"][1]/img/@src').extract()
        if thumbnail != [] and re.search(r'https://', thumbnail[0]) is not None:
            image_url = thumbnail[0]
            os.chdir("D:\环球贸易论坛_forum")
            img = requests.get(image_url)
            f = open(item['title'] + '.jpg', 'ab')
            f.write(img.content)
            f.close()
            item['cover_picture_url'] = thumbnail[0]
            item['thumbnail'] = '环球外贸论坛_forum/'+ item['title']
        else:
            item['thumbnail'] = ''
        item['url'] = response.url
        item['views'] = int(response.xpath('//*[@class="hm ptn"]/span[2]/text()').extract()[0])
        item['createdAt'] = response.xpath('//*[@class="authi"]/em/text()').extract()[0][4:]
        item['updatedAt'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        yield item

import json
import re
import os
import requests
import time
from scrapy import Spider, Request
from XiaomanCustoms.items import InformationItem


class YuGuoSpider(Spider):
    name = 'yuguo'
    start_url = 'http://www.cifnews.com/article/{}'

    def start_requests(self):
        # page = 37934
        # url = self.start_url.format(str(page))
        os.mkdir("D:\雨果网_forum")
        urls = [self.start_url.format(str(i)) for i in range(1, 37772)]
        yield from [Request(url, callback=self.parse_item, dont_filter=True) for url in urls]
        # yield Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        item = InformationItem()
        item['title'] = response.xpath('//*[@id="title"]/text()').extract()[0]
        if re.search(r'亚马逊', item['title']) is not None or re.search(r'eBay', item['title']) is not None:
            item['category'] = 'B2C'
        else:
            item['category'] = 'B2B'
        thumbnail = response.xpath('//*[@class="article-inner"]/p/img/@src').extract()
        if thumbnail != [] and re.search(r'http://', thumbnail[0]) is not None:
            image_url = thumbnail[0]
            os.chdir("D:\雨果网_forum")
            img = requests.get(image_url)
            f = open(item['title'] + '.jpg', 'ab')
            f.write(img.content)
            f.close()
            item['cover_picture_url'] = thumbnail[0]
            item['thumbnail'] = '雨果网_forum/' + item['title']
        else:
            item['thumbnail'] = ''
        item['url'] = response.url
        item['views'] = response.xpath('//*[@class="like-a"]/p/text()').extract()[0]
        item['createdAt'] = response.xpath('//*[@class="time fr"]/text()').extract()[0]
        item['updatedAt'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        yield item

import re

import bs4
import requests
from bs4 import BeautifulSoup
from readability import Document
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
from goose3 import Goose
from goose3.text import StopWordsChinese
from goose3.configuration import Configuration

# from items import AlibabaForumItem
# from settings import HEADER
# from utils import AliBaBaException
from items import AlibabaForumItem
from settings import HEADER
from utils import AliBaBaException


class AliBaBaSpider(CrawlSpider):
    name = 'alibaba'
    s_url = 'https://waimaoquan.alibaba.com/bbs/thread-htm-fid-309-{}.html&tab=digest'

    def start_requests(self):
        '''
        第一个请求
        :return:
        '''
        yield Request(self.s_url.format(1), callback=self.parse_index, meta={'page': 1})

    def parse_index(self, response):
        res = Selector(response)
        # try:
        a_html = res.xpath('//*[@id="J_posts_list"]/tr/td[2]/p[1]/a[3]')
        for a_ in a_html:
                # try:
            a_url = a_.xpath('./ @href').extract()[0]

            yield Request(a_url, callback=self.parse_article, meta={'page': response.meta.get('page'), })
                # except:
                #     continue
        # except:
        #     return
        # finally:
        #
        #     yield Request(self.news_url, callback=self.parse_index, meta={'news': 'start'}, dont_filter=True)
        page = response.meta.get('page')
        if page == 66:
            raise AliBaBaException('所有信息已爬取完毕')
        yield Request(self.s_url.format(page+1), callback=self.parse_index, meta={'page': page+1, 'article': True})

    def parse_article(self, response):
        items = AlibabaForumItem()
        soup = BeautifulSoup(response.text, 'lxml')
        res = Selector(response)
        paragraphs = soup.find_all('div', class_='editor_content')
        if paragraphs == []:
            return
        article = ''
        for i in paragraphs[0].contents:
            if isinstance(i, bs4.element.Tag):
                article += re.sub(r'\r', '', i.text)
        # 文章标题
        title = soup.find_all(id="J_post_title")[0].text
        title = re.sub(r'\[[\u4e00-\u9fa5a-zA-Z]*\]', '', title)
        title = re.sub(r'【[a-zA-Z0-9\u4e00-\u9fa5]*】', '', title)
        title = re.sub(r'[\]\[]', '', title)
        title = re.sub(r'[】【]', '', title)

        items['title'] = title

        # 文章链接
        items['url'] = response.url
        try:
            # 图片链接
            main_part = soup.find_all(id='J_read_main')[0]
            cover_picture_url = main_part.find_all('img', class_='J_post_img')[0].get('src')
            # 图片
            items['thumbnail'] = cover_picture_url
            # picture = requests.get(cover_picture_url, headers=HEADER)
            # with open(r'D:/workspace/alibaba_forum/alibaba_forum/' + title + '.jpg', 'wb') as j:
            #     j.write(picture.content)
            # items['thumbnail'] = r'alibaba_forum/' + title + '.jpg'
        except:
            items['thumbnail'] = ''

        # 点击次数
        items['views'] = res.xpath('//*[@id="read_0"]/table/tr[1]/td[2]/div[2]/div/span[1]/em/text()').extract()[0]

        # 发布时间
        rea_time = res.xpath('//*[@id="read_0"]/table/tr[1]/td[2]/div[4]/span/text()').extract()[0]
        rea_time = re.sub('发布于：', '', rea_time)
        items['createdAt'] = re.sub('\t', '', rea_time)
        yield items

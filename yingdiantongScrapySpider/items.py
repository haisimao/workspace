# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    name = 'company'
    comp_name = scrapy.Field()
    id = scrapy.Field()
    home_page = scrapy.Field()
    comp_tel = scrapy.Field()
    comp_addr = scrapy.Field()
    comp_type = scrapy.Field()
    comp_sales = scrapy.Field()
    employees_num = scrapy.Field()
    country = scrapy.Field()
    sic_code = scrapy.Field()


class LinkManItem(scrapy.Item):
    name = 'linkman'
    cont_first_name = scrapy.Field()
    cont_last_name = scrapy.Field()
    cont_email = scrapy.Field()
    cont_url = scrapy.Field()
    id = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinspidescrapyItem(scrapy.Item):
    name = 'linkedin'
    employees_num = scrapy.Field()
    year_found = scrapy.Field()
    home_page = scrapy.Field()
    comp_type = scrapy.Field()
    comp_intro = scrapy.Field()
    comp_addr = scrapy.Field()
    company_name = scrapy.Field()

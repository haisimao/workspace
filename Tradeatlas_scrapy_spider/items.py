# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TradeatlasScrapySpiderItem(scrapy.Item):
    hashid = scrapy.Field()
    port_time = scrapy.Field()
    origin_country = scrapy.Field()
    prod_desc = scrapy.Field()
    trans_price = scrapy.Field()
    HS_Code = scrapy.Field()
    exporter = scrapy.Field()
    import_country = scrapy.Field()
    importer = scrapy.Field()
    import_email = scrapy.Field()
    import_fax = scrapy.Field()
    import_tel = scrapy.Field()
    import_mail = scrapy.Field()
    import_addr = scrapy.Field()


class CompsItems(scrapy.Item):
    hashid = scrapy.Field()
    comp_name = scrapy.Field()
    home_page = scrapy.Field()
    comp_addr = scrapy.Field()
    country = scrapy.Field()
    comp_tel = scrapy.Field()
    emails = scrapy.Field()
    source = scrapy.Field()




























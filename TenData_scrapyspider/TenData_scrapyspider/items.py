# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Customs_InfoItem(scrapy.Item):
    # customs_info 海关数据表（51项）
    hashid = scrapy.Field()
    port_time = scrapy.Field()
    import_country = scrapy.Field()
    importer = scrapy.Field()
    import_depart = scrapy.Field()
    import_economy = scrapy.Field()
    import_cont = scrapy.Field()
    import_contactinfo = scrapy.Field()
    import_email = scrapy.Field()
    import_fax = scrapy.Field()
    import_tel = scrapy.Field()
    import_mail = scrapy.Field()
    import_addr = scrapy.Field()
    export_country = scrapy.Field()
    exporter = scrapy.Field()
    export_contactinfo = scrapy.Field()
    export_city = scrapy.Field()
    export_addr = scrapy.Field()
    HS_Code = scrapy.Field()
    prim_HScode = scrapy.Field()
    brand = scrapy.Field()
    prod_desc = scrapy.Field()
    trans_price = scrapy.Field()
    trans_unitprice = scrapy.Field()
    offshore_price = scrapy.Field()
    offshore_unitprice = scrapy.Field()
    payment_amount = scrapy.Field()
    invoice_sum = scrapy.Field()
    freight_fee = scrapy.Field()
    insurance_fee = scrapy.Field()
    tax_rate = scrapy.Field()
    customs_clearance = scrapy.Field()
    gross_weight = scrapy.Field()
    gross_amount = scrapy.Field()
    net_weight = scrapy.Field()
    net_amount = scrapy.Field()
    prod_num = scrapy.Field()
    num_unit = scrapy.Field()
    pack_num = scrapy.Field()
    pack_method = scrapy.Field()
    cargo_agent = scrapy.Field()
    ship_type = scrapy.Field()
    ship_comp = scrapy.Field()
    transp_country = scrapy.Field()
    source_port = scrapy.Field()
    destination_port = scrapy.Field()
    transit_port = scrapy.Field()
    origin_country = scrapy.Field()
    customs_name = scrapy.Field()
    customs_agent = scrapy.Field()
    remarks = scrapy.Field()







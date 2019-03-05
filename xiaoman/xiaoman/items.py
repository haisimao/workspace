# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompItem(scrapy.Item):
    # define the fields for your item here like:
    name = 'comps'

    # comp 公司信息表（13项）
    # comp_no = scrapy.Field()      自动生成，为NULL
    comp_name = scrapy.Field()
    main_industry = scrapy.Field()
    home_page = scrapy.Field()
    comp_tel = scrapy.Field()
    comp_addr = scrapy.Field()
    comp_intro = scrapy.Field()
    comp_type = scrapy.Field()
    year_found = scrapy.Field()
    comp_sales = scrapy.Field()
    employees_num = scrapy.Field()
    comp_assets = scrapy.Field()
    trade_style = scrapy.Field()
    hashid = scrapy.Field()
    createdAt = scrapy.Field()
    updatedAt = scrapy.Field()
    # company_name = scrapy.Field()


class ContItem(scrapy.Item):
    # cont 联系人信息表（6项）
    name = 'conts'
    # comp_no = scrapy.Field()      同公司信息表
    hashid = scrapy.Field()
    cont_name = scrapy.Field()
    cont_post = scrapy.Field()
    cont_email = scrapy.Field()
    cone_url = scrapy.Field()
    createdAt = scrapy.Field()
    updatedAt = scrapy.Field()


class CustomsItem(scrapy.Item):
    # customs 海关信息表（8项）
    #customs_num = scrapy.Field()
    # comp_no = scrapy.Field()      同公司信息表
    hashid = scrapy.Field()
    port_time = scrapy.Field()
    all_buyers = scrapy.Field()
    HS_Code = scrapy.Field()
    prod_desc = scrapy.Field()
    value_sum = scrapy.Field()


class Customs_InfoItem(scrapy.Item):
    # customs_info 海关数据表（51项）
    customs_hashid = scrapy.Field()
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






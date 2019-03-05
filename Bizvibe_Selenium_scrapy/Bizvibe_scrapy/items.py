import scrapy


class CompItem(scrapy.Item):
    # define the fields for your item here like:
    name = 'comps'

    comp_name = scrapy.Field()
    main_industry = scrapy.Field()
    home_page = scrapy.Field()
    comp_tel = scrapy.Field()
    comp_addr = scrapy.Field()
    comp_type = scrapy.Field()
    year_found = scrapy.Field()
    comp_sales = scrapy.Field()
    employees_num = scrapy.Field()
    source_ = scrapy.Field()
    country = scrapy.Field()
    hashid = scrapy.Field()
    createdAt = scrapy.Field()
    updatedAt = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    linkedin = scrapy.Field()
    contact_email = scrapy.Field()
    sic_code = scrapy.Field()
    comp_intro = scrapy.Field()


class CompDescItem(scrapy.Item):
    name = 'company_desc'

    comp_intro = scrapy.Field()
    hashid = scrapy.Field()



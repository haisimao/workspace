import json
import os
import requests
import logging
from scrapy import Spider, Request
from XiaomanCustoms.items import CompItem, ContItem, CustomsItem, Customs_InfoItem, ProfitItem, CashItem, Decash_AllItem, DecashItem, Decash_EqItem, ImageItem
from scrapy import FormRequest


class XiaomanSpider(Spider):
    name = 'xiaoman'
    # start_url = 'https://x.xiaoman.cn/api/company-read/mining-list?page={}&page_size=25&countryCode=76&sicCode={}'
    start_url = 'https://x.xiaoman.cn/api/company-read/mining-list?page={}&page_size=25&sicCode={}'

    def start_requests(self):
        sic_code = [56000000,56100000,56110000,56119900,56119901,56119902,56119903,56119904,56119905,56119906,56119907,56200000,56210000,56210100,56210101,56210102,56210103,56210104,56219900,56219901,56219902,56219903,56300000,56320000,56320100,56320101,56320102,56320200,56320201,56320202,56320203,56320204,56329900,56329901,56329902,56329903,56329904,56329905,56329906,56400000,56410000,56419900,56419901,56419902,56500000,56510000,56519900,56519901,56519902,56600000,56610000,56610100,56610101,56610102,56619900,56619901,56619902,56619903,56619904,56619905,56619906,56900000,56990000,56990100,56990101,56990102,56990103,56990200,56990201,56990202,56990300,56990301,56990302,56990303,56990304,56990400,56990401,56990402,56990403,56990404,56990405,56990406,56990407,56999900,56999901,56999902,56999903,56999904,56999905,56999906,56999907,56999908,56999909]
        for sicCode in sic_code:
            parameter = {
                'countryCode': '76',
                'sicCode': str(sicCode)
            }
            urls = [self.start_url.format(str(page), parameter['sicCode']) for page in range(1, 401)]
            yield from [Request(url, callback=self.parse) for url in urls]
            # url = self.start_url.format('1', parameter['sicCode'])
            # yield Request(url, callback=self.parse, meta={'page': 1})

    def parse(self, response):
        data = json.loads(response.text)['data']
        if data['list'] != []:
            hash_ids = [x['companyHashId'] for x in data['list']]   # data为companyHashId列表
            for hash_id in hash_ids:
                # 公司信息
                comp_url = 'https://x.xiaoman.cn/api/company-read/profile?id={}&brief_only=true'.format(hash_id)
                # comp_url = 'https://x.xiaoman.cn/api/company-read/profile?brief_only=true" + "&id=' + hash_id
                yield Request(url=comp_url, callback=self.parse_item, meta={'hashid': hash_id})

                # 出口信息
                # export_url = 'https://x.xiaoman.cn/api/company-read/customs-record?company_type=EXPORT&page=1&page_size=10&id={}'.format(hash_id)
                # yield Request(url=export_url, callback=self.parse_customs, meta={'hashid': hash_id, 'page': 1, 'type': 'EXPORT'})

                # 进口信息
                # import_url = 'https://x.xiaoman.cn/api/company-read/customs-record?company_type=IMPORT&page=1&page_size=10&id={}'.format(hash_id)
                # yield Request(url=import_url, callback=self.parse_customs, meta={'hashid': hash_id, 'page': 1, 'type': 'IMPORT'})

    def parse_item(self, response):
        item_comp = CompItem()
        item_profit = ProfitItem()
        item_cash = CashItem()
        item_decash_all = Decash_AllItem()
        item_decash = DecashItem()
        item_decash_eq = Decash_EqItem()

        # comp 公司信息表（13项）
        data = json.loads(response.text)['data']
        # item['comp_no']   自动生成
        item_comp['comp_name'] = data['companyName'] if 'companyName' in data else ''
        item_comp['hashid'] = response.meta['hashid']
        item_comp['main_industry'] = data['sicName'] if 'sicName' in data else ''
        item_comp['home_page'] = data['homepage'] if 'homepage' in data else ''
        item_comp['comp_tel'] = data['phone'] if 'phone' in data else ''
        item_comp['comp_addr'] = data['address'] if 'address' in data else '' + ',' + data['city'] if 'city' in data else '' \
                                + ',' + data['province'] if 'province' in data else '' + ',' + data['postcode'] if 'postcode' in data else '' \
                                + ',' + data['country'] if 'country' in data else ''
        item_comp['comp_intro'] = data['description'] if 'description' in data else ''
        item_comp['comp_type'] = data['companyType'] if 'companyType' in data else ''
        item_comp['year_found'] = data['foundedYear'] if 'foundedYear' in data else -1
        item_comp['comp_sales'] = data['sales'] if 'sales' in data else -1.00
        item_comp['employees_num'] = data['employees'] if 'employees' in data else -1
        item_comp['comp_assets'] = data['asserts'] if 'asserts' in data else ''
        item_comp['trade_style'] = data['tradestyle'] if 'tradestyle' in data else ''
        item_comp['sic_code'] = 0
        item_comp['custom_import_count'] = 0
        item_comp['custom_export_count'] = 0
        item_comp['email_count'] = ''
        item_comp['comp_add_intro'] = ''
        item_comp['country'] = data['country'] if 'country' in data else ''

        # 公司描述追加
        hash_id = response.meta['hashid']
        comp_add_url = 'https://x.xiaoman.cn/api/company-read/profile-official-site-parse-info?id={}'.format(hash_id)
        yield Request(url=comp_add_url, callback=self.parse_add_intro, meta={'hashid': hash_id, 'item': item_comp})

        # profit 综合损益表（8项）
        if 'incomeStatement' in data:
            for y in range(1, len(data['incomeStatement']['header'])):
                # data['incomeStatement']['width']
                item_profit['hashid'] = response.meta['hashid']
                item_profit['year'] = data['incomeStatement']['header'][y] if data['incomeStatement']['header'][y] != '' else -1
                item_profit['revenue'] = data['incomeStatement']['body'][0][y] if y < len(data['incomeStatement']['body'][0]) else ''
                item_profit['gross_profit'] = data['incomeStatement']['body'][1][y] if y < len(data['incomeStatement']['body'][1]) else ''
                item_profit['operating_income'] = data['incomeStatement']['body'][2][y] if y < len(data['incomeStatement']['body'][2]) else ''
                item_profit['net_income'] = data['incomeStatement']['body'][3][y] if y < len(data['incomeStatement']['body'][3]) else ''
                item_profit['diluted_eps'] = data['incomeStatement']['body'][4][y] if y < len(data['incomeStatement']['body'][4]) else ''
                yield item_profit

        # cash 现金流量表（10项）
        if 'cashFlow' in data:
            for y in range(1, len(data['cashFlow']['header'])):
                item_cash['hashid'] = response.meta['hashid']
                item_cash['year'] = data['cashFlow']['header'][y] if data['incomeStatement']['header'][y] != '' else -1
                item_cash['cash_begin'] = data['cashFlow']['body'][0][y] if y < len(data['cashFlow']['body'][0]) else ''
                item_cash['net_operate'] = data['cashFlow']['body'][1][y] if y < len(data['cashFlow']['body'][1]) else ''
                item_cash['net_invest'] = data['cashFlow']['body'][2][y] if y < len(data['cashFlow']['body'][2]) else ''
                item_cash['net_finance'] = data['cashFlow']['body'][3][y]if y < len(data['cashFlow']['body'][3]) else ''
                item_cash['net_change'] = data['cashFlow']['body'][4][y] if y < len(data['cashFlow']['body'][4]) else ''
                item_cash['cash_end'] = data['cashFlow']['body'][5][y] if y < len(data['cashFlow']['body'][5]) else ''
                item_cash['capital_exp'] = data['cashFlow']['body'][6][y] if y < len(data['cashFlow']['body'][6]) else ''
                yield item_cash

        # decash_all 资产负债表——资产表（13项）
        if 'balanceSheet' in data:
            for y in range(1, len(data['balanceSheet']['header'])):
                item_decash_all['hashid'] = response.meta['hashid']
                item_decash_all['year'] = data['balanceSheet']['header'][y] if data['incomeStatement']['header'][y] != '' else -1
                item_decash_all['current_assets'] = data['balanceSheet']['body'][0][y] if y < len(data['balanceSheet']['body'][0]) else ''
                item_decash_all['cash'] = data['balanceSheet']['body'][1][y] if y < len(data['balanceSheet']['body'][1]) else ''
                item_decash_all['net_receivables'] = data['balanceSheet']['body'][2][y] if y < len(data['balanceSheet']['body'][2]) else ''
                item_decash_all['inventory'] = data['balanceSheet']['body'][3][y] if y < len(data['balanceSheet']['body'][3]) else ''
                item_decash_all['other_income'] = data['balanceSheet']['body'][4][y] if y < len(data['balanceSheet']['body'][4]) else ''
                item_decash_all['assets_summary'] = data['balanceSheet']['body'][5][y] if y < len(data['balanceSheet']['body'][5]) else ''
                item_decash_all['total_curassets'] = data['balanceSheet']['body'][6][y] if y < len(data['balanceSheet']['body'][6]) else ''
                item_decash_all['net_fixed'] = data['balanceSheet']['body'][7][y] if y < len(data['balanceSheet']['body'][7]) else ''
                item_decash_all['other_noncurrent'] = data['balanceSheet']['body'][8][y] if y < len(data['balanceSheet']['body'][8]) else ''
                item_decash_all['total_assets'] = data['balanceSheet']['body'][9][y] if y < len(data['balanceSheet']['body'][9]) else ''
                yield item_decash_all

        # decash 资产负债表——负债表（12项）
        if 'balanceSheet2' in data:
            for y in range(1, len(data['balanceSheet2']['header'])):
                item_decash['hashid'] = response.meta['hashid']
                item_decash['year'] = data['balanceSheet2']['header'][y] if data['incomeStatement']['header'][y] != '' else -1
                item_decash['current_liabilities'] = data['balanceSheet2']['body'][0][y] if y < len(data['balanceSheet2']['body'][0]) else ''
                item_decash['accounts_payable'] = data['balanceSheet2']['body'][1][y] if y < len(data['balanceSheet2']['body'][1]) else ''
                item_decash['short_debt'] = data['balanceSheet2']['body'][2][y] if y < len(data['balanceSheet2']['body'][2]) else ''
                item_decash['other_curliability'] = data['balanceSheet2']['body'][3][y] if y < len(data['balanceSheet2']['body'][3]) else ''
                item_decash['liability_summary'] = data['balanceSheet2']['body'][4][y] if y < len(data['balanceSheet2']['body'][4]) else ''
                item_decash['total_curliability'] = data['balanceSheet2']['body'][5][y] if y < len(data['balanceSheet2']['body'][5]) else ''
                item_decash['long_debt'] = data['balanceSheet2']['body'][6][y] if y < len(data['balanceSheet2']['body'][6]) else ''
                item_decash['other_noncurliability'] = data['balanceSheet2']['body'][7][y] if y < len(data['balanceSheet2']['body'][7]) else ''
                item_decash['total_liability']= data['balanceSheet2']['body'][8][y] if y < len(data['balanceSheet2']['body'][8]) else ''
                yield item_decash

        # decash_eq 资产负债表——所有者权益（9项）
        if 'balanceSheet3' in data:
            for y in range(1, len(data['balanceSheet3']['header'])):
                item_decash_eq['hashid'] = response.meta['hashid']
                item_decash_eq['year'] = data['balanceSheet3']['header'][y] if data['incomeStatement']['header'][y] != '' else -1
                item_decash_eq['equity'] = data['balanceSheet3']['body'][0][y] if y < len(data['balanceSheet3']['body'][0]) else ''
                item_decash_eq['prefer_equity'] = data['balanceSheet3']['body'][1][y] if y < len(data['balanceSheet3']['body'][1]) else ''
                item_decash_eq['common_equity'] = data['balanceSheet3']['body'][2][y] if y < len(data['balanceSheet3']['body'][2]) else ''
                item_decash_eq['equity_summary'] = data['balanceSheet3']['body'][3][y] if y < len(data['balanceSheet3']['body'][3]) else ''
                item_decash_eq['total_equity'] = data['balanceSheet3']['body'][4][y] if y < len(data['balanceSheet3']['body'][4]) else ''
                item_decash_eq['shares_outstanding'] = data['balanceSheet3']['body'][5][y] if y < len(data['balanceSheet3']['body'][5]) else ''
                yield item_decash_eq

    def parse_add_intro(self, response):
        item_comp = response.meta['item']
        hash_id = response.meta['hashid']
        data = json.loads(response.text)['data']
        if data != {}:
            item_comp['comp_add_intro'] = data['description']
        else:
            item_comp['comp_add_intro'] = ''

        # 联系人订购
        # order_url = 'https://x.xiaoman.cn/api/account-write/company-purchase?id={}'.format(hash_id)
        # yield Request(url=order_url, callback=self.parse_order)

        # 联系人信息
        cont_url = 'https://x.xiaoman.cn/api/company-read/profile-emails?id={}&sort=email&keyword=&page=1'.format(hash_id)
        yield Request(url=cont_url, callback=self.parse_cont, meta={'hashid': hash_id, 'page': 1, 'item': item_comp})


    # def parse_customs(self, response):
    #     item = CustomsItem()
    #     page = json.loads(response.text)['data']['totalPages']
    #     data = json.loads(response.text)['data']['content']
    #     if data != []:
    #         for line in data:
    #             item['hashid'] = response.meta['hashid']
    #             item['port_time'] = line['date']
    #             item['all_buyers'] = line['importer'] if 'importer' in line else line['exporter']
    #             item['HS_Code'] = line['hsCode'] if line['hsCode'] != '' else -1
    #             item['prod_desc'] = line['productDesc']
    #             item['value_sum'] = line['price'] if line['price'] != None else -1
    #             yield item
    #             customs_info_url = 'https://x.xiaoman.cn/api/company-read/customs-detail?id={}'.format(line['id'])
    #             yield Request(url=customs_info_url, callback=self.parse_customs_info, meta={'hashid': response.meta['hashid']})
    #         next_page = response.meta['page'] + 1
    #         if next_page <= page:
    #             next_url = 'https://x.xiaoman.cn/api/company-read/customs-record?company_type={}&page={}&page_size=10&id={}'.format(response.meta['type'], next_page, response.meta['hashid'])
    #             yield Request(url=next_url, callback=self.parse_customs, meta={'hashid': response.meta['hashid'], 'page': next_page, 'type': response.meta['type']})

    # def parse_customs_info(self, response):
    #     item = Customs_InfoItem()
    #     data = json.loads(response.text)['data']
    #     item['customs_hashid'] = response.meta['hashid']
    #     item['port_time'] = data['date']
    #     item['import_country'] = data['importerCountry']
    #     item['importer'] = data['importer']
    #     item['import_depart'] = data['importerDepartment']
    #     item['import_economy'] = data['importerEconomicKey']
    #     item['import_cont'] = data['notifyParty']
    #     item['import_contactinfo'] = data['notifyPartyContact']
    #     item['import_email'] = data['importerEmail']
    #     item['import_fax'] = data['importerFax']
    #     item['import_tel'] = data['importerTelephone']
    #     item['import_mail'] = data['importerPostal']
    #     item['import_addr'] = data['importerAddress']
    #     item['export_country'] = data['exporterCountry']
    #     item['exporter'] = data['exporter']
    #     item['export_contactinfo'] = data['exporterContact']
    #     item['export_city'] = data['experterCity']
    #     item['export_addr'] = data['exporterAddress']
    #     item['HS_Code'] = data['hsCode'] if data['hsCode'] != None else -1
    #     item['prim_HScode'] = data['hsCodeSource'] if data['hsCodeSource'] != None else -1
    #     item['brand'] = data['brand']
    #     item['prod_desc'] = data['productDesc']
    #     item['trans_price'] = data['cif'] if data['cif'] != None else -1
    #     item['trans_unitprice'] = data['cifUnit'] if data['cifUnit'] != None else -1
    #     item['offshore_price'] = data['fob'] if data['fob'] != None else -1
    #     item['offshore_unitprice'] = data['fobUnit'] if data['fobUnit'] != None else -1
    #     item['payment_amount'] = data['payment']
    #     item['invoice_sum'] = data['totalInv'] if data['totalInv'] != None else -1
    #     item['freight_fee'] = data['freight'] if data['freight'] != None else -1
    #     item['insurance_fee'] = data['insurance'] if data['insurance'] != None else -1
    #     item['tax_rate'] = data['taxPercents']
    #     item['customs_clearance'] = data['valorAdv'] if data['valorAdv'] != None else -1
    #     item['gross_weight'] = data['gWeight'] if data['gWeight'] != None else -1
    #     item['gross_amount'] = data['totalGWeight'] if data['totalGWeight'] != None else -1
    #     item['net_weight'] = data['nWeight'] if data['nWeight'] != None else -1
    #     item['net_amount'] = data['totalNWeight'] if data['totalNWeight'] != None else -1
    #     item['prod_num'] = data['quantity'] if data['quantity'] != None else -1
    #     item['num_unit'] = data['unitOfQuantity']
    #     item['pack_num'] = data['packages'] if data['packages'] != None else -1
    #     item['pack_method'] = data['typeOfPackage']
    #     item['cargo_agent'] = data['transAgent']
    #     item['ship_type'] = data['transType']
    #     item['ship_comp'] = data['transCorp']
    #     item['transp_country'] = data['transCorpCountry']
    #     item['source_port'] = data['originPort']
    #     item['destination_port'] = data['destPort']
    #     item['transit_port'] = data['transportationWay']
    #     item['origin_country'] = data['originCountry']
    #     item['customs_name'] = data['customs']
    #     item['customs_agent'] = data['customsAgent']
    #     item['remarks'] = data['remark']
    #     yield item

    # def parse_order(self, response):
    #     return None

    def parse_cont(self, response):
        item_comp = response.meta['item']
        item = ContItem()
        if json.loads(response.text)['code'] == 0:
            data = json.loads(response.text)['data']
            item_comp['email_count'] = data['emailCount']
            yield item_comp
            if data['emailCount'] > 0:
                # total_page = data['emailCount'] // 9 + 1
                for email in data['emails']:
                    item['hashid'] = response.meta['hashid']
                    # item['cont_name'] = email['first_name'] + email['last_name']
                    item['cont_first_name'] = email['first_name'] if email['first_name'] != None else ''
                    item['cont_last_name'] = email['last_name'] if email['last_name'] != None else ''
                    item['cont_post'] = email['position'] if email['position'] != None else ''
                    item['cont_email'] = email['id']
                    item['cont_url'] = email['sources'][0]['uri'] if email['sources'] != [] else ''
                    yield item
                # next_page = response.meta['page'] + 1
                # if next_page <= total_page:
                #     next_page = 'https://x.xiaoman.cn/api/company-read/profile-emails?id={}&sort=&keyword=&page={}'.format(response.meta['hashid'], next_page)
                #     yield Request(url=next_page, callback=self.parse_cont, meta={'hashid': response.meta['hashid'], 'page': next_page})
        else:
            item_comp['email_count'] = 0
            yield item_comp

        # 注册商标
        hash_id = response.meta['hashid']
        image_url = 'https://x.xiaoman.cn/api/company-read/profile-trademarks?id={}'.format(hash_id)
        yield Request(url=image_url, callback=self.parse_image, meta={'hashid': hash_id})

    def parse_image(self, response):
        data = json.loads(response.text)['data']
        if data != []:
            logging.warning('图片下载启动！')
            hash_id = response.meta['hashid']
            path = os.path.join('D:\XiaomanImage', hash_id)
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)
            # for image in data:
            #     logging.warning('图片开始下载！')
            #     image_id = image['imageId']
            #     image_url = image['imageUrl']
            #     image = requests.get(image_url)
            #     f = open(image_id + '.jpg', 'ab')
            #     f.write(image.content)
            #     f.close()
            image = data[0]
            logging.warning('图片开始下载！')
            image_id = image['imageId']
            image_url = image['imageUrl']
            image = requests.get(image_url)
            f = open(image_id + '.jpg', 'ab')
            f.write(image.content)
            f.close()

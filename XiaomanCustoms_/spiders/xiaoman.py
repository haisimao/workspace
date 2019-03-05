from scrapy import Spider, Request
from XiaomanCustoms.items import CompItem, ContItem, CustomsItem, Customs_InfoItem, ProfitItem, CashItem, Decash_AllItem, DecashItem, Decash_EqItem, ImageItem
from scrapy import FormRequest
import json


class XiaomanSpider(Spider):
    name = 'xiaoman'
    start_url = 'https://x.xiaoman.cn/api/company-read/mining-list?industryType=sic&page_size={}&page={}&sicCode={}'
    #start_url = 'https://x.xiaoman.cn/api/company-read/mining-list?industryType=sic'

    def start_requests(self):
        parameter = {
            'page_size': '25',
            'sicCode': '01000000,01100000,01110000,01120000,01150000,01160000,01190000,01190100,01190101,01190102,01190103,01190104,01190105,01190200,01190201,01190202,01190203,01190300,01190301,01190302,01190303,01190400,01190401,01190402,01190403,01190404,01199900,01199901,01300000,01310000,01319900,01319901,01320000,01330000,01339900,01339901,01339902,01340000,01390000,01390100,01390101,01390102,01390103,01390104,01390105,01390200,01390201,01390202,01399900,01399901,01399902,01399903,01399904,01399905,01399906,01600000,01610000,01610100,01610101,01610102,01610103,01610104,01610200,01610201,01610202,01610203,01610204,01610300,01610301,01610302,01610303,01610400,01610401,01610402,01610403,01610404,01610405,01610406,01610407,01610408,01610409,01610410,01610411,01619900,01619901,01619902,01619903,01619904,01619905,01619906,01619907,01619908,01619909,01700000,01710000,01719900,01719901,01719902,01719903,01719904,01719905,01719906,01719907,01719908,01719909,01720000,01730000,01739900,01739901,01739902,01739903,01739904,01739905,01739906,01739907,01739908,01740000,01749900,01749901,01749902,01749903,01749904,01749905,01749906,01750000,01759900,01759901,01759902,01759903,01759904,01759905,01759906,01759907,01759908,01759909,01759910,01759911,01790000,01799900,01799901,01799902,01799903,01799904,01799905,01799906,01799907,01799908,01799909,01799910,01799911,01799912,01799913,01800000,01810000,01810100,01810101,01810102,01810103,01810104,01810105,01810106,01810107,01810200,01810201,01810202,01810203,01810204,01810300,01810301,01810302,01810303,01819900,01819901,01819902,01820000,01820100,01820101,01820102,01820103,01820104,01820105,01820106,01829900,01829901,01829902,01829903,01900000,01910000'
        }
        urls = [self.start_url.format(parameter['page_size'], str(page), parameter['sicCode']) for page in range(1, 401)]
        yield from [Request(url, callback=self.parse, dont_filter=True) for url in urls]
        #yield Request(self.start_url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        hash_ids = [x['companyHashId'] for x in data['data']['list']]   # data为companyHashId列表
        for hash_id in hash_ids:
            # 公司信息
            comp_url = 'https://x.xiaoman.cn/api/company-read/profile?brief_only=true" + "&id=' + hash_id
            yield Request(url=comp_url, callback=self.parse_item, meta={'hashid': hash_id}, dont_filter=True)

            # 出口信息
            # export_url = 'https://x.xiaoman.cn/api/company-read/customs-record?company_type=EXPORT&page=1&page_size=10&id={}'.format(hash_id)
            # yield Request(url=export_url, callback=self.parse_customs, meta={'hashid': hash_id, 'page': 1, 'type': 'EXPORT'})

            # 进口信息
            # import_url = 'https://x.xiaoman.cn/api/company-read/customs-record?company_type=IMPORT&page=1&page_size=10&id={}'.format(hash_id)
            # yield Request(url=import_url, callback=self.parse_customs, meta={'hashid': hash_id, 'page': 1, 'type': 'IMPORT'})
            # 联系人信息
            cont_url = 'https://x.xiaoman.cn/api/company-read/profile-emails?id={}&sort=&keyword=&page=1'.format(hash_id)
            yield Request(url=cont_url, callback=self.parse_cont, meta={'hashid': hash_id, 'page': 1}, dont_filter=True)
            # 注册商标
            # image_url = 'https://x.xiaoman.cn/api/company-read/profile-trademarks?id={}'.format(hash_id)
            # yield Request(url=import_url, callback=self.parse_image, meta={'hashid': hash_id})

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
        item_comp['main_industry'] = data['sicName'] if 'sicName' in data else ''
        item_comp['home_page'] = data['homepage'] if 'homepage' in data else ''
        item_comp['comp_tel'] = data['phone'] if 'phone' in data else ''
        item_comp['comp_addr'] = data['address'] if 'address' in data else '' + ',' + data['city'] if 'city' in data else '' \
                                + ',' + data['province'] if 'province' in data else '' + ',' + data['postcode'] if 'postcode' in data else '' \
                                + ',' + data['country'] if 'country' in data else ''
        item_comp['comp_intro'] = data['description'] if 'description' in data else ''
        item_comp['comp_type'] = data['companyType'] if 'companyType' in data else ''
        item_comp['year_found'] = data['foundedYear'] if 'foundedYear' in data else -1
        item_comp['comp_sales'] = data['sales'] if 'sales' in data else ''
        item_comp['employees_num'] = data['employees'] if 'employees' in data else -1
        item_comp['comp_assets'] = data['asserts'] if 'asserts' in data else ''
        item_comp['trade_style'] = data['tradestyle'] if 'tradestyle' in data else ''
        item_comp['hashid'] = response.meta['hashid']
        yield item_comp

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

    def parse_cont(self, response):
        item = ContItem()
        if json.loads(response.text)['code'] == 0:
            data = json.loads(response.text)['data']
            if data['contactCount'] > 0:
                total_page = data['contactCount'] // 9 + 1
                for email in data['emails']:
                    item['hashid'] = response.meta['hashid']
                    item['cont_name'] = email['first_name'] + email['last_name']
                    item['cont_post'] = email['position']
                    item['cont_email'] = email['value']
                    item['cone_url'] = [source['url'] for source in email['sources'] if email['sources'] != []]
                    yield item
                # next_page = response.meta['page'] + 1
                # if next_page <= total_page:
                #     next_page = 'https://x.xiaoman.cn/api/company-read/profile-emails?id={}&sort=&keyword=&page={}'.format(response.meta['hashid'], next_page)
                #     yield Request(url=next_page, callback=self.parse_cont, meta={'hashid': response.meta['hashid'], 'page': next_page})

    def parse_image(self, response):
        item = ImageItem()
        data = json.loads(response.text)['data']
        if data != []:
            item['url'] = response.url
            item['image_path'] = response.meta['hashid']
            item['image_urls'] = [url['imageUrl'] for url in data if url['imageUrl'] != None]
            yield item

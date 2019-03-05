import datetime
import re

import pymysql
from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
from urllib.request import quote

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from LinkedinSpideScrapy.items import LinkedinspidescrapyItem
from LinkedinSpideScrapy.utils import LikedinException
from db import RedisClient


class LinkedinSpider(CrawlSpider):
    name = 'linkedin'
    origin_url = '''https://www.linkedin.com/voyager/api/organization/companies?decoration=%28adsRule%2CaffiliatedCompaniesWithEmployeesRollup%2CaffiliatedCompaniesWithJobsRollup%2CarticlePermalinkForTopCompanies%2CautoGenerated%2CbackgroundCoverImage%2Cclaimable%2CclaimableByViewer%2CcompanyEmployeesSearchPageUrl%2CcompanyPageUrl%2CcompanyType%2CconfirmedLocations*%2CcoverPhoto%2CdataVersion%2Cdescription%2CentityUrn%2CfollowingInfo%2CfoundedOn%2Cheadquarter%2CjobSearchPageUrl%2ClcpTreatment%2Clogo%2Cname%2Ctype%2CoverviewPhoto%2CpaidCompany%2CpartnerCompanyUrl%2CpartnerLogo%2CpartnerLogoImage%2Cpermissions%2CrankForTopCompanies%2CsalesNavigatorCompanyUrl%2Cschool%2Cshowcase%2CstaffCount%2CstaffCountRange%2CstaffingCompany%2CtopCompaniesListName%2CuniversalName%2Curl%2CviewerConnectedToAdministrator%2CviewerEmployee%2CviewerFollowingJobsUpdates%2CviewerPendingAdministrator%2CcompanyIndustries*%2Cindustries%2Cspecialities%2CacquirerCompany~%28entityUrn%2Clogo%2Cname%2Cindustries%2CfollowingInfo%2Curl%2CpaidCompany%2CuniversalName%29%2CaffiliatedCompanies*~%28entityUrn%2Clogo%2Cname%2Cindustries%2CfollowingInfo%2Curl%2CpaidCompany%2CuniversalName%29%2Cgroups*~%28entityUrn%2ClargeLogo%2Clogo%2CgroupName%2CmemberCount%2CwebsiteUrl%2Curl%29%2CshowcasePages*~%28entityUrn%2Clogo%2Cname%2Cindustries%2CfollowingInfo%2Curl%2Cdescription%2CuniversalName%29%29&q=universalName&universalName={}'''

    def __init__(self):
        super(LinkedinSpider, self).__init__()
        # 建立数据库连接
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password="yq201808",
            database='to_balalaba',
            use_unicode=True,
            charset="utf8mb4",  # 指定字符编码
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.conn = RedisClient('cookies', 'linkedin')
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        dispatcher.connect(self.closeSpider, signals.spider_closed)

    def closeSpider(self, spider):
        print('spider closed at {}'.format(datetime.datetime.now()))

    def start_requests(self):
        '''
        第一个请求
        :return:timemore={}&timeless={}
        '''
        with self.connection.cursor() as cursor:
            # 2018/11/9----ID编号记录   733760 --- 904583
            cursor.execute('''select comp_name, comp_no from comps where comp_no < 904583  and comp_no > 733760;''')
            # cursor.execute('''select comp_name, comp_no from comps ORDER BY comp_no DESC;''')
            # cursor.execute('''select comp_name, comp_no from comps;''')
            response = cursor.fetchall()
            print('本次更新' + str(len(response)) + '条数据')
        for comp in response:
            # 规则公司搜索名
            try:
                company_name = re.sub(',', '', comp.get('comp_name'))
                company_name = re.sub(' ', '-', company_name)
                send_url = self.origin_url.format(quote(company_name))
                # 批量进行公司信息提取
                import json
                cookies = json.loads(self.conn.random())
                yield Request(send_url, callback=self.parse_index, meta={'company_name': comp.get('comp_name'), }, cookies=cookies)
            except:
                print('查询{}失败,{}'.format(comp.get('comp_no'), datetime.datetime.now()))
                raise LikedinException('爬取{}阻塞,{}.请重启'.format(comp.get('comp_no'), datetime.datetime.now()))

    def parse_index(self, response):
        import json
        comp_info = json.loads(response.text)
        items = LinkedinspidescrapyItem()
        if comp_info['elements'][0].get('headquarter'):
            try:
                comp_addr = comp_info['elements'][0].get('headquarter')
                if comp_addr:
                    line1 = comp_info['elements'][0].get('headquarter').get('line1')
                    line2 = comp_info['elements'][0].get('headquarter').get('line2')
                    line3 = comp_info['elements'][0].get('headquarter').get('line3')
                    city = comp_info['elements'][0].get('headquarter').get('city')
                    geographicArea = comp_info['elements'][0].get('headquarter').get('geographicArea')
                    postalCode = comp_info['elements'][0].get('headquarter').get('postalCode')
                    country = comp_info['elements'][0].get('headquarter').get('country')
                    if line2:
                        items['comp_addr'] = line1 + ',' + line2 + ',' + city + ',' + geographicArea + ' ' + postalCode + ',' + country
                    elif line3:
                        items['comp_addr'] = line1 + ',' + line2 + ',' + line3 + ',' + city + ',' + geographicArea + ' ' + postalCode + ',' + country
                    else:
                        items['comp_addr'] = line1 + ',' + city + ',' + geographicArea + ' ' + postalCode + ',' + country

            except:
                items['comp_addr'] = ''
            # 公司主页
            try:
                home_page = comp_info['elements'][0].get('companyPageUrl')
                items['home_page'] = home_page if home_page else ''
            except:
                pass
            # 公司规模
            try:
                employees_num = comp_info['elements'][0].get('staffCountRange')
                if employees_num:
                    if int(employees_num.get('start')) == 10001:
                        items['employees_num'] = 10001
                    else:
                        scale = int(employees_num.get('start')) + int(int(employees_num.get('end')) - int(employees_num.get('start'))/2)
                        items['employees_num'] = scale
                else:
                    items['employees_num'] = ''
            except:
                items['employees_num'] = ''
            # 公司描述
            try:
                comp_intro = comp_info['elements'][0].get('description')
                items['comp_intro'] = comp_intro if comp_intro else ''
            except:
                items['comp_intro'] = ''
            # 公司成立年份
            try:
                year_found = comp_info['elements'][0].get('foundedOn').get('year')
                items['year_found'] = year_found if year_found else ''
            except:
                items['year_found'] = ''
            items['company_name'] = response.meta.get('company_name')
        # 公司类型暂不考虑
        # text['elements'][0]['companyType']

        yield items
















































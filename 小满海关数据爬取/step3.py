import requests
import pymysql
import os
import traceback
import time
from Util.Config import GetConfig
from Util.tools import user_agent, XiaoManException
from Util.tools import get_cookie
from Util.tools import remove_cookie

'''
    海关信息表   customs
    海关数据表   customs_info    包括进口出口
'''

con = pymysql.connect(
        host='localhost',
        user='root',
        password="yq201808",
        database='xiaoman',
        use_unicode=True,
        charset="utf8mb4"
    )
cur = con.cursor()

con1 = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='xiaoman',
        password="xiaoman2018!!",
        database='xiaoman',
        use_unicode=True,
        charset="utf8mb4"
    )
cur1 = con1.cursor()


class Spider():
    def __init__(self):
        self.config = GetConfig()
        self.session = requests.Session()
        self.session.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'origin': 'https://x.xiaoman.cn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.errorlog = ''

        self.url1 = 'https://x.xiaoman.cn/api/company-read/customs-record?'
        self.url2 = 'https://x.xiaoman.cn/api/company-read/customs-detail?id='
        self.params = {
            'page_size': 10
        }
        self.flag = False

    def get_data(self, hashid, type, siccode, allpage):
        params1 = self.params
        params1['id'] = hashid
        params1['company_type'] = type
        page = 0
        # while True:
        while page < 5:
            page += 1
            if hashid == self.config.get('hashid3') and str(page) == self.config.get('page3'):
                self.flag = True
            if self.config.get('hashid3') == '':
                self.flag = True
            if self.flag:
                print('休眠{}秒'.format(self.config.get('wait')))
                time.sleep(int(self.config.get('wait')))
                print('\n第{}类，第{}页'.format(siccode, allpage))
                self.config.set('hashid3', hashid)
                self.config.set('page3', str(page))
                params1['page'] = page
                print('{},总页数{}-{}'.format(hashid, type, page))

                user, proxy, cookies = get_cookie()
                print('step3-1 本次代理：{}'.format(proxy))
                self.session.headers['user-agent'] = user_agent()
                self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
                try:
                    response = self.session.get(url=self.url1, params=params1, proxies={'http': proxy}).json()
                    print(response)

                    if response['code'] == 302 or response['code'] == -10002:
                        print('身份信息已过期！')
                        remove_cookie(user)
                        self.get_data(hashid)
                        return

                    if response['code'] == -10005:
                        print('身份信息已过期！')
                        remove_cookie(user)
                        self.get_data(hashid)
                        raise XiaoManException('cookies已失效, 请更换账号登陆')
                        return

                    if response['code'] == -1:
                        return
                    # 判断数据是否为空, 为空则退出
                    content = response['data']['content']
                    if content == []:
                        print('没有记录或抓取完成...')
                        return
                    # totalElements
                    #海关信息表
                    for i in content:
                        line1 = [
                                 hashid,
                                 i['date'],
                                 self.res(i['importer']),
                                 i['hsCode'] if i['hsCode'] != '' else -1,
                                 self.res(i['productDesc']),
                                 i['price'] if i['price'] != None else -1,
                                 # data['totalElements'],
                                 # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                                 ]
                        print(line1)
                        sql = "insert into customs values ('{0[0]}', '{0[1]}', '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}', now())".format(line1)
                        print('insert into customs:')
                        self.write2sql(sql)
                        #customs_info详情信息表
                        self.get_data1(i['id'], hashid)
                        time.sleep(1)
                    if page == 1:
                        try:
                            total = response['data']['totalElements'] if response['data']['totalElements'] else '0'
                            cur1.execute('insert into custom_data_total (hashid, type, total) values (%s,%s,%s)', (hashid, type, total))
                            cur.execute('insert into custom_data_total (hashid, type, total) values (%s,%s,%s)', (hashid, type, total))
                            con.commit()
                            con1.commit()
                        except:
                            print('插入总量数据出错')
                        print(response['data']['totalElements'])
                except Exception as e:
                    self.errorlog += '{}-{}-{}-{}&'.format(hashid, page, type, traceback.format_exc())
                    # print(traceback.format_exc())
                    # print('{}-{}-{}获取失败...\n'.format(hashid, type, page))
            else:
                return

    def get_data1(self, contentid, hashid):
        '''
        海关明细表
        :param contentid:
        :param hashid:
        :return:
        '''
        url = self.url2 + contentid

        user, proxy, cookies = get_cookie()
        print('step3-2 本次代理：{}'.format(proxy))
        self.session.headers['user-agent'] = user_agent()
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        try:
            response = self.session.get(url=url, proxies={'http': proxy}).json()
            data = ''
            if 'data' in response:
                data = response['data']
            else:
                return
            # customs_info详情信息表

            line2 = [
                hashid,
                self.res(data['date']) if 'data' in data else "",
                data['importerCountry'],
                self.res(data['importer']),
                data['importerDepartment'],
                data['importerEconomicKey'],
                data['notifyParty'],
                self.res(data['notifyPartyContact']) if data['notifyPartyContact'] != None else "",
                data['importerEmail'],
                data['importerFax'],
                data['importerTelephone'],
                data['importerPostal'],
                self.res(data['importerAddress']) if data['importerAddress'] != None else "",
                data['exporterCountry'],
                self.res(data['exporter']),
                self.res(data['exporterContact']) if data['exporterContact'] != None else "",
                data['experterCity'],
                self.res(data['exporterAddress']) if data['exporterAddress'] != None else "",
                self.res(data['hsCode']) if data['hsCode'] != None else '' + data['hsCodeDesc'] if data['hsCodeDesc'] != None else '',
                data['hsCodeSource'],
                data['brand'],
                self.res(data['productDesc']),
                data['cif'] if data['cif'] != None else -1,
                data['cifUnit'] if data['cifUnit'] != None else -1,
                data['fob'] if data['fob'] != None else -1,
                data['fobUnit'] if data['fobUnit'] != None else -1,
                data['payment'],
                data['totalInv'] if data['totalInv'] != None else -1,
                data['freight'] if data['freight'] != None else -1,
                data['insurance'] if data['insurance'] != None else -1,
                data['taxPercents'],
                data['valorAdv'] if data['valorAdv'] != None else -1,
                data['gWeight'] if data['gWeight'] != None else -1,
                data['totalGWeight'] if data['totalGWeight'] != None else -1,
                data['nWeight'] if data['nWeight'] != None else -1,
                data['totalNWeight'] if data['totalNWeight'] != None else -1,
                data['quantity'] if data['quantity'] != None else -1,
                data['unitOfQuantity'],
                data['packages'] if data['packages'] != None else -1,
                data['typeOfPackage'],
                data['transAgent'],
                data['transType'],
                data['transCorp'],
                data['transCorpCountry'],
                self.res(data['originPort']) if data['originPort'] != None else "",
                self.res(data['destPort']) if data['destPort'] != None else "",
                data['transportationWay'],
                data['originCountry'],
                data['customs'],
                data['customsAgent'],
                data['remark'],
                # data['totalElements'],
                # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
            ]
            sql = "insert into customs_info values " \
                  "(null, '{0[0]}', '{0[1]}', '{0[2]}','{0[3]}', '{0[4]}', '{0[5]}', '{0[6]}', '{0[7]}','{0[8]}', '{0[9]}'," \
                  "'{0[10]}', '{0[11]}', '{0[12]}','{0[13]}', '{0[14]}', '{0[15]}', '{0[16]}', '{0[17]}','{0[18]}', '{0[19]}'," \
                  "'{0[20]}', '{0[21]}', {0[22]},{0[23]}, {0[24]}, {0[25]}, '{0[26]}', {0[27]},{0[28]}, {0[29]}," \
                  "'{0[30]}', {0[31]}, {0[32]},{0[33]}, {0[34]}, {0[35]}, {0[36]}, '{0[37]}',{0[38]}, '{0[39]}'," \
                  "'{0[40]}', '{0[41]}', '{0[42]}','{0[43]}', '{0[44]}', '{0[45]}', '{0[46]}', '{0[47]}','{0[48]}', '{0[49]}'," \
                  "'{0[50]}', now())".format(line2)
            print('insert into customs_info:')
            self.write2sql(sql)
        except:
            self.errorlog +=  '{}-{}&'.format(contentid, traceback.format_exc())
            # print(traceback.format_exc())
            # print('{}获取失败...\n'.format(contentid))

    def res(self, str):
        return str.replace('\'', '\\\'')

    def write2sql(self, sql):
        '''
        执行SQL语句
        :param sql:
        :return:
        '''
        print(sql)
        cur.execute(sql)
        cur1.execute(sql)
        con.commit()
        con1.commit()

    def write2log(self, name):
        if not os.path.exists("log"):
            os.mkdir("log")
        if not os.path.exists("log/step3"):
            os.mkdir("log/step3")
        with open('log/step3/{}.txt'.format(name), 'a', encoding='utf-8') as w:
            w.write(self.errorlog)


def step3(hashids, siccode, allpage):
    sp = Spider()

    print('step3 start...')
    if str(allpage) == sp.config.get('allpage3'):
        print('加载进度...')
        for hi in hashids:
            sp.get_data(hi[0], 'IMPORT', siccode, allpage)
            sp.get_data(hi[0], 'EXPORT', siccode, allpage)
        if sp.errorlog != '':
            sp.write2log(hashids[0][0])
        sp.config.set('hashid3', '')
        sp.config.set('page3', '1')
        sp.config.set('allpage3', str(allpage+1))
    else:
        print('本页内容已抓取！')
    print('step3结束..')


if __name__ == '__main__':
    sp = Spider()
    sp.get_data('2bc272ea8fd39b71', 'IMPORT', 'test', 1)
    sp.get_data('2bc272ea8fd39b71', 'EXPORT', 'test', 1)
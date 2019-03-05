# _*_ coding:utf-8 _*_
#created on 2018/6/27 20:09
import requests
import time
import os
import json
import pymysql
import traceback
from login1 import login
from Util.Config import GetConfig
from Util.tools import user_agent, XiaoManException
from Util.tools import get_cookie
from Util.tools import remove_cookie

'''
    公司信息           comp
    遍历综合损益表      profit
    现金流量表         cash
    资产负债表资产表    decash_all
    资产负债表负债表    decash
    所有者权益表       decash_eq
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

        self.url1 = 'https://x.xiaoman.cn/api/company-read/profile?brief_only=true'
        self.errorlog = ''

    def get_data(self, hashid):
        url = self.url1 + '&id=' + hashid
        print(url)

        user, proxy, cookies = get_cookie()
        print('step2:本次代理：{}'.format(proxy))
        self.session.headers['user-agent'] = user_agent()
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        try:
            response = self.session.get(url=url, proxies={'http': proxy}).json()
            time.sleep(1)
            uri = 'https://x.xiaoman.cn/api/company-read/profile-official-site-parse-info?id=' + hashid
            response_add_copm_info = self.session.get(url=uri, proxies={'http': proxy}).json()
            print(response, response_add_copm_info.get('data').get('description'))

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

            if 'data' not in response:
                return
            data = response['data']

            address = data['address'] + ',' + data['city'] + ',' + data['province'] if 'province' in data else "" + ',' + (data['postcode'] + ',' if 'postcode' in data else '')  + data['country']

            comp_add_description = response_add_copm_info.get('data').get('description')

            print(hashid)

            # 公司信息comp
            line = [self.res(data['companyName']),
                    self.res(data['sicName']) if data['sicName'] != None else "",
                    self.res(data['homepage']) if data['homepage'] != None else "",
                    data['phone'] if 'phone' in data else "",
                    self.res(address) if address != None else "",
                    self.res(data['description']),
                    self.res(data['locationType']) if 'locationType' in data and data['locationType'] != None else "",
                    data['yearofFounding'] if 'yearofFounding' in data and data['yearofFounding'] != None else -1,
                    data['sales'],
                    data['employeesAllSites'].replace(',', '') if 'employeesAllSites' in data and data['employeesAllSites'] != None else -1,
                    str(data['balanceSheet']['body'][len(data['balanceSheet']['body']) - 1][1] if 'balanceSheet' in data else ""),
                    data['tradestyle'] if 'tradestyle' in data and data['tradestyle'] != None else "",
                    hashid,
                    comp_add_description,
                    ]
            print(line)
            sql = "insert into comp values (null, '{0[0]}', '{0[12]}', '{0[1]}', '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}', '{0[6]}', {0[7]}, {0[8]}, '{0[9]}', '{0[10]}', '{0[11]}', now(), '{0[13]}')".format(line)
            print('insert into comp')
            self.write2sql(sql)

            # 遍历综合损益表profit
            if 'incomeStatement' in data:
                data1 = data['incomeStatement']
                for y in  range(1,len(data1['header'])):
                    if data1['header'][y] == '':
                        break
                    line = [
                        hashid,
                        self.res(data1['header'][y]),
                        self.res(data1['body'][0][y]),
                        self.res(data1['body'][1][y]),
                        self.res(data1['body'][2][y]),
                        self.res(data1['body'][3][y]),
                        self.res(data1['body'][4][y]),
                        # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                    ]
                    print(line)
                    sql = "insert into profit values ( '{0[0]}', {0[1]}, '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}', '{0[6]}', now())".format(line)
                    print('insert into profit:')
                    self.write2sql(sql)

            # 现金流量表cash
            if 'cashFlow' in data:
                data1 = data['cashFlow']
                for y in range(1, len(data1['header'])):
                    if data1['header'][y] == '':
                        break
                    line = [
                        hashid,
                        self.res(data1['header'][y]),
                        self.res(data1['body'][0][y]),
                        self.res(data1['body'][1][y]),
                        self.res(data1['body'][2][y]),
                        self.res(data1['body'][3][y]),
                        self.res(data1['body'][4][y]),
                        self.res(data1['body'][5][y]),
                        self.res(data1['body'][6][y]),
                        # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                    ]
                    print(line)
                    sql = "insert into cash values ('{0[0]}', {0[1]}, '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}', '{0[6]}', '{0[7]}', '{0[8]}' , now())".format(line)
                    print('insert into cash:')
                    self.write2sql(sql)

            # 资产负债表资产表decash_all
            if 'balanceSheet' in data:
                data1 = data['balanceSheet']
                for y in range(1, len(data1['header'])):
                    if data1['header'][y] == '':
                        break
                    line = [
                        hashid,
                        self.res(data1['header'][y]),
                        self.res(data1['body'][0][y]) if 1 < len(data1['body'][0]) else '',
                        self.res(data1['body'][1][y]),
                        self.res(data1['body'][2][y]),
                        self.res(data1['body'][3][y]),
                        self.res(data1['body'][4][y]),
                        self.res(data1['body'][5][y]) if 1 < len(data1['body'][5]) else '',
                        self.res(data1['body'][6][y]),
                        self.res(data1['body'][7][y]),
                        self.res(data1['body'][8][y]),
                        self.res(data1['body'][9][y]),
                        # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                    ]
                    print(line)
                    sql = "insert into decash_all values ( '{0[0]}', {0[1]}, '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}', '{0[6]}', '{0[7]}', '{0[8]}', '{0[9]}', '{0[10]}', '{0[11]}' , now())".format(line)
                    print('insert into decash_all:')
                    self.write2sql(sql)

            # 资产负债表负债表decash
            if 'balanceSheet2' in data:
                data1 = data['balanceSheet2']
                for y in range(1, len(data1['header'])):
                    if data1['header'][y] == '':
                        break
                    line = [
                        hashid,
                        self.res(data1['header'][y]),
                        self.res(data1['body'][0][y]) if 1 < len(data1['body'][0]) else '',
                        self.res(data1['body'][1][y]),
                        self.res(data1['body'][2][y]),
                        self.res(data1['body'][3][y]),
                        self.res(data1['body'][4][y]) if 1 < len(data1['body'][4]) else '',
                        self.res(data1['body'][5][y]) if 1 < len(data1['body'][5]) else '',
                        self.res(data1['body'][6][y]),
                        self.res(data1['body'][7][y]),
                        self.res(data1['body'][8][y]),
                        # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                    ]
                    print(line)
                    sql = "insert into decash values ( '{0[0]}', {0[1]}, '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}', '{0[6]}', '{0[7]}', '{0[8]}', '{0[9]}', '{0[10]}' , now())".format(line)
                    print('insert into decash:')
                    self.write2sql(sql)

            # 所有者权益表decash_eq
            if 'balanceSheet3' in data:
                data1 = data['balanceSheet3']
                for y in range(1, len(data1['header'])):
                    if data1['header'][y] == '':
                        break
                    line = [
                        hashid,
                        self.res(data1['header'][y]),
                        self.res(data1['body'][0][y]) if 1 < len(data1['body'][0]) else '',
                        self.res(data1['body'][1][y]),
                        self.res(data1['body'][2][y]),
                        self.res(data1['body'][3][y]) if 1 < len(data1['body'][3]) else '',
                        self.res(data1['body'][4][y]) if 1 < len(data1['body'][4]) else '',
                        self.res(data1['body'][5][y]) if 1 < len(data1['body'][5]) else '',
                        # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                    ]
                    print(line)
                    sql = "insert into decash_eq values ( '{0[0]}', {0[1]}, '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}', '{0[6]}', '{0[7]}', now())".format(line)
                    print('insert into decash_eq:')
                    self.write2sql(sql)

        except:
            self.errorlog += '{}-{}&'.format(hashid, traceback.format_exc())
            # print(traceback.format_exc())
            # print('{}获取失败...\n'.format(hashid))

    def res(self, str):
        return str.replace('\'', '\\\'')

    def write2sql(self, sql):
        print(sql)
        cur.execute(sql)
        cur1.execute(sql)
        con.commit()
        con1.commit()

    def write2log(self, name):
        if not os.path.exists("log"):
            os.mkdir("log")
        if not os.path.exists("log/step2"):
            os.mkdir("log/step2")
        with open('log/step2/{}.txt'.format(name), 'a', encoding='utf-8') as w:
                w.write(self.errorlog)


def step2(hashids, siccode, allpage):
    sp = Spider()

    flag = False

    print('step2 start...')
    if str(allpage) >= sp.config.get('allpage2'):
        print('加载进度...')
        for hi in hashids:
            if hi[0] == sp.config.get('hashid2'):
                flag = True
            if sp.config.get('hashid2') == '':
                flag = True
            if flag:
                print('休眠{}秒'.format(sp.config.get('wait')))
                time.sleep(int(sp.config.get('wait')))
                print('\n第{}类，第{}页'.format(siccode, allpage))
                sp.config.set('hashid2', hi[0])
                sp.get_data(hi[0])
        if sp.errorlog != '':
            sp.write2log(hashids[0][0])
        sp.config.set('hashid2', '')
        sp.config.set('allpage2', str(allpage+1))
    else:
        print('本页内容已抓取！')
    print('step2结束！')
    return


if __name__ == '__main__':
    pass
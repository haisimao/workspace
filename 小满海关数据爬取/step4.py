# _*_ coding:utf-8 _*_
#created on 2018/6/27 20:09
import requests
import csv
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
    联系人信息表  cont
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
        port= 3306,
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
        self.url1 = 'https://x.xiaoman.cn/api/company-read/profile-emails?id={}&sort=email&keyword='
        self.errorlog = ''
        self.flag = False

    def get_data(self, hashid, siccode, allpage):
        url = self.url1.format(hashid)
        page = 0
        # while True:
        while page < 1:
            page += 1   # 本次爬取的页数
            if hashid == self.config.get('hashid4') and str(page) == self.config.get('page4'):  #
                self.flag = True
            if self.config.get('hashid4') == '':    # 判断是否配置文件存在公司名
                self.flag = True
            if self.flag:
                print('休眠{}秒'.format(self.config.get('wait')))
                time.sleep(int(self.config.get('wait')))
                print('\n第{}类，第{}页'.format(siccode, allpage))
                self.config.set('hashid4', hashid)
                self.config.set('page4', str(page))
                url_ = url + '&page=' + str(page)
                print(url_)

                user, proxy, cookies = get_cookie()
                print('step4本次代理：{}'.format(proxy))
                self.session.headers['user-agent'] = user_agent()
                self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
                try:
                    # 订购
                    uri = 'https://x.xiaoman.cn/api/account-write/company-purchase?id={}'.format(hashid)
                    self.session.get(url=uri, proxies={'http': proxy})
                    # 正式请求
                    response = self.session.get(url=url_, proxies={'http': proxy}).json()
                    print(url_)
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
                    print(hashid)

                    emails = response['data']['emails']
                    if len(emails) == 0:
                        print('数据已获取完成...')
                        break
                    for email in emails:
                        line = [
                            hashid,
                            self.res(email['first_name']) if email['first_name'] != None else '' + ' ' + self.res(email['last_name']) if email['last_name'] != None else '',
                            self.res(email['position']) if email['position'] != None else "",
                            self.res(email['id']),
                            self.res(email['sources'][0]['uri']) if 0 < len(email['sources']) else '',
                            # time.strftime('%Y-%m-%d %H:%M', time.localtime()),
                        ]
                        print(line)
                        sql = "insert into cont values ( '{0[0]}', '{0[1]}', '{0[2]}', '{0[3]}', '{0[4]}', now())".format(line)
                        print('insert into cont:')
                        self.write2sql(sql)

                except:
                    self.errorlog += '{}-{}&'.format(hashid, traceback.format_exc())
                    # print(traceback.format_exc())
                    # print('{}获取失败...\n'.format(hashid))
                time.sleep(2)
            else:
                return

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
        if not os.path.exists("log/step4"):
            os.mkdir("log/step4")
        with open('log/step4/{}.txt'.format(name), 'a', encoding='utf-8') as w:
            w.write(self.errorlog)


def step4(hashids, siccode, allpage):
    print(hashids, siccode, allpage)
    sp = Spider()
    flag = False

    print('step4 start...')
    if str(allpage) >= sp.config.get('allpage4'):
        print('加载进度...')
        for hi in hashids:
            sp.get_data(hi[0], siccode, allpage)
        if sp.errorlog != '':
            sp.write2log(hashids[0][0])
        sp.config.set('hashid4', '')
        sp.config.set('page4', '1')
        sp.config.set('allpage4', str(allpage+1))
    else:
        print('本页内容已抓取！')
    print('step4 stop...')


if __name__ == '__main__':
    pass
# _*_ coding:utf-8 _*_
#created on 2018/6/27 20:09
import requests
import csv
import time
import os
import json
import traceback
from login1 import login
from Util.Config import GetConfig
from Util.tools import user_agent, XiaoManException
from Util.tools import get_cookie
from Util.tools import remove_cookie

'''
    公司商标
'''


class Spider():
    def __init__(self):
        self.config = GetConfig()
        self.session = requests.Session()
        self.session.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'origin': 'https://x.xiaoman.cn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.url1 = 'https://x.xiaoman.cn/api/company-read/profile-trademarks?id='
        self.errorlog = ''

    def get_data(self,hashid):
        url = self.url1 + hashid
        # print( '\n', hashid)
        print(url)

        user, proxy, cookies = get_cookie()
        print('step5本次代理：{}'.format(proxy))
        self.session.headers['user-agent'] = user_agent()
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        try:
            response = self.session.get(url=url, proxies={'http': proxy}).json()
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

            for data in response['data']:
                if ('jpg' in data['imageId'] or 'png' in data['imageUrl']) and data['imageUrl'] != None:
                    self.get_img(hashid, data['imageId'].replace('/', ''), data['imageUrl'])

        except:
            pass
            # self.errorlog += '{}-{}&'.format(hashid, traceback.format_exc())
            # print(traceback.format_exc())
            # print(hashid + '获取失败...\n')

    def get_img(self, hashid, name, url):
        if not os.path.exists("img"):
            os.mkdir("img")
        if not os.path.exists("img/" + hashid):
            os.mkdir("img/" + hashid)
        with open('img/' + hashid + '/' + name, 'wb') as w:
            print(url)
            proxy = self.get_proxy()
            print('step5下载图片,本次代理：{}'.format(proxy))
            try:
                response = self.session.get(url=url)
                w.write(response.content)
                print(hashid + '/' + name + '下载成功...')
            except Exception as e:
                self.errorlog += '{}-{}-{}&'.format(hashid, name, traceback.format_exc())
                # print(traceback.format_exc())
                # print('{}-{}获取失败...\n'.format(hashid, name))

    def write2log(self, name):
        if not os.path.exists("log"):
            os.mkdir("log")
        if not os.path.exists("log/step5"):
            os.mkdir("log/step5")
        with open('log/step5/{}.txt'.format(name), 'a', encoding='utf-8') as w:
            w.write(self.errorlog)


def step5(hashids, siccode, allpage):
    sp = Spider()
    flag = False
    print('step5 start...')
    if str(allpage) >= sp.config.get('allpage5'):
        print('加载进度...')
        for hi in hashids:
            if hi == sp.config.get('hashid5'):
                flag = True
            if sp.config.get('hashid5') == '':
                flag = True
            if flag:
                print('休眠{}秒'.format(sp.config.get('wait')))
                time.sleep(int(sp.config.get('wait')))
                print('\n第{}类，第{}页'.format(siccode, allpage))
                sp.config.set('hashid5', hi[0])
                sp.get_data(hi[0])
        if sp.errorlog != '':
            sp.write2log(hashids[0][0])
        sp.config.set('hashid5', '')
        sp.config.set('allpage5', str(allpage+1))
    else:
        print('本页内容已抓取！')
    print('step5 stop...')


if __name__ == '__main__':
    pass
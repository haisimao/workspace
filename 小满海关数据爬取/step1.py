# _*_ coding:utf-8 _*_
# created on 2018/6/23 17:53
import requests
import csv
import time
import os
import json
import traceback
from multiprocessing import Process
from Util.Config import GetConfig
from Util.tools import user_agent, XiaoManException
from Util.tools import get_cookie
from Util.tools import remove_cookie

from login1 import login
from step2 import step2
from step3 import step3
from step4 import step4
from step5 import step5

'''
    获取hashid
'''


class Spider():
    def __init__(self):
        self.session = requests.Session()   # 用于维持会话
        self.session.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'origin': 'https://x.xiaoman.cn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }

        self.url1 = 'https://x.xiaoman.cn/api/company-read/mining-list?industryType=sic'
        self.params = {
            'page_size': 25,
            'sicCode': '01000000,01100000,01110000,01120000,01150000,01160000,01190000,01190100,01190101,01190102,01190103,01190104,01190105,01190200,01190201,01190202,01190203,01190300,01190301,01190302,01190303,01190400,01190401,01190402,01190403,01190404,01199900,01199901,01300000,01310000,01319900,01319901,01320000,01330000,01339900,01339901,01339902,01340000,01390000,01390100,01390101,01390102,01390103,01390104,01390105,01390200,01390201,01390202,01399900,01399901,01399902,01399903,01399904,01399905,01399906,01600000,01610000,01610100,01610101,01610102,01610103,01610104,01610200,01610201,01610202,01610203,01610204,01610300,01610301,01610302,01610303,01610400,01610401,01610402,01610403,01610404,01610405,01610406,01610407,01610408,01610409,01610410,01610411,01619900,01619901,01619902,01619903,01619904,01619905,01619906,01619907,01619908,01619909,01700000,01710000,01719900,01719901,01719902,01719903,01719904,01719905,01719906,01719907,01719908,01719909,01720000,01730000,01739900,01739901,01739902,01739903,01739904,01739905,01739906,01739907,01739908,01740000,01749900,01749901,01749902,01749903,01749904,01749905,01749906,01750000,01759900,01759901,01759902,01759903,01759904,01759905,01759906,01759907,01759908,01759909,01759910,01759911,01790000,01799900,01799901,01799902,01799903,01799904,01799905,01799906,01799907,01799908,01799909,01799910,01799911,01799912,01799913,01800000,01810000,01810100,01810101,01810102,01810103,01810104,01810105,01810106,01810107,01810200,01810201,01810202,01810203,01810204,01810300,01810301,01810302,01810303,01819900,01819901,01819902,01820000,01820100,01820101,01820102,01820103,01820104,01820105,01820106,01829900,01829901,01829902,01829903,01900000,01910000,02000000,02100000,02110000,02120000,02130000,02139900,02139901,02140000,02140100,02140101,02140102,02140103,02140200,02140201,02140202,02140203,02140204,02190000,02400000,02410000,02419900,02419901,02419902,02500000,02510000,02519900,02519901,02519902,02519903,02519904,02519905,02520000,02529900,02529901,02530000,02539900,02539901,02539902,02540000,02549900,02549901,02590000,02599900,02599901,02599902,02599903,02599904,02599905,02599906,02700000,02710000,02719900,02719901,02719902,02719903,02719904,02719905,02720000,02729900,02729901,02729902,02729903,02729904,02729905,02730000,02730100,02730101,02730102,02730103,02730104,02730105,02730200,02730201,02730202,02790000,02790100,02790101,02790102,02790200,02790201,02790300,02790301,02790302,02790303,02790400,02790401,02790402,02790403,02799900,02799901,02799902,02799903,02900000,02910000,02919900,02919901,02919902,07000000,07100000,07110000,07119900,07119901,07119902,07119903,07119904,07119905,07119906,07119907,07200000,07210000,07210100,07210101,07210102,07210103,07210104,07210105,07210200,07210201,07210202,07210300,07210301,07210302,07210303,07210304,07210400,07210401,07210402,07210403,07210404,07210405,07210406,07210407,07210408,07210409,07210410,07219900,07219901,07219902,07220000,07220100,07220101,07220102,07220103,07220104,07220105,07220106,07220200,07220201,07220202,07220203,07220204,07220300,07220301,07220302,07220303,07220304,07220305,07220306,07229900,07229901,07229902,07230000,07230100,07230101,07230102,07230103,07230104,07230105,07230106,07230107,07230108,07230109,07230200,07230201,07230202,07230203,07230204,07230205,07230206,07230207,07230208,07230300,07230301,07230302,07230303,07230304,07230305,07230306,07230307,07230308,07230400,07230401,07230402,07230403,07230404,07230405,07230406,07230500,07230501,07230502,07230503,07230504,07230505,07239900,07239901,07239902,07239903,07240000,07249900,07249901,07400000,07410000,07419900,07419901,07419902,07420000,07429900,07429901,07429902,07500000,07510000,07510100,07510101,07510102,07510200,07510201,07510202,07510300,07510301,07510302,07510400,07510401,07510402,07510403,07519900,07519901,07519902,07519903,07519904,07519905,07520000,07520100,07520101,07520102,07520103,07520104,07520200,07520201,07520202,07520203,07520204,07520300,07520301,07520302,07520303,07529900,07529901,07529902,07529903,07600000,07610000,07619900,07619901,07620000,07629900,07629901,07629902,07629903,07800000,07810000,07810100,07810101,07810102,07810200,07810201,07810202,07810203,07820000,07820100,07820101,07820102,07820200,07820201,07820202,07820203,07820204,07820205,07820206,07820207,07820208,07820209,07820210,07829900,07829901,07829902,07829903,07830000,07830100,07830101,07830102,07830103,07830104,07830105,07830200,07830201,07830202,07830203,07830204,07839900,07839901,07839902,07839903,07839904'
        }

        self.errorlog = ''
        '''(01/02/07/09/21/22/23/24/25/26/27/30/31/32/33/34/35/36/37/48/49/50/51/52/53/54/55/57/ 59)'''

    def get_data(self, siccode, page):
        params = self.params
        params['page'] = page
        user, proxy, cookies = get_cookie()
        print('本次代理：{}'.format(proxy))
        self.session.headers['user-agent'] = user_agent()   # 设置会话的头信息
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)  # 将字典转换成cookiejar,然后放在会话中
        try:
            response = self.session.post(url=self.url1, data=params, proxies={'http': proxy}).json()
            print(response)

            if response['code'] == -10005:
                print('身份信息已过期！')
                remove_cookie(user)
                self.get_data(siccode, page)
                raise XiaoManException('cookies已失效, 请更换账号登陆')
                return

            if response['code'] == -10002:
                print('身份信息已过期！')
                remove_cookie(user)
                self.get_data(siccode, page)
                return

            if response['msg'] != 'success':
                time.sleep(10)
                self.get_data(siccode, page)
                return

            if response['status'] == -1:
                print('获取完成...')
                return 1
            if 'data' not in response:
                return
            datas = [[x['companyHashId']] for x in response['data']['list']]    # data为companyHashId列表

            # step2(datas)  # 调用第二步
            # step3(datas)  # 调用第三步
            # step4(datas)  # 调用第四步
            # step5(datas)  # 调用第五步

            print(len(datas))

            p_list = list()                                                 # siccode:当前爬取的类    page:当前爬取页数
            p2 = Process(target=step2(datas, siccode, page), name='step2')  # 调用第二步
            p_list.append(p2)
            p3 = Process(target=step3(datas, siccode, page), name='step3')  # 调用第三步
            p_list.append(p3)
            p4 = Process(target=step4(datas, siccode, page), name='step4')  # 调用第四步
            p_list.append(p4)
            p5 = Process(target=step5(datas, siccode, page), name='step5')  # 调用第五步
            p_list.append(p5)

            for p in p_list:
                p.daemon = True
                p.start()

            for p in p_list:
                p.join()

        except:
            # traceback.print_exc()  # 直接打印出来
            # traceback.print_exc(file=open('tb.txt', 'w+')) # 写到文件
            # print(traceback.format_exc())   # 返回字符串
            self.errorlog += '{}-{}-{}&'.format(sic, page, traceback.format_exc())
            print('{}-第{}页失败...'.format(traceback.format_exc(), page))
            print('休眠10min后重试')
            time.sleep(60*10)
            self.get_data(siccode, page)

    def write2log(self, name):
        if not os.path.exists("log"):
            os.mkdir("log")
        if not os.path.exists("log/step1"):
            os.mkdir("log/step1")
        with open('log/step1/{}.txt'.format(name), 'a', encoding='utf-8', newline='') as w:
            w.write(self.errorlog)


if __name__ == '__main__':
    sp = Spider()
    flag = False
    with open('Util/SicCode.json', 'r', encoding='utf-8') as w:
        sicCode = json.loads(w.read()) # 转换成列表

    for sic in range(0, 29):
        sp.params['sicCode'] = sicCode[sic]
        sp.errorlog = ''
        for page in range(1, 401):
            config = GetConfig()
            if str(sic) == config.get('sic') and str(page) == config.get('page1'):
                flag = True
            if config.get('sic') == '':
                flag = True
            if flag:
                config.set('sic', str(sic))
                config.set('page1', str(page))
                print('第{}类，第{}页，'.format(sicCode[sic][:8], page) + sicCode[sic])
                if sp.get_data(sicCode[sic][:8], page) == 1:
                    break
                time.sleep(0.5)
            else:
                continue
            if sp.errorlog != '':
                sp.write2log(sicCode[sic][:8])
        if flag:
            config.set('allpage2', '1')
            config.set('allpage3', '1')
            config.set('allpage5', '1')
            config.set('allpage5', '1')
    config.set('sic', '')
    config.set('page1', '1')
    config.set('allpage2', '1')
    config.set('hashid2', '')
    config.set('hashid3', '')
    config.set('page3', '1')
    config.set('allpage3', '1')
    config.set('hashid4', '')
    config.set('page4', '1')
    config.set('allpage4', '1')
    config.set('hashid5', '')
    config.set('allpage5', '1')
    print('爬取完成！！！！！')
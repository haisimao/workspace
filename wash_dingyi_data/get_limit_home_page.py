import datetime
from threading import Thread

import pymysql


balalaba = pymysql.connect(
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

with balalaba.cursor() as cursor:
    '''

    '''
    # comp_no 记录 1091494  ,   2731521   , 1311367
    cursor.execute('select home_page from comps where comp_no > 1311367 and comp_no < 2731521; ')
    # cursor.execute('select home_page from comps where createdAt > "2019-01-14" and createdAt < "2019-01-14" ; ')
    res = cursor.fetchall()


def main(res_, i):
    for url in res_:
        if url.get('home_page'):
            with open(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_2019-01-18\comp{}_2019_01_18.txt'.format(i), 'a+', encoding='utf-8') as file:
                file.write(url.get('home_page').strip() + '\n')


if __name__ == '__main__':
    for i in range(0, 50, 2):
        res_ = res[i*10000:(i+2)*10000]
        if res_:
            print('单次插入完成,{}.时间{}'.format(i, datetime.datetime.now()))
            # main(res_, i)
            p1 = Thread(target=main, args=(res_, i))
            p1.start()


import threading

import pymysql
# 创建{'comp_name': 'hashid'} 的字典
balalaba = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        password="zx123ZX!@#",
        database='balalaba',
        use_unicode=True,
        charset="utf8mb4",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


if __name__ == '__main__':
    sem_pool = threading.Semaphore(50)  # 限制线程的最大数量为100个
    try:
        while True:
            with balalaba.cursor() as cursor_balalaba:
                cursor_balalaba.execute(
                    '''select hashid from conts where cont_url = '企业邮箱' GROUP BY hashid HAVING count(*) > 20;''')
                results = cursor_balalaba.fetchall()
                if len(results) == 0:
                    break
                for result in results:
                    hashid = result.get('hashid')
                    cursor_balalaba.execute(
                        '''delete from conts where hashid = '{}' and cont_url = '企业邮箱' ORDER BY id desc limit 1 ;'''.format(
                            hashid))
    except:
        print('1, ')



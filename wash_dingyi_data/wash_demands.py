import threading

import pymysql

xiaoman = pymysql.connect(
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

counter_lock = threading.Lock()


def wash_main():
        with balalaba.cursor() as cursor_xiaoman:
            cursor_xiaoman.execute('''select comp_name from demands where comp_name in (select comp_name from comps) group by(comp_name);''')
            results = cursor_xiaoman.fetchall()
            print(len(results))
            for comp_name_dict in results:
                comp_name = comp_name_dict.get('comp_name')
                try:
                    cursor_xiaoman.execute('''select hashid from comps where comp_name = "{}";'''.format(comp_name))
                    hashid = cursor_xiaoman.fetchone().get('hashid')
                    cursor_xiaoman.execute('''update low_priority demands set hashid=%s where comp_name=%s''', (hashid, comp_name))
                    print('输出{}....{}......{}'.format(hashid, comp_name, results.index(comp_name_dict)))
                except:
                    print('dddd')
                    print('输出{}'.format(comp_name))


if __name__ == '__main__':
    wash_main()

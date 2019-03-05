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
with balalaba.cursor() as cursor_balalaba:
    cursor_balalaba.execute('''select home_page, hashid from {} where length(home_page) > 1;'''.format('comps'))
    result = cursor_balalaba.fetchall()
    print(len(result))
comp_name_hashid_dict = {}
for res in result:
    home_page = res['home_page'].replace('http://www.', '')
    home_page = home_page.replace('www.', '')
    home_page = home_page.replace('http://www.', '')
    comp_name_hashid_dict[res['hashid']] = home_page

contName_hashid_dict = {}

with balalaba.cursor() as cursor_balalaba:
    cursor_balalaba.execute('''select hashid from conts GROUP BY hashid HAVING count(hashid) > 20  order by count(hashid);''')
    results = cursor_balalaba.fetchall()
    print(len(results))
    for result in results:
        hashid = result.get('hashid')
        cursor_balalaba.execute('''select cont_email from conts where hashid = '{}'; '''.format(hashid))
        cont_emails = cursor_balalaba.fetchall()
        contName_hashid_dict[hashid] = [res.get('cont_email') for res in cont_emails]


contEmails = []
for hashid in contName_hashid_dict.keys():
    homePage = comp_name_hashid_dict.get(hashid)
    cont_Email_list = contName_hashid_dict.get(hashid)
    for contEmail in cont_Email_list:
        if homePage and contEmail:
            if homePage in contEmail:
                contEmails.append(contEmail)

print(len(contEmails))


def update_url(Emails):
    with balalaba.cursor() as cursor_balalaba:
        sql = '''update conts set cont_url = '企业邮箱' where cont_email = 'awarnecke@azfamily.com'  '''
        for email in Emails:
            line = " or cont_email = '{}' ".format(email)
            sql = sql + line
        sql = sql + ';'
        cursor_balalaba.execute(sql)


if __name__ == '__main__':
    sem_pool = threading.Semaphore(50)  # 限制线程的最大数量为100个
    num = len(contEmails)
    page = 20000
    # 190000
    j = 9
    try:
        my_data = contEmails[j * page:(j + 1) * page]
        with balalaba.cursor() as cursor_balalaba:
            for email in my_data:
                cursor_balalaba.execute(
                    '''update conts set cont_url = '{}' where cont_email = '{}' ;'''.format('企业邮箱', email))
    except:
        print('1, ')



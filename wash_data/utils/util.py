import pymysql


def comps_hashid():
    balalaba = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        password="zx123ZX!@#",
        database='to_balalaba',
        use_unicode=True,
        charset="utf8mb4",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
    with balalaba.cursor() as cursor_balalaba:
        cursor_balalaba.execute('''select comp_name, hashid from {};'''.format('comps'))
        result = cursor_balalaba.fetchall()
        print(len(result))
    comp_name_hashid_dict = {}
    for res in result:
        comp_name_hashid_dict[res['comp_name']] = res['hashid']

    return comp_name_hashid_dict


if __name__ == '__main__':
    pass
    # import pandas as pd
    import json
    comp_hashid = comps_hashid()
    with open(r'./comp_hashid.json', 'w+') as f:
        json.dump(comp_hashid, f)
    # print(encrypt_md5('fafafgggggf'))
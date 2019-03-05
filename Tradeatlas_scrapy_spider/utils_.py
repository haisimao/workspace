import pymysql
from selenium import webdriver
import string
import zipfile

def create_proxy_auth_extension(proxy_host, proxy_port,
                                proxy_username, proxy_password,
                                scheme='http', plugin_path=None):
    if plugin_path is None:
        plugin_path = r'D:/{}_{}@http-dyn.abuyun.com_9020.zip'.format(proxy_username, proxy_password)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Abuyun Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


class TradeatlasException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


# MD5加密 #
import hashlib


def encrypt_md5(str=''):
    md = hashlib.md5()  # 创建md5对象
    md.update(str.encode(encoding='utf-8'))  # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    return md.hexdigest()[9:25]  # 加密


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
    # import json
    # comp_hashid = comps_hashid()
    # with open(r'./comp_hashid.json', 'w+') as f:
    #     json.dump(comp_hashid, f)
    # print(encrypt_md5('fafafgggggf'))



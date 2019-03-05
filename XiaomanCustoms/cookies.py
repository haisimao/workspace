import json
import logging
import time
import requests
import redis
import string
import zipfile
import re
from selenium import webdriver
from .settings import REDIS_URL


# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"

logger = logging.getLogger(__name__)

# 使用REDIS_URL链接Redis数据库，decode_response=True保持写入的键值对为str类型，否则为byte类型
# xiaoman
reds = redis.Redis.from_url(REDIS_URL, db=2, decode_responses=True)
# weixin
# reds = redis.Redis.from_url(REDIS_URL, db=3, decode_responses=True)


class CookieTool(object):
    def __init__(self):
        self.login_url = "https://login.xiaoman.cn/login"

    # 获取Cookie
    def get_cookie(self, user, password):
        chrome_options = webdriver.ChromeOptions()

        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # 使用代理
        proxy_auth_plugin_path = self.create_proxy_auth_extension(
            proxy_host=proxyHost,
            proxy_port=proxyPort,
            proxy_username=proxyUser,
            proxy_password=proxyPass)

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_extension(proxy_auth_plugin_path)

        flag = False
        while 1:
            try:
                browser = webdriver.Chrome(chrome_options=chrome_options)
                # browser.get("https://login.xiaoman.cn/login")
                browser.get("https://login.xiaoman.cn/login?system_id=discovery&return_url=https%3A%2F%2Fx.xiaoman.cn%2F")
                # browser.get('https://mp.weixin.qq.com/')
                time.sleep(1)
                # xiaoman
                browser.find_element_by_id("email").send_keys(user)
                time.sleep(1)
                browser.find_element_by_id("password").send_keys(password)
                time.sleep(1)
                # weixin
                # browser.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input')
                # browser.find_element_by_name('account').send_keys()
                # browser.find_element_by_name('password').send_keys()
                if flag:
                    # xiaoman
                    browser.find_element_by_id("remember").click()
                    # weixin
                    # browser.find_element_by_class_name('icon_checkbox').click()
                # xiaoman
                browser.find_element_by_xpath("//button[@type = 'submit']").click()
                # weixin
                # browser.find_element_by_class_name('btn_login').click()
                time.sleep(2)

                cookies = {}
                cookies_items = browser.get_cookies()
                for cookies_item in cookies_items:
                    cookies[cookies_item['name']] = cookies_item['value']
                # cookies = [item["name"] + ":" + item["value"] for item in browser.get_cookies()]
                # cookies_map = {}
                # for item in cookies:
                #     key_value = item.split(":")
                #     cookies_map[key_value[0]] = key_value[1]
                if cookies != {}:
                    print(cookies)
                    browser.close()
                    browser.quit()
                    break
                # if cookies_map != {}:
                #     print(cookies_map)
                #     browser.close()
                #     browser.quit()
                #     break
            except:
                browser.close()
                browser.quit()
                print("本次登陆失败，正在重新登陆！")
        return json.dumps(cookies)

    # 写入Redis数据库
    def init_cookie(self, red, spider_name):
        redkeys = reds.keys()
        for user in redkeys:
            password = reds.get(user)
            if red.get("%s:Cookies:%s--%s" % (spider_name, user, password)) is None:
                cookie = self.get_cookie(user, password)
                red.set("%s:Cookies:%s--%s" % (spider_name, user, password), cookie)

    # 删除Cookie
    def remove_cookie(self, red, spider_name, user, password):
        red.delete("%s:Cookies:%s--%s" % (spider_name, user, password))

    # 更新Cookie
    def update_cookie(self, red, spider_name, user, password):
        self.remove_cookie(red, spider_name, user, password)
        self.init_cookie(red, spider_name)

    def create_proxy_auth_extension(self, proxy_host, proxy_port,
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

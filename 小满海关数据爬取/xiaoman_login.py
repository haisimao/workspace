# _*_ coding:utf-8 _*_
#created on 2018/6/13 21:55
from selenium import webdriver
import time
import requests
import random


class Spider(object):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()

        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # 使用代理
        self.proxy = self.get_proxy()
        print('本次代理：{}'.format(self.proxy))
        chrome_options.add_argument('--proxy-server=http://{}'.format(self.proxy))
        self.web = webdriver.Chrome(chrome_options=chrome_options)  # 创建实例

    def get_login(self, user, pwd):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.action_chains import ActionChains
        wait = WebDriverWait(self.web, 50)
        # self.web.maximize_window()
        try:
            self.web.get('https://login.xiaoman.cn/login?system_id=discovery&return_url=https%3A%2F%2Fx.xiaoman.cn%2F')
            # time.sleep(2)
            # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login')))
            # li = self.web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[6]')
            # a = self.web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[6]/a')
            # # self.web.execute_script("arguments[0].scrollIntoView();", li)
            # ActionChains(self.web).move_to_element(li).click(li).perform()
            # self.web.find_element_by_xpath('/ html / body / div[2] / div / div[3] / a[3]').click()
            # time.sleep(3)
            # self.web.switch_to_window(self.web.window_handles[1])
            # username = self.web.find_element_by_id('email')
            # username.send_keys(user)
            # password = self.web.find_element_by_id('password')
            # password.send_keys(pwd)
            # time.sleep(1)
            # flag = 0
            # # flag = random.randint(0, 1)  # 随机1-7
            # if flag == 1:
            #     remember = self.web.find_element_by_id('remember')
            #     remember.click()
            #     time.sleep(1)
            # login = self.web.find_element_by_xpath("//button[@type = 'submit']")
            # login.click()
            time.sleep(4)
            username = self.web.find_element_by_id('email')
            username.send_keys(user)

            password = self.web.find_element_by_id('password')
            password.send_keys(pwd)

            time.sleep(random.randint(1, 3))
            flag = 0
            # flag = random.randint(0, 1)  # 随机1-7
            if flag == 1:
                remember = self.web.find_element_by_id('remember')
                remember.click()
                time.sleep(1)
            login = self.web.find_element_by_xpath("//button[@type = 'submit']")
            login.click()
        except:
            self.web.quit()
            chrome_options = webdriver.ChromeOptions()

            # 禁止图片加载
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)

            # 使用代理
            self.proxy = self.get_proxy()
            print('本次代理：{}'.format(self.proxy))
            chrome_options.add_argument('--proxy-server=http://{}'.format(self.proxy))
            self.web = webdriver.Chrome(chrome_options=chrome_options)  # 创建实例
            return self.get_login(user, pwd)

        time.sleep(4)
        print(self.web.get_cookies())
        cookie = [item["name"] + ":" + item["value"] for item in self.web.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        cook_map = {}
        for item in cookie:
            str = item.split(':')
            cook_map[str[0]] = str[1]

        print('cookies：', cook_map)
        if 'clientId' not in cook_map:
            print('登入失败！')
            self.web.close()
            return self.proxy, {}
        print('登入成功...')
        self.web.quit()
        return self.proxy, cook_map

    def get_proxy(self):
        return requests.get(url="http://api.http.niumoip.com/v1/http/ip/get?p_id=192&s_id=1&u=VjVXNQ4!AGIBOwEvCUcBPg8gVmoCOgEQBFNXU1NV&number=1&port=1&type=2&map=1&pro=0&city=0&pb=1&mr=3&cs=1").text


def login(user, pwd):
    sp = Spider()
    print('尝试登入 user：{}\tpwd：{}'.format(user, pwd))
    return sp.get_login(user, pwd)   #返回cookies


if __name__ == '__main__':
    # for i in range(50):
    # sp = Spider()
    # print(sp.get_login('1571427194@qq.com', 'Yq201808'))
    print(int(round(time.time() * 1000)))
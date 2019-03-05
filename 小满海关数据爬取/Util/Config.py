# _*_ coding:utf-8 _*_
# created on 2018/7/18 13:07
from configparser import ConfigParser  # py3
# -*- coding: utf-8 -*-


class GetConfig(object):
    def __init__(self):
        self.config = ConfigParser()  # 直接读取ini文件内容，初始化config实例（建立一个空的数据集实例）
        self.config.read('./Config.ini')  # 通过load文件filename来初始化config实例
        # self.config.write(open('../Config.ini', 'w'))  # 保存配置

    def get(self, params):
        # print('get到：{}'.format(self.config.get('XIAOMAN', params)))  # 获得指定section中的key的value
        return self.config.get('XIAOMAN', params)

    def set(self, params, value):
        self.config.set('XIAOMAN', params, value)
        self.config.write(open('./Config.ini', 'w'))  # 保存配置
        print('{}已更新为：{}'.format(params, value))

    def setPage(self, step, page):
        self.config.set('PAGE', step, str(page))
        self.config.write(open('./Config.ini', 'w'))  # 保存配置
        print('{}分类page已更新为：{}'.format(step, page))


#
#
#     @LazyProperty
#     def proxy_getter_functions(self):
#         return self.config_file.options('ProxyGetter')

if __name__ == '__main__':
    gc = GetConfig()
    print(gc.getsic())
    gc.setsic(1)
    pass
    # print(config.get('STEP1', 'sic'))  # 获得指定section中的key的value
    # config.get(section, key) # 获得指定section中的key的value
    # config.getint(section, key)

    # config.getfloat(section, key)
    # config.getboolean(section, key)
    # config.set(section, key, value)在指定section中，添加一对key - value键值对，没有section时返回

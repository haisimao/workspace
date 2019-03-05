"""
MySQl连接类
"""
from scrapy.utils.project import get_project_settings
import pymysql
import logging
from XiaomanCustoms.settings import MYSQL_LOCALHOST

settings = get_project_settings()


class MySQLConnection(object):
    """MySQL连接类"""

    def __init__(self, settings):
        self.conn = pymysql.connect(**MYSQL_LOCALHOST['mysql'])
        self.cursor = self.conn.cursor()

    def _check(self):
        """检查连接"""
        try:
            self.conn.ping()
        except:
            # log.msg("MySQL断开连接，重新连接。", level=log.WARNING)
            logging.WARNING("MySQL断开连接，重新连接。")
            self.conn.close()
            self.conn = pymysql.connect(**MYSQL_LOCALHOST['mysql'])
            self.cursor = self.conn.cursor()

    def __getattribute__(self, attr):
        try:
            # conn这个名字是在__init__中固定的，请勿乱修改
            # conn这个判断一定不能省略，否则会造成无限递归！
            if 'conn' != attr:
                super(MySQLConnection, self).__getattribute__('_check')()
            return super(MySQLConnection, self).__getattribute__(attr)
        except KeyError:
            return '不正确的MySQL属性！'
# -*- coding: utf-8 -*-

# Scrapy settings for Bizvibe_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import time
from urllib.parse import quote

BOT_NAME = 'Bizvibe_scrapy'

SPIDER_MODULES = ['Bizvibe_scrapy.spiders']
NEWSPIDER_MODULE = 'Bizvibe_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Bizvibe_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Bizvibe_scrapy.middlewares.BizvibeScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'Bizvibe_scrapy.middlewares.RandUserAgent': 543,
    'Bizvibe_scrapy.middlewares.RandIPROXY': 544,
    # 'Bizvibe_scrapy.middlewares.DLMiddleware': 545,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Bizvibe_scrapy.pipelines.BizvibePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 配置日志信息
import datetime
today = datetime.datetime.now()
LOG_LEVEL = 'INFO'
LOG_FILE = './log/bizvibe_scrapy_{}_{}_{}.txt'.format(today.year, today.month, today.day)

# CLOSESPIDER_TIMEOUT = 3500  # 设置爬虫定时关闭时间

MAX_PAGE = 100

SELENIUM_TIMEOUT = 20

PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

MONGO_URI = 'localhost'

MONGODB_PORT = 27017

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"


COOKIES_DICT = \
{'srch_countrycode': 'worldwide', 'BZVAUTH': '4770602676', '_ga': 'GA1.2.1849756302.1550830313', '_gat': '1',
 '_gid': 'GA1.2.1477537488.1550830313', '_pk_ses.8.9a72': '*', 'PHPSESSID': 'hku1pt4qv4c8pvf7kcrpfo1fv3', 'verifyCookie': 'Y',
 'sessionid': 'hku1pt4qv4c8pvf7kcrpfo1fv3', 'BZVU': '93114', 'authsession': '93114~zNaODZKRDJUivNBPJi7OJW2qOx4~SUNNY~~Evans Toy Store~10038174~A~evanstoys.com~eHh4eHgyOEBxcS5jb20=',
 '_pk_id.8.9a72': '1d7f2f8575cf2679.1550830315.1.1550830330.1550830315.', 'srch_country': 'Worldwide'}




# 配置爬取参数
SICCODE = '390000'
#    Textiles
CATEGORY = ['1554']
CATEGORY_SICCODE = {
# '1571'	:'220000',  1
# '1592':'280000',1
# '1184':  '310000',1
# '10017':'500000',1
# '1274'	:'500000',1
# '1262'	:'500000',1
# '1599'	:'230000',1
# '1189'	:'230000',1
# '1234':  '230000',1
# '1437':  '230000',1
# '1450':  '230000',1
# '1443':  '220000',1
# '1493':  '230000',1
# '1409':  '310000',1
# '1555': '390000',1
# '1480':	'360000',1
# '1219':	'250000',1
'10011':'250000',
# '1613':	'250000',
# '1612':	'250000',
# '1471':	'250000',
# '1515':	'250000',
# '1220':	'250000',
# '1109':	'250000',
# '1524':	'250000',
# '1467':	'250000',

}
URL = 'https://www.bizvibe.com/worldwide/agriculture?rd=mfgimlagffociojh_='
SEARCH_PAGE = 0

# -*- coding: utf-8 -*-

# Scrapy settings for Bizvibe_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

BOT_NAME = 'Bizvibe_scrapy'

SPIDER_MODULES = ['Bizvibe_scrapy.spiders']
NEWSPIDER_MODULE = 'Bizvibe_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Bizvibe_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 6
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
    # 'Bizvibe_scrapy.middlewares.RandIPROXY': 544,
    'Bizvibe_scrapy.middlewares.DLMiddleware': 542,

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


CLOSESPIDER_TIMEOUT = 3500  # 设置爬虫定时关闭时间

MAX_PAGE = 100

SELENIUM_TIMEOUT = 3600

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
    [{'domain': 'www.bizvibe.com', 'expiry': 1550456015, 'httpOnly': False, 'name': 'srch_countrycode', 'path': '/',
      'secure': False, 'value': 'worldwide'},
     {'domain': 'www.bizvibe.com', 'expiry': 1551147206.33443, 'httpOnly': False, 'name': 'BZVAUTH', 'path': '/',
      'secure': False, 'value': '4573710414'},
     {'domain': '.bizvibe.com', 'expiry': 1612923211, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False,
      'value': 'GA1.2.988373931.1549851194'},
     {'domain': '.bizvibe.com', 'expiry': 1549851253, 'httpOnly': False, 'name': '_gat', 'path': '/', 'secure': False,
      'value': '1'},
     {'domain': '.bizvibe.com', 'expiry': 1549937611, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False,
      'value': 'GA1.2.1465343640.1549851194'},
     {'domain': 'www.bizvibe.com', 'expiry': 1549853011, 'httpOnly': False, 'name': '_pk_ses.8.9a72', 'path': '/',
      'secure': False, 'value': '*'},
     {'domain': 'www.bizvibe.com', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'secure': False,
      'value': '463ofqpmoah2h488ddl3271l66'},
     {'domain': 'www.bizvibe.com', 'expiry': 1552443206, 'httpOnly': False, 'name': 'verifyCookie', 'path': '/',
      'secure': False, 'value': 'Y'},
     {'domain': 'www.bizvibe.com', 'expiry': 1551147206.334404, 'httpOnly': False, 'name': 'sessionid', 'path': '/',
      'secure': False, 'value': '463ofqpmoah2h488ddl3271l66'},
     {'domain': '.www.bizvibe.com', 'expiry': 1551147206.334417, 'httpOnly': True, 'name': 'BZVU', 'path': '/',
      'secure': False, 'value': '89271'},
     {'domain': 'www.bizvibe.com', 'expiry': 1552443206, 'httpOnly': False, 'name': 'authsession', 'path': '/',
      'secure': False,
      'value': '89271~43TdFqvK2Pcg2gOtugvvBmfFL6U~Lilin~~上海钰祺网络科技有限公司~10037557~A~balalaba.com~eHh4eHgzMUBxcS5jb20='},
     {'domain': 'www.bizvibe.com', 'expiry': 1583806395, 'httpOnly': False, 'name': '_pk_id.8.9a72', 'path': '/',
      'secure': False, 'value': '2043b586ce655251.1549851195.1.1549851212.1549851195.'},
     {'domain': 'www.bizvibe.com', 'expiry': 1550456015, 'httpOnly': False, 'name': 'srch_country', 'path': '/',
      'secure': False, 'value': 'Worldwide'}]

# 配置爬取参数
SICCODE = '01800000'
URL = 'https://www.bizvibe.com/worldwide/agriculture?rd=mfgimlagffociojh_='
SEARCH_PAGE = 3

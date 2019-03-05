# -*- coding: utf-8 -*-

# Scrapy settings for Tradeatlas_scrapy_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Tradeatlas_scrapy_spider'

SPIDER_MODULES = ['Tradeatlas_scrapy_spider.spiders']
NEWSPIDER_MODULE = 'Tradeatlas_scrapy_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Tradeatlas_scrapy_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 16

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
#    'Tradeatlas_scrapy_spider.middlewares.TradeatlasScrapySpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Tradeatlas_scrapy_spider.middlewares.RandIPROXY': 543,
   'Tradeatlas_scrapy_spider.middlewares.SetCookies': 544,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Tradeatlas_scrapy_spider.pipelines.TradeatlasPipeline': 300,
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

COOKIES = \
    {
    '__utmz':'262406345.1543825999.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '__utmz':'1.1543825999.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc:262406345',
    ' __utmc':'1',
    '__utma':'262406345.244459286.1543825999.1550050750.1550108537.6',
    '__utma':'1.2001971904.1543825999.1550050750.1550108538.6',
    '__utmb':'262406345.18.10.1550108537',
    '__utmb':'1.18.10.1550108538',
    'tradeatlassession':'eyJpdiI6IkdrOUU3NkhrMWlKUVkxT1BJc1gzenp1bTVGdHZoN1p4bGJHbTNWNVwvOU9NPSIsInZhbHVlIjoiTFwvdW9cL3VVdStlaVVmQ1MzRGtNZFdGTlhBdmQrbGJOSGlsaldRWUpcL2h4UjVsa3d2VXJXK0pNSzl0d21mRmExbDdPWGFCd3BqQ3ZLbEdybHQrMmFDOXc9PSIsIm1hYyI6ImNlOTc4NWM0YzlmMjA0MWEwM2I5MTBkNzc1Y2FlYWVkMDM2NDA4Yzk5Y2IyNzQ5ZDViN2YwMmVmNTFjMTFiYTIifQ%3D%3D',
    'lang_value':'eyJpdiI6IlwvSStwMjRJR1dxVmVaQUdMWWE4ZUJBVkpQSFE4OGJKTkltWGdzTnhmXC9yVT0iLCJ2YWx1ZSI6IkpYdU9qa2o2cTdBdE9YeGFlV3RZMFJIN1V1Rzg0dDR2Rlwvb0ptWmFyXC9maz0iLCJtYWMiOiIxMzQ3MDJlZDYxNzFhMWMyZmIyYjNiMGJkNzlhM2E0MTdlZWY0N2U5Zjc2OTZhMzg0YzU4Yzc2MGZjZDlhOTk4In0%3D',
    }








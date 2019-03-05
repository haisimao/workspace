# -*- coding: utf-8 -*-

# Scrapy settings for alibaba project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime

BOT_NAME = 'alibaba'

SPIDER_MODULES = ['alibaba.spiders']
NEWSPIDER_MODULE = 'alibaba.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'alibaba (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
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
#    'alibaba.middlewares.AlibabaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'alibaba.middlewares.AlibabaDownloaderMiddleware': 543,
    'alibaba.middlewares.SeleniumMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'alibaba.pipelines.AliBaBaTimePipeline': 300,
   'alibaba.pipelines.AliBaBaInsertPipeline': 301,
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

SELENIUM_TIMEOUT = 2000

PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

MONGO_URI = 'localhost'

MONGODB_PORT = 27017

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"





































































COOKIES_DICT = [{'domain': '.alibaba.com', 'httpOnly': True, 'name': 'cookie2', 'path': '/', 'secure': False, 'value': '141b80db9530fadf4108dd9ed579fd1b'}, {'domain': '.alibaba.com', 'expiry': 1537862230.84445, 'httpOnly': False, 'name': '_m_h5_tk', 'path': '/', 'secure': False, 'value': '2e5f4bf8c3916e145626697e5502cbbe_1537266792596'}, {'domain': '.alibaba.com', 'expiry': 3684741075.682659, 'httpOnly': False, 'name': 'xman_us_f', 'path': '/', 'secure': False, 'value': 'x_locale=zh_CN&x_l=1&last_popup_time=1537257430449&x_user=CN|service|fochier|cgs|234644214&no_popup_today=n'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': '_tb_token_', 'path': '/', 'secure': False, 'value': '59356e68ee386'}, {'domain': '.alibaba.com', 'expiry': 1844843823.803878, 'httpOnly': False, 'name': 't', 'path': '/', 'secure': False, 'value': 'a9fe0ece238ec23b9da466facf8ce568'}, {'domain': '.alibaba.com', 'expiry': 3626384459.682565, 'httpOnly': False, 'name': 'ali_apache_id', 'path': '/', 'secure': False, 'value': '182.149.162.151.1537257430423.238260.3'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': 'xman_us_t', 'path': '/', 'secure': False, 'value': 'ctoken=19i9api1fxp8o&l_source=alibaba&x_user=xA7sSc5U+RXkYb1xCD3Az93Lx7W2qrVzbix22Hr83Ls=&x_lid=cn1524443896ownl&sign=y&need_popup=y'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': 'acs_usuc_t', 'path': '/', 'secure': False, 'value': 'acs_rt=0cf8bc3c143c490cacc055c55165c807'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': 'intl_locale', 'path': '/', 'secure': False, 'value': 'zh_CN'}, {'domain': '.alibaba.com', 'expiry': 3684741075.682789, 'httpOnly': True, 'name': 'intl_common_forever', 'path': '/', 'secure': False, 'value': 'DZmUH1pPXfUVGjzMJUXBqcr22URXiYy6Htv3YVjZl4MIOsIui6w+aA=='}, {'domain': '.alibaba.com', 'expiry': 3684741075.682815, 'httpOnly': True, 'name': 'xman_f', 'path': '/', 'secure': False, 'value': '2VdzXdLNqHtpFwEBpZiV+xFRO6h9ALtxUtK5iDhUiMPrDGqSt/QYoItbbgEoriJ0fKaVh/WpNjIGUDPyhbyNwuI9eqsRwubgQLJV5AD0K/QfRO4Pua/VAyTLx3yvNHybYjOZFimIajYRq+0LIA9tPpITF5wN8O45hX5LLyz+d75cmAek3MsGZO5juoYB959AFMIQBtncZUe+0W893PoRzbRraJGk7NLUAtnytIxrsKxm2CkY0s/zTit5Bj5EKL5/nIptDTSzpx07Si8nVqtO0y4MpPpp4cqhB2NGKhXZebnUtd94PCGfC6kRy2x1jh6OunhFMCrqUjrxxEaqkiSPPwTP4GQG84MAjCAcTFxU91tuiNOiebZ2pVBrMGx2U+1y0ZawBcYacC35uqIxgGdt4a3Rxa/IawmmuyBBYy1l+RMieTsCts3Hdw=='}, {'domain': 'www.alibaba.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/', 'secure': False, 'value': '3BD39CE0CE14FE45EADDF9DDD308B24F'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': 'acs_rt', 'path': '/', 'secure': False, 'value': '182.149.162.151.1537257432605.6'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': 'v', 'path': '/', 'secure': False, 'value': '0'}, {'domain': '.alibaba.com', 'expiry': 1537862230.84448, 'httpOnly': False, 'name': '_m_h5_tk_enc', 'path': '/', 'secure': False, 'value': 'c8ef766769a3ceb9844218b8640473e5'}, {'domain': '.alibaba.com', 'expiry': 2167977430, 'httpOnly': False, 'name': 'cna', 'path': '/', 'secure': False, 'value': 'y50nFPg9HWkCAbaVopfr+0iU'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': 'csg', 'path': '/', 'secure': False, 'value': 'eb01d56f'}, {'domain': '.alibaba.com', 'httpOnly': False, 'name': 'ali_apache_tracktmp', 'path': '/', 'secure': False, 'value': 'W_signed=Y'}, {'domain': '.alibaba.com', 'expiry': 3684741080.392263, 'httpOnly': False, 'name': 'ali_apache_track', 'path': '/', 'secure': False, 'value': 'mt=3|ms=|mid=cn1524443896ownl'}, {'domain': '.alibaba.com', 'expiry': 1552809431, 'httpOnly': False, 'name': 'isg', 'path': '/', 'secure': False, 'value': 'BCQkmYJUIzcVCFd7Qfy-Sk-d9SLWFUheNs59Vj5Fvu-y6cSzZs6AtljLrQDUNoB_'}, {'domain': '.alibaba.com', 'httpOnly': True, 'name': 'xman_t', 'path': '/', 'secure': False, 'value': 'eAfPXnUpu1KGpWabZjuh1x+DnpKTpIchGzviWo6GZGlxbiFFfdSaOp8gwzpfmOnNIyapBfOA7Bf7zv0ICAfQOApXPDLeEWPUKObfWmftngdAQiFdkndTHZ0LHEs5jPbWvK5TP+s3x6Akpegb+uQaPWSskfSiN+pNQCRPaESoIreFMf56ROik0VtWzAmG5r2cjlpWsWTSAaDLUphCfKUCCRvXQbRiFYTyG9y6fcZdohOY/z7IFvog1LFd1/gO2g8jOvhKXxdIITy0c8f5xoHSZqGcG9BdJbMRCHTW1DzjuJ2qlkFUvtISFShOBp6qXn1H+9vSj5whe43XDIGieohcxO0xMf3binwDN+wicPsu4looUdz4JdlnCO422Uiup3pWtClEGQ6iPe9ujUJpH8M2h2vVsM9jxzw/vCJAcrEphp9B5l9TnaETKVTTHFy8zyNqwoU1GWmSLDzoiqtkUmsy8IXtzV4bZH3pQT7qFga3DmP43RGyFn1ZkE6+hW8T6LIH3+L2R2y8NCvIeDctXw7MSFQOWGmqum98eS55+ul6vk0jG9i4/zPZe3mA5N1Ii3noUkZDmTK+XqNqVU5xI6ZqnKUA+aDhFbaonJ/K8ZESKk84nQe5OTIy6iDwyE+7EyqPz7YWFp814l2UxbAeJM1/vNFyqinxviUcHcrtMiRSUsn54LHes00Ph5aZOK47w9DcTNFkLk5fgX+gpvrKQdOOaT6de3SYA+ZO'}]

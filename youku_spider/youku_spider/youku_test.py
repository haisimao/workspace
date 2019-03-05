# from fake_useragent import UserAgent
# ua = UserAgent()
# # ua.update()
#
# # attr = getattr(ua, 'chrome')
# print(ua.chrome)


import urllib.parse


a = "http://zh.wikipedia.org/wiki/亚马逊"


print(urllib.parse.quote(a))
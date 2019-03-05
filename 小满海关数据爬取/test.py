from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)
# ua = UserAgent()
# ua.update()
rua = getattr(ua, 'chrome')
print(rua)







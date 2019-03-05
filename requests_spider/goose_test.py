import time

from goose3 import Goose
from goose3.text import StopWordsChinese
# 初始化，设置中文分词
g = Goose({'stopwords_class': StopWordsChinese,
           'browser_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})
# 文章地址
urls = [
    'http://www.dugdalebros.com/',
    'http://www.vernoncounty.org',
    'http://www.seacresthcm.com',
    'http://www.crjustice.org',
    'http://www.dismas.com',
    'http://www.wellsnursing.org',
    'http://www.villa.cdom.org',
    'http://www.wdhospital.com',
    'http://www.matherhospital.org',
]
# 获取文章内容
for url in urls:
    article = g.extract(url=url)
    # 标题
    print('标题：', article.title)
    # 显示正文
    print(article.raw_html)
    print('***********************************************')
    time.sleep(3)
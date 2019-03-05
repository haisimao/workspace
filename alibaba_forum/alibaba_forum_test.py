from datetime import datetime

import requests
from goose3 import Goose, Configuration
from goose3.text import StopWordsChinese
from readability import Document

url = 'https://waimaoquan.alibaba.com/bbs/thread-htm-fid-309-66.html&tab=digest'
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',}


res = requests.get(url=url, headers=header)

from lxml import etree

html = etree.HTML(res.text)

a_list = html.xpath('//*[@id="J_posts_list"]/tr/td[2]/p[1]/a[3]/@href')


# print(len(a_list))

uri = 'https://www.cifnews.com/article/30666'

g = Goose({'stopwords_class': StopWordsChinese})
article = g.extract(url=uri)
config = Configuration()
config.enable_image_fetching = True
text = article.cleaned_text
# print(text)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
# res = requests.get('https://waimaoquan.alibaba.com/bbs/attachment/1809/thread/309_713107_6a75458c47ea357.png', headers=header)
# with open('sds.jpg', 'wb') as j:
#     j.write(res.content)

# 要访问的目标页面
targetUrl = "http://test.abuyun.com"

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
  "host": proxyHost,
  "port": proxyPort,
  "user": proxyUser,
  "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

# resp = requests.get('https://blog.csdn.net/qq_29186489/article/details/78496747', proxies=proxies, headers=header)
#
# print(resp.status_code)
# print(resp.text)


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import jieba
import matplotlib.pyplot as plt

# 传入需要分词的字符串
# 将分词后的结果以空格连接

words = " ".join(jieba.cut('''我们在做销售的过程中，经常碰到一种很头痛的问题，就是某个客户问你：“在我们国家有没有跟别的客户甚至大客户合作过？” 

这种问题呢，虽然有些时候，是一些客人为了避免同质化竞争，决定绕开一些供应商；但是大部分客人问这个问题的目的，是希望了解你的产品是否适合他的市场。如果你已经给他的同行供货，那说明品质、测试等等问题都是可以搞定的，因为他的同行可以用，他自然可以用，就那么简单。 

比如你给target美国报价，如果你已经是Home Depot或者Walmart的现有供应商，那很容易可以打进去，这就是“同行效应”。如果不是，你完全没有做过美国市场，哪怕你对于其他欧洲客户做了很多生意，哪怕你产品很好，品质很好，那些美国大买家一般也不会轻易考虑你，只会优先考虑他们同行现成的供应商，这样用起来方便，得心应手，跟单和谈判环节可以简单许多，节约大家时间。 

反过来，如果你做欧线的，或许是德国Lidl的供应商，那么你再开发Aldi，Tchibo，Metro，会十分容易，因为有前车之鉴，已经是他们同一层次的别的大买家的现成供应商，这就是优势～！ 

这跟你找工作是一个道理。 

假设你是google的程序员，你要跳槽apple，跳槽microsoft，很容易，猎头很轻易能把你介绍进去，基本不是问题。但是你如果在一个名不见经传的小公司做程序员，你要进入上面几家大公司，千难万难。不是说不可能，而是这个机会比那些背景好的会少很多。你能力再强，但是别人不知道啊，别人不见得会给你展示的机会。 

这就好比我过去在小公司工作的时候，我也会抱怨，觉得一些大公司的业务员能力超级烂，rubbish级别的，远不如我，还拿我几倍的薪水，我也不服气，也不甘心，但是事实就是如此，别人不给我面试机会，别人看不上我的职业背景，根本没法信任我。这就是现实，也是心态。 

因为你背景弱，等于是输在了起跑线上，后期要更努力，去争取别人剩下来的那么一丁点儿机会。 

话题有些扯远了，拉回正题吧。 

所以我过去做业务的时候，只要是有机会跟某个大买家合作了，哪怕只是一个很小的样品单，还是通过港台或者新加坡贸易商拿下的，都能让我无比开心。这说明有一个巨大的广告机会，我可以好好利用起来。 

很多年前做了disney的一个小单，还是做砸了做亏了，但是毕竟资料有，样品有，各种操作流程和验厂和测试要求都知道一些，就可以在接触别的客人的时候，让别人知道我是disney现有的供应商，结果，果然拿下的日本的hello kitty和德国nici的订单，这就是强大的广告效应。disney的同行会觉得，wow，你是disney供应商啊，那自然也可以给我们供货了。 

但是这类机会，其实有的时候，会被客人套上一个紧箍咒。 

比如我过去合作过的一个德国客人，我姑且把他称作A吧，A在德国市场真的是举足轻重，非常了不起，给我的订单也不小，每年4-5单，非常稳定。但是问题是，A跟我签了保密协议，约定我不能透露出，我给他们供货的情况，也不能把我给他们做的产品给别家看。 

这个问题就让我愁了很久，毕竟我还在跟另外一个德国买家B接触，毕竟B不如A，但是也是一个很优质的客人。可是B一直没下单纠结的问题，不是我的产品问题，也不是价格问题，样品和各种测试报告都已经确认了，B唯一担心的，就是我缺乏操作德国大客户的经验，生怕订单下过来后搞砸了，所以B一直在观望，也在物色别的供应商。 

我尽管屡次三番跟B说，我们有丰富的德国市场经验，目前有跟德国大客户合作，但是因为保密协议的问题，不能透露更详细的内容，也不能给你看那个德国客户的产品图片和任何测试报告。但是这个解释，B是不信的，他认为我为了拿订单，自然这么吹嘘，这么撒谎，但是我拿不出证据。 

所以我想了一招： 

本部分内容设定了隐藏,需要回复后才能看到

邮件发过去后，我就给B打了个电话，口头say sorry，解释了一下我们因为保密协议的关系，所以很多东西没法透露，请他谅解。但是我发了一些样品间的图片过来，如果你够仔细的话，应该可以从中看出一些我们另一个德国大客户的产品图片。当然，这是你自己发现的，我从来没有透露任何信息给你。结果B心领神会地大笑，后来订单就过来了。 '''))

# 导入背景图
backgroud_image = plt.imread("C:/Users/YQ/Desktop/好i.jpg")

# 设置停用词
stopwords = STOPWORDS
stopwords.add("电影")

wc = WordCloud(stopwords=stopwords,
# font_path="C:/Windows/Fonts/simkai.ttf",  # 解决显示口字型乱码问题
mask = backgroud_image, background_color="white", max_words=100)

my_wc = wc.generate_from_text(words)

image_colors = ImageColorGenerator(backgroud_image)


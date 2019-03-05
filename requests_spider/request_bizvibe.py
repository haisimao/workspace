import time
from urllib.parse import quote

import json
import requests

# 要访问的目标页面

origin_url = 'https://www.bizvibe.com/assets/json/level2Category16.json'

targetUrl = origin_url


header = {
            # 'origin': 'https://www.bizvibe.com',
            'Host': 'www.bizvibe.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            # 'Referer': 'https://www.bizvibe.com/worldwide/agriculture?page=2?rd=nlgehfefgfoclbpf_='
 }
data = json.dumps({"category":"10016","country":"","location_type":"","keyword":"","domain":"","revenue":"0","employee":"0","type":"undefined","offset":"0","limit":"12"})


cookies = \
    {'srch_countrycode': 'worldwide', 'BZVAUTH': '4573710414', '_ga': 'GA1.2.1759705083.1550453236', '_gat': '1',
     '_gid': 'GA1.2.1673095261.1550453236', '_pk_ses.8.9a72': '*', 'PHPSESSID': 'vbfd6c05jggc7uqprun72u64v0',
     'verifyCookie': 'Y', 'sessionid': 'vbfd6c05jggc7uqprun72u64v0', 'BZVU': '89271',
     'authsession': quote('89271~43TdFqvK2Pcg2gOtugvvBmfFL6U~Lilin~~上海钰祺网络科技有限公司~10037557~A~balalaba.com~eHh4eHgzMUBxcS5jb20='),
     '_pk_id.8.9a72': '6a411cae503639d9.1550453237.1.1550453253.1550453237.', 'srch_country': 'Worldwide'}


#################################
resp = requests.post(targetUrl, data=data, headers=header, cookies=cookies, allow_redirects=False)
# resp = requests.get(targetUrl, headers=header, cookies=cookies, allow_redirects=False)


print(resp.status_code, resp.url)
print(resp.text)

data = json.loads(resp.text)

ca_dict = {}
hits = data.get('hits').get('hits')
for hit in hits:
    _source = hit.get('_source')
    ca_dict[_source.get('unspsc_name')] = _source.get('unspsc_code')







































import time

import requests

# 要访问的目标页面
from db import RedisClient

origin_url = 'http://wmt.tendata.cn/trade/search?_dc={}&queryCodesDesc={}&page={}'
# origin_url = 'http://bizr.tendata.cn/api/user/companies/add'

targetUrl = origin_url.format(int(time.time() * 1000),
                                                      '%7B%22country%22%3A%22north_america%22%2C%22startDate%22%3A%222016-01-01%22%2C%22endDate%22%3A%222018-01-02%22%2C%22filterBlank%22%3Atrue%2C%22filterFields%22%3A%5B%22importer%22%5D%2C%22filterLogistics%22%3Atrue%2C%22highlights%22%3A%5B%22importer%22%5D%2C%22conditions%22%3A%7B%22importer%22%3A%5B%22%2BSCHNUCK%20MARKETS%2C%20INC.%22%5D%7D%2C%22rangeConditions%22%3A%7B%7D%2C%22description%22%3A%22%E7%AE%80%E8%BF%B0%EF%BC%9A2016-01-01-2018-01-02%EF%BC%8C%E8%BF%9B%E5%8F%A3%E5%95%86%EF%BC%9A%E5%8C%85%E5%90%AB%E2%80%9CSCHNUCK%20MARKETS%2C%20INC.%E2%80%9D%EF%BC%8C%22%2C%22catalog%22%3A%22imports%22%7D',
                                                      '1')


header = {
            'origin': 'http://wmt.tendata.cn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'X-CSRF-TOKEN': '811a6640-1a6b-4261-9b0e-b447455214f3',

 }
import json
# conn = RedisClient('cookies', 'tendata')
# cookies = json.loads(conn.random())
cookies = {
# 'Hm_lvt_d115b732f965ca67bde8c17cfd29e338':'1543223374',
# 'UM_distinctid':'1675392fd1a2fc-0fc5e6f33d23da-9393265-1fa400-1675392fd1c105',
# 'Hm_lpvt_d115b732f965ca67bde8c17cfd29e338':'1543471831',
# 'JSESSIONID':'5C1E799ECA932AA13E97AAD4D072F766',
# 'CNZZDATA2366241':'cnzz_eid%3D1705041332-1543468006-null%26ntime%3D1543482744',

'__SDID':'94a2424d8bfde4b7',
'Hm_lvt_d115b732f965ca67bde8c17cfd29e338':'1543223374' ,
'UM_distinctid': '1675392fd1a2fc-0fc5e6f33d23da-9393265-1fa400-1675392fd1c105',
'Hm_lpvt_d115b732f965ca67bde8c17cfd29e338': '1543471831',
'JSESSIONID':'2737D5634CF55F6FE390B851B0D31DF1',
'CNZZDATA2366241':'cnzz_eid%3D1126902450-1543295400-%26ntime%3D{}'.format(int(time.time() * 10)),

}
resp = requests.post(targetUrl, headers=header, cookies=cookies)

print(resp.status_code)
import json
# print(json.loads(resp.text))
print(resp.text)
























import time

import requests

# 要访问的目标页面
from db import RedisClient
from urllib.request import quote

# origin_url = 'http://wmt.tendata.cn/trade/search?_dc={}&queryCodesDesc={}&page={}'
origin_url = 'http://bizr.tendata.cn/api/user/companies/add?name={}&catalog={}&country={}&companySource={}'
# origin_url = 'http://bizr.tendata.cn/api/user/companies/add'

targetUrl = origin_url.format(quote("2310439 ONTARIO INC"),
                "BUYER",
                "NORTH_AMERICA",
                "SEARCH")


import json
# conn = RedisClient('cookies', 'tendata')
# cookies = json.loads(conn.random())
header = {
            'origin': 'http://wmt.tendata.cn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'X-CSRF-TOKEN': '8b17fa32-4b2b-43e1-b819-221d1e062ba8',

 }
cookies = {
# '__SDID':'94a2424d8bfde4b7',
'Hm_lvt_d115b732f965ca67bde8c17cfd29e338':'1543223374' ,
'UM_distinctid': '1675392fd1a2fc-0fc5e6f33d23da-9393265-1fa400-1675392fd1c105',
'Hm_lpvt_d115b732f965ca67bde8c17cfd29e338': '1543471831',
'JSESSIONID':'2737D5634CF55F6FE390B851B0D31DF1',
'CNZZDATA2366241':'cnzz_eid%3D1705041332-1543468006-null%26ntime%3D1543481507',


}
{
	"name": quote("2310439 ONTARIO INC"),
	"catalog": quote("BUYER"),
	"country": quote("NORTH_AMERICA"),
	"companySource": quote("SEARCH")
}

data = {
	"name": json.dumps("2310439 ONTARIO INC"),
	"catalog": json.dumps("BUYER"),
	"country": json.dumps("NORTH_AMERICA"),
	"companySource": json.dumps("SEARCH"),
}
# http://bizr.tendata.cn/user/search#/detail?type=buyer&value=inc&mode=company
resp = requests.put(targetUrl, headers=header, cookies=cookies, allow_redirects=False)

print(resp.status_code, resp.text)

if __name__ == '__main__':
    pass






















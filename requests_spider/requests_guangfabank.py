import time
from urllib.parse import quote

import requests

# 要访问的目标页面
origin_url = 'http://www.cgbchina.com.cn/Channel/185652'
targetUrl = origin_url
header = {
            'origin': 'http://www.cgbchina.com.cn',
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
 }
data = {
'operation': 'net',
'searchNetBranch': '%B3%C9%B6%BC%B7%D6%D0%D0',
'currPage': '1',
'pageSize': '20',
'searchNetBranchSel': '%B3%C9%B6%BC%B7%D6%D0%D0',
'searchNetKeyword': '',
'equType2': '-1',
'searchATMBranch2': '%B1%B1%BE%A9%B7%D6%D0%D0',
'searchATMKeyword2': '',
}
cookies = {
'JSESSIONID':'0000gU13_vV_MprJ7P8C_KU0Bh4:1bh1u2rel',
'gdb':'1560389824.52491.0000',
'_gscu_1273929099':'4691734783xdws57',
'_gscbrs_1273929099':'1',
'_gspc1':'1',
'_gspc2':'1',
'_gscs_1273929099':'46917347isyi2f57|pv:7',
}

resp = requests.post(targetUrl, data=data, headers=header,cookies=cookies , allow_redirects=False)

print(resp.status_code, resp.url)
print(resp.text)



















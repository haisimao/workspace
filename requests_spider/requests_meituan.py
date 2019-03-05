import time
from urllib.parse import quote

import json
import requests

# 要访问的目标页面

origin_url = 'https://ihotel.meituan.com/group/v2/poi/detail/service?utm_medium=pc&version_name=999.9&poiId=170543955&X-FOR-WITH=fSKnAjslhf9eFgISD%2FuFkzD69qBmIJjxJgmQxz%2BhTeTtOK4W1hCLe9UaPL5o3fdYdm4yCvP9rRk%2FgIQYuXzSF%2BuQJkTXJObD7AJCyHr1h8qs3pNOFR1ti7WO1gbsQY6pSkkIWhc4eB1fUmnR50G7Fw%3D%3D'

targetUrl = origin_url


header = {
            'Host': 'ihotel.meituan.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
 }
data = json.dumps(
    {'utm_medium': 'pc',
'version_name': '999.9',
'poiId': '170543955',
'X-FOR-WITH': "fSKnAjslhf9eFgISD/uFkzD69qBmIJjxJgmQxz+hTeTtOK4W1hCLe9UaPL5o3fdYdm4yCvP9rRk/gIQYuXzSF+uQJkTXJObD7AJCyHr1h8qs3pNOFR1ti7WO1gbsQY6pSkkIWhc4eB1fUmnR50G7Fw==",}

)


resp = requests.get(targetUrl, data=data, headers=header, allow_redirects=False)


print(resp.status_code, resp.url)
print(resp.text)

import time
from urllib.parse import quote

import requests

# 要访问的目标页面
from bs4 import BeautifulSoup

# origin_url = 'https://www.tradeatlas.com/p7search/US/HS_CODE/6115/1293832800000/1356991199000?page=1'
origin_url = 'https://www.tradeatlas.com/p7firm/US/mcgregor-industries-inc/eyJhMSI6IkhTX0NPREUiLCJkMSI6IjYxMTUiLCJzMSI6MTI5MzgzMjgwMCwiZjEiOjEzNTY5OTExOTksImlsayI6IjU1ZTc0YWI1ZTlhOGYzNDkifQ==/272e60e1e6276d7a'
targetUrl = origin_url
header = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
 }
data = {}
cookies = {
'__utmz':'262406345.1543825999.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
'__utmz':'1.1543825999.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc:262406345',
' __utmc':'1',
'__utma':'262406345.244459286.1543825999.1550050750.1550108537.6',
'__utma':'1.2001971904.1543825999.1550050750.1550108538.6',
'__utmb':'262406345.18.10.1550108537',
'__utmb':'1.18.10.1550108538',
'tradeatlassession':'eyJpdiI6IkdrOUU3NkhrMWlKUVkxT1BJc1gzenp1bTVGdHZoN1p4bGJHbTNWNVwvOU9NPSIsInZhbHVlIjoiTFwvdW9cL3VVdStlaVVmQ1MzRGtNZFdGTlhBdmQrbGJOSGlsaldRWUpcL2h4UjVsa3d2VXJXK0pNSzl0d21mRmExbDdPWGFCd3BqQ3ZLbEdybHQrMmFDOXc9PSIsIm1hYyI6ImNlOTc4NWM0YzlmMjA0MWEwM2I5MTBkNzc1Y2FlYWVkMDM2NDA4Yzk5Y2IyNzQ5ZDViN2YwMmVmNTFjMTFiYTIifQ%3D%3D',
'lang_value':'eyJpdiI6IlwvSStwMjRJR1dxVmVaQUdMWWE4ZUJBVkpQSFE4OGJKTkltWGdzTnhmXC9yVT0iLCJ2YWx1ZSI6IkpYdU9qa2o2cTdBdE9YeGFlV3RZMFJIN1V1Rzg0dDR2Rlwvb0ptWmFyXC9maz0iLCJtYWMiOiIxMzQ3MDJlZDYxNzFhMWMyZmIyYjNiMGJkNzlhM2E0MTdlZWY0N2U5Zjc2OTZhMzg0YzU4Yzc2MGZjZDlhOTk4In0%3D',
}

resp = requests.get(targetUrl,  headers=header, cookies=cookies, allow_redirects=False)

print(resp.status_code, resp.url)
# print(resp.text)
# soup = BeautifulSoup(resp.text, 'lxml')
# div_searchresult = soup.find_all('div', attrs={'class': 'searchresult'})[0] if soup.find_all('div', attrs={'class': 'searchresult'}) else None
# tr_list = div_searchresult.find_all('tr')
#
# for tr in tr_list:
#     a_tag = tr.find_all('a')[0] if tr.find_all('a') else None
#     if a_tag != None:
#         a_src = a_tag.get('href')
#         print(a_src)
soup = BeautifulSoup(resp.text, 'lxml')
ul_list = soup.find_all('ul', attrs={'class': 'dt-sc-fancy-list'})
comp_ul = ul_list[0] if ul_list else None
email_ul = ul_list[-1] if ul_list else None
if comp_ul:
    comp_lis = comp_ul.find_all('li')
    comp_name = comp_lis[0].text.replace('Name : ', '').replace('\n', '').strip() if comp_lis[0].text else ''
    comp_Address = comp_lis[1].text.replace('Address :', '').replace('\n', '').strip() if comp_lis[1].text else ''
    comp_Country = comp_lis[-1].text.replace('Country :', '').replace('\n', '').strip() if comp_lis[-1].text else ''
if email_ul:
    email_lis = email_ul.find_all('li')
    web_page = email_lis[0].text.replace('Web Page', '').replace(':', '').replace('\n', '').strip() if email_lis[0].text else ''
    EMail = email_lis[1].text.replace('E-Mail', '').replace(':', '').replace('\n', '').strip() if email_lis[1].text else ''
    Telephone = email_lis[2].text.replace('Telephone', '').replace(':', '').replace('\n', '').strip() if email_lis[2].text else ''
    fax = email_lis[3].text.replace('Fax :', '').replace('\n', '').strip() if email_lis[3].text else ''
# custom_div = soup.find('div', attrs={'class': 'searchresult'})
# tr_list = custom_div.find_all('tr')[1:]
# for tr in tr_list:
#     td_list = tr.find_all('td')
#     port_time = td_list[0].string.strip() if td_list[0].string else ''
#     hs_code = td_list[1].string.strip() if td_list[1].string else ''
#     proe_dese = td_list[2].string.strip() if td_list[2].string else ''
#     EXPORTER = td_list[3].string.strip() if td_list[3].string else ''
#     COUNTRYOFORIGIN = td_list[4].string.strip() if td_list[4].string else ''
#     value_sum = td_list[-1].string.strip() if td_list[-1].string else ''
#
    print(EMail, Telephone)

































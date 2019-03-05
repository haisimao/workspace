
import jsonpath
import requests
import js


url = 'http://www.cebpubservice.com/ctpsp_iiss/SecondaryAction/findDetails.do'
# url = 'http://rczp.hsbank.com.cn:8000/cggl/modules/pur/PUR4040/pur_bid_announcement_context.screen?title_id=2048'

hearder = {
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


# # 顶部信息
param_data1 = {
    'schemaVersion': 'V60.02',
    # 'businessKeyWord': 'tenderBulletin',
    'businessKeyWord': 'tenderProject',
    'tenderProjectCode': js.get_js(),
}
print(js.get_js())
res = requests.post(url=url, data=param_data1)
# print(js.get_js())
print(res.content.decode('utf-8'))
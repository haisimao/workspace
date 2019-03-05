import datetime

import execjs
# 碧岭900kWp分布式光伏设施农业项目,粤江公司2018年氨站压力管道定检服务委外项目招标公告,
# 中国石化集团资产经营管理有限公司齐鲁石化分公司供排水厂炼油第三循环水场安全隐患治理项目工程监理招标公告
tenderProjectCode=['E4403000004007138002', 'M4401000017182995299', 'B1100000013016685002']
js_tenderProjectCode = ['FC6E8B11AFCAF76627FA1A14C8AB05CF2B376D1D0E1BF14887D7D07AC568EC85D8E3A603C18407B2',
                        '02078ECD74EBC280B5521A709A975AB38D7F7046CF5943999F5C3BBE5BFBA2C7062F2D19CC44A1E4',
                        '65531A4C3DA57E7611AD827D1E8F3078C7B0CA2ABC6AD759D7C004922924024AE505839452465E04']
# 执行本地的js


def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("./JS.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    Cu_time = ctx.call('CurentTime')
    return ctx.call('strEnc', 'A4310000000000218001', Cu_time, 'cebpubservice', 'iiss')


# // var key1 = CurentTime();
# // var key2 = "cebpubservice";
# // var key3 = "iiss";
if __name__ == '__main__':
    print(get_js())


'''
1F37356009A953353860F628B09420D03860F628B09420D01C7242368CF9848BAA0CAAA5949267F3

'''





























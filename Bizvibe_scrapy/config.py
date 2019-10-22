# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    # 'weibo': 'WeiboCookiesGenerator',
    # 'baidu': 'BaiDuGenerator',
    # 'alibaba': 'AliBaBaGenerator',
    'linkedin': 'LinkedinGenerator',

}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    # 'weibo': 'WeiboValidTester',
    # 'alibaba': 'AliBaBaValidTester',
    'linkedin': 'LinkedinValidTester',
}
# 测试类的URI
TEST_URL_MAP = {
    'weibo': 'https://m.weibo.cn/',
    'baidu': 'http://news.baidu.com/',
    'alibaba': 'http://sourcing.alibaba.com/?spm=a2700.8293689.scGlobalHomeHeader.376.46ce65aavJsBwp&tracelog=header_rfq_market',
    'linkedin': '''https://www.linkedin.com/voyager/api/organization/companies?decoration=%28adsRule%2CaffiliatedCompaniesWithEmployeesRollup%2CaffiliatedCompaniesWithJobsRollup%2CarticlePermalinkForTopCompanies%2CautoGenerated%2CbackgroundCoverImage%2Cclaimable%2CclaimableByViewer%2CcompanyEmployeesSearchPageUrl%2CcompanyPageUrl%2CcompanyType%2CconfirmedLocations*%2CcoverPhoto%2CdataVersion%2Cdescription%2CentityUrn%2CfollowingInfo%2CfoundedOn%2Cheadquarter%2CjobSearchPageUrl%2ClcpTreatment%2Clogo%2Cname%2Ctype%2CoverviewPhoto%2CpaidCompany%2CpartnerCompanyUrl%2CpartnerLogo%2CpartnerLogoImage%2Cpermissions%2CrankForTopCompanies%2CsalesNavigatorCompanyUrl%2Cschool%2Cshowcase%2CstaffCount%2CstaffCountRange%2CstaffingCompany%2CtopCompaniesListName%2CuniversalName%2Curl%2CviewerConnectedToAdministrator%2CviewerEmployee%2CviewerFollowingJobsUpdates%2CviewerPendingAdministrator%2CcompanyIndustries*%2Cindustries%2Cspecialities%2CacquirerCompany~%28entityUrn%2Clogo%2Cname%2Cindustries%2CfollowingInfo%2Curl%2CpaidCompany%2CuniversalName%29%2CaffiliatedCompanies*~%28entityUrn%2Clogo%2Cname%2Cindustries%2CfollowingInfo%2Curl%2CpaidCompany%2CuniversalName%29%2Cgroups*~%28entityUrn%2ClargeLogo%2Clogo%2CgroupName%2CmemberCount%2CwebsiteUrl%2Curl%29%2CshowcasePages*~%28entityUrn%2Clogo%2Cname%2Cindustries%2CfollowingInfo%2Curl%2Cdescription%2CuniversalName%29%29&q=universalName&universalName={}''',
}

# 产生器和验证器循环周期
CYCLE = 120000

# API地址和端口
API_HOST = '127.0.0.1'
API_PORT = 8000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = False

# cookies的保存状态,原生或者{name: value}
COOKIES_STATUS = False

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "H64TRI2ZE542872D"
proxyPass = "701A47442D6A8BF1"
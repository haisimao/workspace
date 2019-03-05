import time
import os

while True:
    # os.system("scrapy crawl bizvibe -s JOBDIR=crawls/storeMyRequest")
    os.system("scrapy crawl bizvibe")
    time.sleep(3700)  # 运行时间间隔

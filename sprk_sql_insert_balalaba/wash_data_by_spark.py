import os
import sys
#配置环境变量并导入pyspark
os.environ['SPARK_HOME'] = r'D:\work_env\spark-2.4.0-bin-hadoop2.7'
sys.path.append(r"D:\work_env\spark-2.4.0-bin-hadoop2.7\python")
sys.path.append(r"D:\work_env\spark-2.4.0-bin-hadoop2.7\python\lib/py4j-0.9-src.zip")
from pyspark import SparkContext, SparkConf

appName ="spark_1" #应用程序名称
master = "spark://hadoop01:7077"       #hadoop01为主节点hostname，请换成自己的主节点主机名称
conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)

data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)
res = distData.reduce(lambda a, b: a + b)
print("===========================================")
print(res)
print("===========================================")


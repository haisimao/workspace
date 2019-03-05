from pyspark import SparkContext
from pyspark.sql import SQLContext


if __name__ == "__main__":
    sc = SparkContext(appName="mysqltest")
    sqlContext = SQLContext(sc)
    df = sqlContext.read.format("jdbc").options(url="jdbc:mysql://127.0.0.1\
	 	:3306/to_balalaba?user=root&password=yq201808", dbtable="comps").load()
    df.show()

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

from clustering import main, sb

if __name__ == "__main__":
    conf = SparkConf()
    conf.setMaster('yarn')
    conf.setAppName('mikra-project-1')
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    main(spark, sc)
    sb.build()

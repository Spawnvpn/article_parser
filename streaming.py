import json
import os
import sys

# Path for spark source folder
import uuid

os.environ['SPARK_HOME'] = '/home/vagrant/spark-2.1.0-bin-hadoop2.7/'

# Append pyspark  to Python Path
sys.path.append("/home/vagrant/spark-2.1.0-bin-hadoop2.7/python/pyspark")

os.environ['PYSPARK_PYTHON'] = "/usr/bin/python2.7"

sys.path.append("/home/vagrant/spark-2.1.0-bin-hadoop2.7/python")
sys.path.append("/home/vagrant/spark-2.1.0-bin-hadoop2.7/python/lib/py4j-0.10.3-src.zip")
try:
    from pyspark import SparkContext
    from pyspark import SparkConf
    from pyspark.streaming import StreamingContext
    from pyspark.sql import HiveContext, Row
    print("Successfully imported Spark Modules")

except ImportError as e:
    print("Can not import Spark Modules", e)
    sys.exit(1)


sc = SparkContext('local[2]')
ssc = StreamingContext(sc, 3)
lines = ssc.textFileStream("hdfs://192.168.1.23:8020/user/bogdan")
hiveCtx = HiveContext(sc)


# text_file = sc.textFile("hdfs://0.0.0.0:9020/user/bogdan")

# counts = lines.flatMap(lambda line: line.strip().split(" "))

def save_file(rdd):
    path = 'hdfs://192.168.1.23:8020/user/spark/output/{0}'.format(str(uuid.uuid4()))
    rdd.saveAsTextFile(path)
    return path


data = lines.map(lambda x: json.loads(x))
# data.pprint()
data.foreachRDD(lambda x: process_data(x) if not x.isEmpty() else x)

def process_data(rdd):
    # rdd.map(lambda x: x['content']).saveAsTextFile('hdfs://0.0.0.0:9020/user/spark/output/{0}'.format(str(uuid.uuid4())))
    counts = rdd.flatMap(lambda line: line['content'].strip().split(" "))\
        .map(lambda word: (word, 1))\
        .reduceByKey(lambda a, b: a + b, 1)\
        .map(lambda (a, b): (b, a))\
        .sortByKey(0, 1)\
        .map(lambda (a, b): (b, a)).saveAsTextFile('hdfs://192.168.1.23:8020/user/spark/' + str(uuid.uuid4()))
    # counts.saveAsTextFiles('hdfs://0.0.0.0:9020/user/spark/scrapy_word_counter')

    # json_data.foreachRDD(save_to_db)
# data.map(lambda x: x['content']).saveAsTextFiles('hdfs://0.0.0.0:9020/user/spark/output')
# content = data.map(lambda x: x['content'])
# content.saveAsTextFiles('hdfs://0.0.0.0:9020/user/spark/output')


# counts = lines.flatMap(lambda line: line.strip().split(" "))\
#     .map(lambda word: (word, 1))\
#     .reduceByKey(lambda a, b: a + b, 1)\
#     .map(lambda (a, b): (b, a))\
#     .sortByKey(0, 1)\
#     .map(lambda (a, b): (b, a))
# counts.saveAsTextFiles('hdfs://0.0.0.0:9020/user/spark/output')
# print(type(counts))

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate

from math import log
from pyspark.sql import SparkSession
import datetime

start=datetime.datetime.now()
logFile = "logs.json"  # Should be some file on your system
# logFile="../34-Apache-Spark-ML-Claims/patent_claims_fulltext.csv"
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile) # .cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()
end=datetime.datetime.now()

print("Elapsed time for logFile {}: {}".format(logFile,end-start))
print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()

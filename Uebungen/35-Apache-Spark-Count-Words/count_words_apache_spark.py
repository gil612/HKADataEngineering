# source: https://www.informatik-aktuell.de/entwicklung/methoden/einfuehrung-in-spark-ein-text-mining-projekt.html
# https://stackoverflow.com/questions/48927271/count-number-of-words-in-a-spark-dataframe/48930628

from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import datetime

start=datetime.datetime.now()
inputFile="patent_claims_excerpt3.csv"
#inputFile = "patent_claims_excerpt2.csv"
#inputFile="patent_claims_fulltext_cleaned.csv"
spark = SparkSession.builder.appName("Count occurrence of each words").getOrCreate()

# select columns from csv file
# create a column with an id
print('Opening file {}'.format(inputFile))
df=spark.read.csv(inputFile,sep=',',header=True,quote='"') \
        .drop("claim_no") \
        .drop("dependencies") \
        .drop("ind_flg") \
        .drop("appl_id")
print('First columns of dataframe:')
print(df.columns)
print('#rows in the dataframe:')
print(df.count())

# Count occurrence of each word
print('Count occurrence of each word:')
df.withColumn('word', f.explode(f.split(f.col('claim_txt'), '\W')))\
    .groupBy('word')\
    .count()\
    .sort('count', ascending=False)\
    .show()

end=datetime.datetime.now()
print('Elapsed time: {}'.format(end-start))

spark.stop()

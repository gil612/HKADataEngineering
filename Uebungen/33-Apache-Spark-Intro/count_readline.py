# count lines with letter 'a' and 'b'
import datetime
from sys import exc_info

start=datetime.datetime.now()
count_a=0
count_b=0
# fn='logs.json'
fn="../34-Apache-Spark-ML-Claims/patent_claims_fulltext.csv"
with open(fn,"r") as fo:
    while True:
        try:
            tmpstr=fo.readline()
            if not tmpstr:
                break
            if 'a' in tmpstr:
                count_a=count_a+1
            if 'b' in tmpstr:
                count_b=count_b+1
        except:
            print('Ignored error')
end=datetime.datetime.now()

print("Elapsed time for logFile {}: {}".format(fn,end-start))
print("Lines with a: %i, lines with b: %i" % (count_a, count_b))

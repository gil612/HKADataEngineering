from math import log
import datetime

start=datetime.datetime.now()

fn= "logs.json"  # Should be some file on your system
#fn="../34-Apache-Spark-ML-Claims/patent_claims_fulltext.csv"

with open(fn,"r") as fo:
    tmp_list=fo.readlines()
    a=0
    b=0
    for x in tmp_list:
        if "a" in x:
            a +=1
        if "b" in x:
            b+=1

end=datetime.datetime.now()

print("a = "+str(a) +"\nb = "+str(b))
print(end-start)
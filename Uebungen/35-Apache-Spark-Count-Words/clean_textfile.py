# remove lines with failure prone characters from file
import datetime
inputFile="patent_claims_fulltext.csv"
outFile=inputFile.split('.') +"_cleaned" + ".csv"

start=datetime.datetime.now()
cnt=0
with open(inputFile,'r') as fo:
    with open(outFile,'w',buffering=100000) as fw:
        while True:
            try:
                str=fo.readline()
                if str == '' or str is None:
                    break
                fw.write(str)
            except:
                cnt+=1
                print('Failed to read line (count: {})'.format(cnt))
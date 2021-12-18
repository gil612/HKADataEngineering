# see https://github.com/influxdata/influxdb-client-python#queries
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

url="http://localhost:8086"
bucket="DataEngineering4"
# after having started influx db, get token from http://localhost:8086/,
# go to "Load Data" -> "API Tokens", click on <USER> token and copy your token
token="pHLo0PUuqh1KB-uVdkH-wHdbL2mWgD7jqol1kuDwK0N9730qYu0VVJavWhqYmB7ifmmHWBqHaV3UN7616yycQA=="
org="HKA"

client = InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

# Query: using Pandas DataFrame
query='from(bucket:"{}")' \
        ' |> range(start: 0, stop: now())' \
        ' |> filter(fn: (r) => r._measurement == "research-plant")' \
        ' |> max()'.format(bucket)

start=datetime.datetime.now()
df=query_api.query_data_frame(query)
print(df.head())
end=datetime.datetime.now()
print('Elapsed {}'.format(end-start))
# Close client
client.close()
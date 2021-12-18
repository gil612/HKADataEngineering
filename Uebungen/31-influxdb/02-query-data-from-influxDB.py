# see https://docs.influxdata.com/influxdb/v2.1/api-guide/client-libraries/python/
import influxdb_client

url="http://localhost:8086"
bucket="DataEngineering"
# after having started influx db, get token from http://localhost:8086/,
# go to "Load Data" -> "API Tokens", click on <USER> token and copy your token
token="pHLo0PUuqh1KB-uVdkH-wHdbL2mWgD7jqol1kuDwK0N9730qYu0VVJavWhqYmB7ifmmHWBqHaV3UN7616yycQA=="
org="HKA"

# Instantiate the client
client=influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

query_api = client.query_api()
query = ' from(bucket:"{}")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "my_measurement")\
|> filter(fn: (r) => r.location == "Prague")\
|> filter(fn:(r) => r._field == "temperature" )'.format(bucket)
result = query_api.query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))

print(results)
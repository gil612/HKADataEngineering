# see https://docs.influxdata.com/influxdb/v2.1/api-guide/client-libraries/python/

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

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

#Instantiate a write client
write_api=client.write_api(write_options=SYNCHRONOUS)

#Create a point object and write it to InfluxDB
p=influxdb_client.Point("my_measurement").tag("location", "Prague") \
   .field("temperature", 25.3)
write_api.write(bucket=bucket, org=org, record=p)


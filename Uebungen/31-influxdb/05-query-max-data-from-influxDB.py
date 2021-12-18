# see https://github.com/influxdata/influxdb-client-python#writes
from influxdb_client import InfluxDBClient
import datetime

token="pHLo0PUuqh1KB-uVdkH-wHdbL2mWgD7jqol1kuDwK0N9730qYu0VVJavWhqYmB7ifmmHWBqHaV3UN7616yycQA=="
org="HKA"
bucket="DataEngineering4"
client=InfluxDBClient(url="http://localhost:8086", token=token, org=org, debug=True)

start=datetime.datetime.now()
# Querying max values of data from research plant
query='from(bucket:"{}")' \
        ' |> range(start: 0, stop: now())' \
        ' |> filter(fn: (r) => r._measurement == "research-plant")' \
        ' |> max()'.format(bucket)
result=client.query_api().query(query=query)

# Processing results
print()
print("=== results ===")
print()
for table in result:
    for record in table.records:
        print('max {0:5} = {1}'.format(record.get_field(), record.get_value()))
end=datetime.datetime.now()
print('Elapsed {}'.format(end-start))
# Close client
client.close()
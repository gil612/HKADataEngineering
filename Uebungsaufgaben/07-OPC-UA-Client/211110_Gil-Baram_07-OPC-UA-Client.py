import asyncio
from asyncua import ua, Node, Client
async def opc_ua_Client():
   async with Client(url = 'opc.tcp://opcua.demo-this.com:51210/UA/SampleServer') as client:


      node = client.get_node('ns=4;i=1259')
      value = await node.read_value()
      print('Boiler #1/Drum1001/LIX001/Output', value)

      node_measurment = client.get_node('ns=4;i=1274')
      value = await node_measurment.read_value()
      print('Boiler #1/FC1001/Measurement', value)

      node2 = client.get_node('ns=5;i=15')
      value = await node.read_value()
      print('Boiler #2/Pipe2002/FTX002/Output', value )


asyncio.run(opc_ua_Client())


# Boiler #1/Drum1001/LIX001/Output -0.0932
# Boiler #1/FC1001/Measurement 0.649
# Boiler #2/Pipe2002/FTX002/Output -0.098
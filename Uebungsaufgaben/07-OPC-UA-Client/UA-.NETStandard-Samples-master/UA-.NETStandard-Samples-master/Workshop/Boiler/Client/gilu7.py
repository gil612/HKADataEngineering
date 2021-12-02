import asyncio
from asyncua import Client, Node, ua

async def main():
    url = 'opc.tcp://opcua.demo-this.com:51210/UA/SampleServer'
    async with Client(url=url) as client:

        # boiler #1
        output = client.get_node('ns=4;i=1259')
        print("Value for Boiler #1/Drum1001/LIX001/Output", await output.read_value())
        
        # boiler #1
        meassurement = client.get_node('ns=4;i=1274')
        print("Value for Boiler #1/FC1001/Measurement", await meassurement.read_value())
        
        # boiler 2
        output_2 = client.get_node('ns=5;i=15')
        print("Value for Boiler #2/Pipe2002/FTX002/Output", await output_2.read_value())
      


asyncio.run(main())


# async with Client(url='opc.tcp://localhost:4840/freeopcua/server/') as client:
#     while True:
#         # Do something with client
#         node = client.get_node('i=85')
#         value = await node.read_value()
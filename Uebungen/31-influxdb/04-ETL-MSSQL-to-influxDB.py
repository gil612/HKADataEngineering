# for influxDB part, see https://github.com/influxdata/influxdb-client-python#writes

# influxDB imports
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime
start=datetime.datetime.now()
# influxDB
url="http://localhost:8086"
token="pHLo0PUuqh1KB-uVdkH-wHdbL2mWgD7jqol1kuDwK0N9730qYu0VVJavWhqYmB7ifmmHWBqHaV3UN7616yycQA=="
org="HKA"
bucket="DataEngineering2"

# MSSQL connection
import pyodbc

server = 'md2c0gdc' 
database = 'HSKA_Anlagenschema' 
username = 'sa' 
password = 'KWmz6QOHDPLIPqzJD9t2' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor=cnxn.cursor()

# read all data from DB ordered by time
cursor.execute("""SELECT TOP 1000 [Id]
      ,[LI10002/MonAnalog.PV_Out#Value]
      ,[YC10001/Valve$Analog.MV#Value]
      ,[PI12002/MonAnalog.PV_Out#Value]
      ,[PL1200/CM.siP_Out#Value]
      ,[PL1100/CM.siP_Out#Value]
      ,[PI12003/MonAnalog.PV_Out#Value]
      ,[PDI14014/MonAnalog.PV_Out#Value]
      ,[YC14001/Valve$Analog.MV#Value]
      ,[FIC14002/PID.MV#Value]
      ,[FIC14002/PID.PV_Out#Value]
      ,[FIC14002/PID.SP#Value]
      ,[PI14013/MonAnalog.PV_Out#Value]
      ,[YC14006/Valve$Analog.MV#Value]
      ,[PDIC14010/PID.MV#Value]
      ,[PDIC14010/PID.PV_Out#Value]
      ,[PDIC14010/PID.SP#Value]
      ,[PI14012/MonAnalog.PV_Out#Value]
      ,[YC23001/Valve$Analog.MV#Value]
      ,[YC22001/Valve$Analog.MV#Value]
      ,[YC21001/Valve$Analog.MV#Value]
      ,[FIC23002/PID.PV_Out#Value]
      ,[FIC23002/PID.MV#Value]
      ,[FIC23002/PID.SP#Value]
      ,[FIC22002/PID.MV#Value]
      ,[FIC22002/PID.PV_Out#Value]
      ,[FIC22002/PID.SP#Value]
      ,[FIC21002/PID.MV#Value]
      ,[FIC21002/PID.PV_Out#Value]
      ,[FIC21002/PID.SP#Value]
      ,[YS23004/Valve.Ctrl#Value]
      ,[YS22004/Valve.Ctrl#Value]
      ,[YS21004/Valve.Ctrl#Value]
      ,[LIC23002/PID.MV#Value]
      ,[LIC23002/PID.PV_Out#Value]
      ,[LIC23002/PID.SP#Value]
      ,[LIC22002/PID.MV#Value]
      ,[LIC22002/PID.PV_Out#Value]
      ,[LIC22002/PID.SP#Value]
      ,[LIC21002/PID.MV#Value]
      ,[LIC21002/PID.PV_Out#Value]
      ,[LIC21002/PID.SP#Value]
      ,[YC23006/Valve$Analog.MV#Value]
      ,[YC22006/Valve$Analog.MV#Value]
      ,[YC21006/Valve$Analog.MV#Value]
      ,[PL2350/DriveSpeedContr.RbkOut#Value]
      ,[PL2350/DriveSpeedContr.FbkFwdOut#Value]
      ,[PL2350/DriveSpeedContr.FbkRevOut#Value]
      ,[PL2250/DriveSpeedContr.RbkOut#Value]
      ,[PL2250/DriveSpeedContr.FbkFwdOut#Value]
      ,[PL2250/DriveSpeedContr.FbkRevOut#Value]
      ,[PL2150/DriveSpeedContr.RbkOut#Value]
      ,[PL2150/DriveSpeedContr.FbkFwdOut#Value]
      ,[PL2150/DriveSpeedContr.FbkRevOut#Value]
      ,[YS23012/Vlv2WayL.CtrlV0#Value]
      ,[YS23012/Vlv2WayL.CtrlV1#Value]
      ,[YS23012/Vlv2WayL.CtrlV2#Value]
      ,[YS22012/Vlv2WayL.CtrlV0#Value]
      ,[YS22012/Vlv2WayL.CtrlV1#Value]
      ,[YS22012/Vlv2WayL.CtrlV2#Value]
      ,[YS21012/Vlv2WayL.CtrlV0#Value]
      ,[YS14004/Valve.Ctrl#Value]
      ,[PIC14007/PID.MV#Value]
      ,[PIC14007/PID.PV_Out#Value]
      ,[PIC14007/PID.SP#Value]
      ,[YC14008/Valve$Analog.Ctrl#Value]
      ,[PI10003/MonAnalog.PV_Out#Value]
      ,[YS10004/Valve.Ctrl#Value]
      ,[DeviationID/DeviationID.PV#Value]
      ,[YS10008/Valve.Ctrl#Value]
      ,[YS11004/Valve.Ctrl#Value]
      ,[YS14010/Valve.Ctrl#Value]
      ,[YS14011/Valve.Ctrl#Value]
      ,[YS14003/Valve.Ctrl#Value]
      ,[YS14005/Valve.Ctrl#Value]
      ,[FIC33004/FI.PV_Out#Value]
      ,[YS21012/Vlv2WayL.CtrlV1#Value]
      ,[YS21012/Vlv2WayL.CtrlV2#Value]
      ,[SFC_Dreitank_StepNo/CuStepNo.PV#Value]
      ,[timestamp]
  FROM [HKA_SmA].[dbo].[timeseries_SmAKheDreiTankAllVariables]""")

# write each row to influxDB
client=influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
write_api=client.write_api(write_options=SYNCHRONOUS)

row=True
while(row):
    row=cursor.fetchone()
    if row:
        if row[1] is None:
            continue
        p=influxdb_client.Point("research-plant") \
            .tag("type","measurements") \
            .field("Id",float(row[0])) \
            .field("LI10002/MonAnalog.PV_Out#Value",float(row[1])) \
            .field("YC10001/Valve$Analog.MV#Value",float(row[2])) \
            .field("PI12002/MonAnalog.PV_Out#Value",float(row[3])) \
            .field("PL1200/CM.siP_Out#Value",float(row[4])) \
            .field("PL1100/CM.siP_Out#Value",float(row[5])) \
            .field("PI12003/MonAnalog.PV_Out#Value",float(row[6])) \
            .field("PDI14014/MonAnalog.PV_Out#Value",float(row[7])) \
            .field("YC14001/Valve$Analog.MV#Value",float(row[8])) \
            .field("FIC14002/PID.MV#Value",float(row[9])) \
            .field("FIC14002/PID.PV_Out#Value",float(row[10])) \
            .field("FIC14002/PID.SP#Value",float(row[11])) \
            .field("PI14013/MonAnalog.PV_Out#Value",float(row[12])) \
            .field("YC14006/Valve$Analog.MV#Value",float(row[13])) \
            .field("PDIC14010/PID.MV#Value",float(row[14])) \
            .field("PDIC14010/PID.PV_Out#Value",float(row[15])) \
            .field("PDIC14010/PID.SP#Value",float(row[16])) \
            .field("PI14012/MonAnalog.PV_Out#Value",float(row[17])) \
            .field("YC23001/Valve$Analog.MV#Value",float(row[18])) \
            .field("YC22001/Valve$Analog.MV#Value",float(row[19])) \
            .field("YC21001/Valve$Analog.MV#Value",float(row[20])) \
            .field("FIC23002/PID.PV_Out#Value",float(row[21])) \
            .field("FIC23002/PID.MV#Value",float(row[22])) \
            .field("FIC23002/PID.SP#Value",float(row[23])) \
            .field("FIC22002/PID.MV#Value",float(row[24])) \
            .field("FIC22002/PID.PV_Out#Value",float(row[25])) \
            .field("FIC22002/PID.SP#Value",float(row[26])) \
            .field("FIC21002/PID.MV#Value",float(row[27])) \
            .field("FIC21002/PID.PV_Out#Value",float(row[28])) \
            .field("FIC21002/PID.SP#Value",float(row[29])) \
            .field("YS23004/Valve.Ctrl#Value",float(row[30])) \
            .field("YS22004/Valve.Ctrl#Value",float(row[31])) \
            .field("YS21004/Valve.Ctrl#Value",float(row[32])) \
            .field("LIC23002/PID.MV#Value",float(row[33])) \
            .field("LIC23002/PID.PV_Out#Value",float(row[34])) \
            .field("LIC23002/PID.SP#Value",float(row[35])) \
            .field("LIC22002/PID.MV#Value",float(row[36])) \
            .field("LIC22002/PID.PV_Out#Value",float(row[37])) \
            .field("LIC22002/PID.SP#Value",float(row[38])) \
            .field("LIC21002/PID.MV#Value",float(row[39])) \
            .field("LIC21002/PID.PV_Out#Value",float(row[40])) \
            .field("LIC21002/PID.SP#Value",float(row[41])) \
            .field("YC23006/Valve$Analog.MV#Value",float(row[42])) \
            .field("YC22006/Valve$Analog.MV#Value",float(row[43])) \
            .field("YC21006/Valve$Analog.MV#Value",float(row[44])) \
            .field("PL2350/DriveSpeedContr.RbkOut#Value",float(row[45])) \
            .field("PL2350/DriveSpeedContr.FbkFwdOut#Value",float(row[46])) \
            .field("PL2350/DriveSpeedContr.FbkRevOut#Value",float(row[47])) \
            .field("PL2250/DriveSpeedContr.RbkOut#Value",float(row[48])) \
            .field("PL2250/DriveSpeedContr.FbkFwdOut#Value",float(row[49])) \
            .field("PL2250/DriveSpeedContr.FbkRevOut#Value",float(row[50])) \
            .field("PL2150/DriveSpeedContr.RbkOut#Value",float(row[51])) \
            .field("PL2150/DriveSpeedContr.FbkFwdOut#Value",float(row[52])) \
            .field("PL2150/DriveSpeedContr.FbkRevOut#Value",float(row[53])) \
            .field("YS23012/Vlv2WayL.CtrlV0#Value",float(row[54])) \
            .field("YS23012/Vlv2WayL.CtrlV1#Value",float(row[55])) \
            .field("YS23012/Vlv2WayL.CtrlV2#Value",float(row[56])) \
            .field("YS22012/Vlv2WayL.CtrlV0#Value",float(row[57])) \
            .field("YS22012/Vlv2WayL.CtrlV1#Value",float(row[58])) \
            .field("YS22012/Vlv2WayL.CtrlV2#Value",float(row[59])) \
            .field("YS21012/Vlv2WayL.CtrlV0#Value",float(row[60])) \
            .field("YS14004/Valve.Ctrl#Value",float(row[61])) \
            .field("PIC14007/PID.MV#Value",float(row[62])) \
            .field("PIC14007/PID.PV_Out#Value",float(row[63])) \
            .field("PIC14007/PID.SP#Value",float(row[64])) \
            .field("YC14008/Valve$Analog.Ctrl#Value",float(row[65])) \
            .field("PI10003/MonAnalog.PV_Out#Value",float(row[66])) \
            .field("YS10004/Valve.Ctrl#Value",float(row[67])) \
            .field("DeviationID/DeviationID.PV#Value",float(row[68])) \
            .field("YS10008/Valve.Ctrl#Value",float(row[69])) \
            .field("YS11004/Valve.Ctrl#Value",float(row[70])) \
            .field("YS14010/Valve.Ctrl#Value",float(row[71])) \
            .field("YS14011/Valve.Ctrl#Value",float(row[72])) \
            .field("YS14003/Valve.Ctrl#Value",float(row[73])) \
            .field("YS14005/Valve.Ctrl#Value",float(row[74])) \
            .field("FIC33004/FI.PV_Out#Value",float(row[75])) \
            .field("YS21012/Vlv2WayL.CtrlV1#Value",float(row[76])) \
            .field("YS21012/Vlv2WayL.CtrlV2#Value",float(row[77])) \
            .field("SFC_Dreitank_StepNo/CuStepNo.PV#Value",float(row[78])) \
            .time(row[79])
        write_api.write(bucket=bucket, org=org, record=p)

write_api.close()
client.close()
cursor.close()
end=datetime.datetime.now()
print('Elapsed {}'.format(end-start))
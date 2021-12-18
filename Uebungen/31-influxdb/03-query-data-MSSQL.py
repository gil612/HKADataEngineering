import pyodbc
import datetime

server = 'md2c0gdc' 
database = 'HSKA_Anlagenschema' 
username = 'sa' 
password = 'KWmz6QOHDPLIPqzJD9t2' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# read all data from DB ordered by time
start=datetime.datetime.now()
cursor.execute("""SELECT *
  FROM [HKA_SmA].[dbo].[timeseries_SmAKheDreiTankAllVariables]
  ORDER BY [timestamp]""")
row=cursor.fetchall()
end=datetime.datetime.now()
print('Elapsed: {}'.format(end-start))
print('Done')

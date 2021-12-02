import pyodbc
import pandas as pd

def get_datapoints(config,function_id:int)->pd.DataFrame:
    drv = pyodbc.drivers()
    DRIVER_NAME=drv[3]
    SQL_STR="Driver={"+DRIVER_NAME+"};SERVER="+config['SERVER']+';DATABASE='+config['DBSRC']+';UID='+config['UID']+';PWD='+config['PWD']
    cnxn=pyodbc.connect(SQL_STR)
    SQL="""SELECT [x],[y] FROM [dbo].[datapoints]
            WHERE [FunctionId]={}
            ORDER BY [x]
        """.format(function_id)
    df=pd.read_sql(SQL,cnxn)
    cnxn.close()
    return df

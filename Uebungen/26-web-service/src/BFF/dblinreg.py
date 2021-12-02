# retrieve results from db linear regression

from typing import List
import pyodbc
LStr=List[str]

def get_functions(config)->LStr:
    # check if db exists
    fnc=[]
    rmse=[]
    if exists_db(config):
        drv=pyodbc.drivers()
        DRIVER_NAME=drv[3]
        SQL_STR="Driver={"+DRIVER_NAME+"};SERVER="+config['SERVER']+';DATABASE='+config['DBLINREG']+';UID='+config['UID']+';PWD='+config['PWD']
        cnxn=pyodbc.connect(SQL_STR)
        cursor=cnxn.cursor()
        for row in cursor.execute("SELECT [FunctionId],[function],[RMSE] FROM [dbo].[linregresult] WHERE [ready]=1").fetchall():
            fnc.append('{}: {}'.format(row[0],row[1]))
            rmse.append('{}: {}'.format(row[0],row[2]))
    return fnc,rmse

def exists_db(config)->bool:
    drv=pyodbc.drivers()
    DRIVER_NAME=drv[3]
    SQL_STR="Driver={"+DRIVER_NAME+"};SERVER="+config['SERVER']+';UID='+config['UID']+';PWD='+config['PWD']
    cnxn=pyodbc.connect(SQL_STR, autocommit=True)
    cursor=cnxn.cursor()
    # check if db exists
    SQL_QUERY="SELECT COUNT(name) FROM sys.databases WHERE name='{}'".format(config['DBLINREG'])
    cursor.execute(SQL_QUERY)
    cnt=cursor.fetchone()
    return not (cnt[0]==0)
from typing import List
import numpy as np
import pyodbc

from Functions import Functions

# define list of functions as type (for better IDE-Support)
LFunctions=List[Functions]

def create_db(config)->bool:
    drv=pyodbc.drivers()
    DRIVER_NAME=drv[3]
    SQL_STR="Driver={"+DRIVER_NAME+"};SERVER="+config['SERVER']+';UID='+config['UID']+';PWD='+config['PWD']
    cnxn=pyodbc.connect(SQL_STR, autocommit=True)
    cursor=cnxn.cursor()
    # check if db exists
    SQL_QUERY="SELECT COUNT(name) FROM sys.databases WHERE name='{}'".format(config['DATABASE'])
    cursor.execute(SQL_QUERY)
    cnt=cursor.fetchone()
    if cnt[0] == 0:
        # create db
        SQL_QUERY = "CREATE DATABASE [{}]".format(config['DATABASE'])
        cursor.execute(SQL_QUERY)
        cnxn.close()
        # create tables
        create_table_functions(config)
        fill_function_db(config)
        return True
    return False

def create_table_functions(config):
    drv=pyodbc.drivers()
    DRIVER_NAME = drv[3]
    SQL_STR="Driver={"+DRIVER_NAME+"};SERVER="+config['SERVER']+';DATABASE='+config['DATABASE']+';UID='+config['UID']+';PWD='+config['PWD']
    cnxn=pyodbc.connect(SQL_STR, autocommit=True)
    cursor=cnxn.cursor()
    # table "functions" describes the available functions
    SQL_QUERY="""CREATE TABLE [dbo].[Functions](
        [Id] [int] IDENTITY(1,1) NOT NULL,
        [Name] [nvarchar](max) NOT NULL,
        [Description] [nvarchar](max) NULL
        )
        """
    cursor.execute(SQL_QUERY)
    # table "datapoints" contains x and y-data points
    SQL_QUERY="""CREATE TABLE [dbo].[datapoints](
        [Id] [int] IDENTITY(1,1) NOT NULL,
        [FunctionId] [int] NOT NULL,
        [x] [float] NOT NULL,
        [y] [float] NOT NULL
        )
        """
    cursor.execute(SQL_QUERY)
    cnxn.commit()
    cnxn.close()

def fill_function_db(config):
    drv=pyodbc.drivers()
    DRIVER_NAME=drv[3]
    SQL_STR="Driver={"+DRIVER_NAME+"};SERVER="+config['SERVER']+';DATABASE='+config['DATABASE']+';UID='+config['UID']+';PWD='+config['PWD']
    cnxn=pyodbc.connect(SQL_STR, autocommit=True)
    cursor=cnxn.cursor()
    # function 1: y=3*x+4
    cursor.execute("INSERT INTO Functions(Name,Description) VALUES (?,?)","y=3*x+4","linear function")
    # function 2: y=3*x^2-1
    cursor.execute("INSERT INTO Functions(Name,Description) VALUES (?,?)","y=3*x^2+1","quadratic function")
    # function 3: y=2*(x+1)**3+3
    cursor.execute("INSERT INTO Functions(Name,Description) VALUES (?,?)","y=2*(x+1)**3+3","cubic function")
    # insert data points for function 1
    functionId=cursor.execute("SELECT Id FROM Functions WHERE Name='y=3*x+4'").fetchone()[0]
    xv=np.linspace(-5.0,10,num=1000)
    for x in xv:
        y=3*x+4
        cursor.execute("INSERT INTO datapoints(FunctionId,x,y) VALUES (?,?,?)",functionId,x,y)
    # insert data points for function 2
    functionId=cursor.execute("SELECT Id FROM Functions WHERE Name='y=3*x^2+1'").fetchone()[0]
    xv=np.linspace(-7.0,6,num=2000)
    for x in xv:
        y=3*x**2+1
        cursor.execute("INSERT INTO datapoints(FunctionId,x,y) VALUES (?,?,?)",functionId,x,y)
    # insert data points for function 3
    functionId=cursor.execute("SELECT Id FROM Functions WHERE Name='y=2*(x+1)**3+3'").fetchone()[0]
    xv=np.linspace(-4.0,3.0,num=1500)
    for x in xv:
        y=2*(x+1.0)**3.0+3.0
        cursor.execute("INSERT INTO datapoints(FunctionId,x,y) VALUES (?,?,?)",functionId,x,y)
    cnxn.commit()
    cnxn.close()

def get_functions_db(config)->LFunctions:
    drv=pyodbc.drivers()
    DRIVER_NAME=drv[3]
    SQL_STR="Driver={"+DRIVER_NAME+"};SERVER="+config['SERVER']+';DATABASE='+config['DATABASE']+';UID='+config['UID']+';PWD='+config['PWD']
    cnxn=pyodbc.connect(SQL_STR)
    cursor=cnxn.cursor()
    functions=[]
    for rows in cursor.execute("SELECT * FROM Functions").fetchall():
        functions.append(Functions(rows[0],rows[1],rows[2]))
    return functions


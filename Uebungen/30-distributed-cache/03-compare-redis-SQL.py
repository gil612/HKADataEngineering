import redis
import pyodbc
import datetime
import random

# parameters for MSSQL
server = 'md2c0gdc' 
database = 'HKA_DC' 
username = 'sa' 
password = 'KWmz6QOHDPLIPqzJD9t2' 
# open connection
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

def SetSQL(key,value)->bool:
    exists=cursor.execute("SELECT TOP 1 Id FROM [HKA_DC_Test] WHERE Id=?",key).fetchone()
    if exists is None:
        cursor.execute(
            """INSERT INTO [HKA_DC_Test] (Id, Value,ExpiresAtTime) VALUES ('{}',CONVERT(varbinary,'{}'),'2021-12-17')"""
            .format(key,value))
        cursor.commit()

def GetSQL(key)->str:
    value=cursor.execute("""
        SELECT Value FROM [HKA_DC_Test] WHERE Id=?""",key).fetchone()
    if not value:
        raise 'Failed to read from MS SQL Server.'
    return value[0]

# instantiate connection to redis
r=redis.Redis(host='localhost', port=6379, db=0)

# write once and retrieve 10000 times
success=r.set('1','test')
if not success:
    raise 'Failed to write to memurai (redis derivate) cache.'
start=datetime.datetime.now()
for i in range(10000):
    success=r.get('1')
    if not success:
        raise 'Failed to read from redis cache.'
end=datetime.datetime.now()
elReadRedisSmall=end-start
print('Reading small chunks from memurai (redis derivate): {}'.format(elReadRedisSmall))

# write once to SQL server and read 10000 times
SetSQL('1','test')

start=datetime.datetime.now()
for i in range(10000):
    GetSQL('1')
end=datetime.datetime.now()
elReadSQLSmall=end-start
print('Reading small chunks from MS SQL: {}'.format(elReadSQLSmall))

# set and get 10000 random entries with redis
start=datetime.datetime.now()
for i in range(10000):
    hash=random.getrandbits(128)
    success=r.set(str(hash),str(hash))
    if not success:
        raise 'Failed to write to redis cache.'
    value=r.get(str(hash))
end=datetime.datetime.now()
elReadWriteRedisSmall=end-start
print('Writing/reading small random chunks from memurai (redis derivate): {}'.format(elReadWriteRedisSmall))

# set and get 10000 random entries with SQL
start=datetime.datetime.now()
for i in range(10000):
    hash=random.getrandbits(128)
    SetSQL(str(hash),str(hash))
    value=GetSQL(str(hash))
end=datetime.datetime.now()
elReadWriteSQLSmall=end-start
print('Writing/reading small random chunks from SQL: {}'.format(elReadWriteSQLSmall))

# set and get large random entries for memurai (redis derivate)
print('Writing and reading large random chunks to/from memurai (redis derivate):')
d=10
while True:
    start=datetime.datetime.now()
    key=random.getrandbits(128)
    hash=random.getrandbits(int(d))
    success=r.set(str(key),hash)
    if not success:
        raise 'Failed to write to redis cache.'
    value=r.get(str(hash))
    end=datetime.datetime.now()
    print('{}\t{}'.format(int(d),end-start))
    elReadWriteRedisLarge=end-start
    dRedis=int(d)
    d*=1.2
    if (end-start)>datetime.timedelta(seconds=30):
        break

# set and get large random entries for redis for SQL
print('Writing and reading large random chunks to/from SQL:')
d=10
while True:
    start=datetime.datetime.now()
    key=random.getrandbits(128)
    hash=random.getrandbits(int(d))
    SetSQL(str(key),str(hash))    
    value=GetSQL(str(key))
    end=datetime.datetime.now()
    print('{}\t{}'.format(int(d),end-start))
    elReadWriteSQLLarge=end-start
    dSQL=int(d)
    d*=1.2
    if (end-start)>datetime.timedelta(seconds=30):
        break

print('')
print('########## Summary #########')
print('Test                     SQL          \tmemurai')
print('Read small chunks        {} \t{}'.format(elReadSQLSmall,elReadRedisSmall))
print('Read/write small chunks  {} \t{}'.format(elReadWriteSQLSmall,elReadWriteRedisSmall))
print('I/O large > 30 s,        {} \t{}'.format(elReadWriteSQLLarge,elReadWriteRedisLarge))
print('          data size      {} \t{}'.format(dSQL,dRedis))
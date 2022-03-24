# DFTOPO

### How to Install
```
pip install dftopo
```

### Import into your code
```
from dftopo import dfps
```

## Examples
### Connection.
```
dbname='your_dbname'
user='your_user'
password='your_password'
host='your_host'
port='your_port'
schema='your_schema1,your_schema2'

engine = dfps.connection(dbname,user,password,host,port,schema)
```

### Pure SQL. 
```
query = f"""
    SELECT * FROM your_schema1.your_table
    """

list(dfps.query_execution(query, engine))
```

### Read data from postgres in python. 
```
query = f"""
    SELECT * FROM your_schema2.your_table
    """

df = dfps.read(query, engine)
```
### Load data from python to Postgres. 
```
dfps.load(df,"test2", engine,'your_schema1')
dfps.load(df,"test2", engine,'your_schema2')
```

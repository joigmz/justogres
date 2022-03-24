# Usage
## 1. Create client object
```
psql = clientPsql(
        host = <your host>,
        user = <your user>,
        password = <your password>,
        port=<your port (optional)>,
        db_name=<your database name>,
    )
```
## 2. select read or insert method
### 2.1 read() -> return pandas.DataFrame object
```
df = psql.read(<your sql query>,<chunksize (optional)>)
```

### 2.2 insert() -> return None
```
psql.insert(
    <your pd.DataFrame object>,
    table_name=<your table name>, #if doesn't exist, will be created
    schema=<your schema name>, #should be created previously
    chunksize=<your chunksize to load (default: 1000)>)
```

## Examples:
### init client
```
psql = clientPsql(
        host = os.environ.get("host_justo_pg"),
        user = os.environ.get("username_justo_pg"),
        password = os.environ.get("password_justo_pg"),
        port=os.environ.get("port_justo_pg"),
        db_name='postgres',
    )
```
### if we are gonna read
```
q="""SELECT * 
FROM schema_name.table_name;
"""
df = psql.read(query=q)
```

### if we are gonna insert
```
df = pd.read_csv('example.csv')
psql.insert(
    df,
    table_name='test_table',
    schema='test_schema',
    )
```
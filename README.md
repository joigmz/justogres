# Install
```
pip install justogres
```

# Usage
## 0. import 
```
from justogres import clientPsql
```
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
## 2. execute query or insert method
### 2.1 exec_query()
```
psql.exec_query(
    <your sql query>,
    chunksize = <chunksize (optional)>)
```
#### if query return something, method return pandas.Dataframe object

### 2.2 insert() -> return None
```
psql.insert(
    <your pd.DataFrame object>,
    table_name=<your table name>, #if doesn't exist, will be created
    schema=<your schema name>, #should be created previously
    chunksize=<your chunksize to load (default: 1000)>)
```

# Examples:
### first we must init client
```
from justogres import clientPsql

psql = clientPsql(
        host = os.environ.get("host_justo_pg"),
        user = os.environ.get("username_justo_pg"),
        password = os.environ.get("password_justo_pg"),
        port=os.environ.get("port_justo_pg"),
        db_name='postgres',
    )
```
### Then follow this options:
#### 1.if we are gona execute query
```
q="""DELETE 
    FROM schema_name.table_name 
    WHERE column_name='value';"""
psql.exec_query(q)
```
#### 1.1 (special case) if we are gonna read
```
q="""SELECT * 
    FROM schema_name.table_name;"""
df = psql.read(q)
```
optional: read with pandas library
```
q="""SELECT * 
    FROM schema_name.table_name;"""
df = psql.read_with_pandas(q)
```

#### 2. if we are gonna insert
```
df = pd.read_csv('example.csv')
psql.insert(
    df,
    table_name='test_table',
    schema='test_schema',
    )
```

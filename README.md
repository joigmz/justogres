# Overview
Justogres is a connector to comunicate pandas.DataFrame objects with postgres database

# Quick start
for more details review [documentation](./docs/)

## Install or upgrade package
install:
```
pip install justogres
```
upgrade:
```
pip install justogres --upgrade
```
## Init module
```
from justogres import clientPsql

psql = clientPsql(
        host = "<your host>",
        user = "<your user>",
        password = "<your password>",
        db_name = "<your database name>",
    )
``` 
## Insert data into postgres
```
import pandas as pd
example_df = pd.DataFrame(data=example_data)

psql.insert(
    example_df,
    table_name=<your table name>, #if doesn't exist table, will be created
    schema=<your schema name>, #should be created previously
    
    #optional
    chunksize=<your chunksize to load (default: 1000)>,
    column_types={<name_column_df>:<data_type postgres>})# if not declare column types, will be assigned automatically
```

## Read table of postgres
we have 2 ways to read DB, both return pandas.DataFrame object but its main difference is the type of data that is assigned to the columns of the dataframe
### 1. use exec_query() -> all columns are defines as object (string datatype in pandas)
```
query_example_to_read="""SELECT * 
    FROM schema_name.table_name;"""

df = psql.exec_query(
    query_example_to_read,

    #optional
    chunksize=<your chunksize to load (default: 1000)>
    )
```

### 2. use read_with_pandas() -> columns are defined with datatype declare for each column into DB
```
query_example_to_read="""SELECT * 
    FROM schema_name.table_name;"""

df = psql.read_with_pandas(
    query_example_to_read,

    #optional
    **kwargs=<all attributes we can use with pandas.read_sql()>
    )
```
for more info of [pandas.read_sql()](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html)

## Execute sql queries
this method doesn't return anything
```
query_example="""DELETE 
    FROM schema_name.table_name 
    WHERE column_name='value';"""

psql.exec_query(
    query_example,
    #optional
    chunksize=<your chunksize to load (default: 1000)>
    )
```
# Overview
here is a detailed description of the functions included in the module, to see details about the updates review [releases](releases.md)


# clientPsql (host:str, user:str, password:str, port:str='5432', db_name:str = 'postgres')
init class object, parameters:
- host: **string** with IP address or DNS
- user: **string** with user name which have access
- password: **string** with password of user
- port: (optional) **string** with the port through which the connection is made, by default is '5432'
- db_name: **string** with the name of database to connect

return None

## 1. clientPsql(...).exec_query( query, chunksize=1000)
function that allows executing SQL queries

parameters:
- query: **string** with SQL query to execute
- chunksize: **integer** with the length of rows that will be sent in the communication, by default your size is 1000  

return: DataFrame (only if it is a SELECT query, otherwise return None)

## 2. clientPsql(...).read_with_pandas(query,**kwargs)
exclusive function to read data from the database using pandas module, we can add any attribute of [pandas.read_sql()](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) in **kwargs

parameters:
- query: **string** with *SELECT* SQL query to execute

return: DataFrame

## 3. clientPsql(...).insert(df, table_name:str, schema:str='public', chunksize:int = 1000, column_types = {})
function to insert data from Dataframe to SQL table

parameters:
- df: **pandas.DataFrame** is a table with data to load into database
- table_name: **string** with the name of table to load data 
- schema: **string** with te schema name where is located the table, by default utilize *public* schema
- chunk_size: **integer** with the length of rows that will be sent in the communication, by default your size is 1000  
- column_types: (optional) **dictionary** with name columns and data types which we want load (by default the module will assign the data type), example:
    ```
    column_types={
        'name':'TEXT',
        'date':'TIMESTAMP',
        'price':'BIGINT',
        ...
        '<name_colum_df>':'<data_type_to_load_into_DB>',
    }
    ```
    *It is not necessary to add all the columns, only those that we are interested in modifying their data type assigned by default*

return: None

## 4. clientPsql(...).get_engine():
funtion that return psycopg2.connector object, this is utilized how attribute of methods in other modules as *sqlalchemy* or *pandas*

parameters: None

return: psycopg2.connect() object
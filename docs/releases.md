# 3.0.1
### add method:
- read_with_pandas()
    - parameters:
        - query: (string) select sql query 
        - **kwargs: parameters of [pandas.read_sql()](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html)
    - return: pandas.DataFrame object
### add feature:
- add attribute column_types on insert() to choose data type of each column (optional)
    - add parameters:
        - (optional) column_types: dict with {name_column : type_on_db,...} ,default = {}
    - return: none
### fix bug:
- fix raise error when select query no return data, now return empty dataframe with your columns

# 3.0.0
### add methods:
- insert()
    - parameters:
        - df: pandas.Dataframe object to insert, 
        - table_name: string with table name, 
        - (optional) schema: string with schema name, default = 'public'
        - (optional) chunksize: integer , default = 1000
    - return: none
- exec_query():
    - parameters:
        - query: string with sql query
        - (optional) chunksize: integer , default = 1000

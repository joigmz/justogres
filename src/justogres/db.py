import os
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import register_adapter,AsIs
import numpy as np
import pandas as pd
#from metrics import profile

class clientPsql():
    def __init__(
        self,
        host:str,
        user:str,
        password:str,
        port:str='5432',
        db_name:str = 'postgres'
        ) -> None:

        #credentials
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port=port
        self.database=db_name
        #register adapters
        register_adapter(np.int64,AsIs)
        register_adapter(np.bool_,AsIs)

    #@profile
    def read(
        self,
        query,
        chunksize=1000
        ):

        try:
            conn = psycopg2.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.database,
                )
            with conn.cursor() as cur:
                cur.itersize = chunksize
                cur.execute(query)
                column_name = [desc[0] for desc in cur.description]
                response = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as e:
            print ('Error reading...',e)
            column_name = None
            response = None
        finally:
            
            if conn is not None:
                conn.close()
                return pd.DataFrame(np.array(response),columns=column_name)
    
    def create_staging_table(
        self,
        cursor,
        table_name:str, 
        schema:str='public',
        data_types=dict
        ) -> None:

        query = f"""CREATE UNLOGGED TABLE IF NOT EXISTS {schema}.{table_name}
        ({','.join(map_column_types(data_types))});"""
        cursor.execute(query)
    
    #@profile
    def insert (
        self,
        df, 
        table_name:str, 
        schema:str='public', 
        chunksize:int = 1000
        )->None:

        try:
            conn = psycopg2.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.database,
                )
            with conn.cursor() as cur:
                self.create_staging_table(
                    cur,
                    table_name=table_name,
                    schema=schema,
                    data_types=df.dtypes.to_dict()
                    )
                
                if 'Unnamed: 0' in df.columns.tolist():
                    execute_values(
                        cur,
                        f'INSERT INTO {schema}.{table_name} VALUES %s;',
                        (values[1:] for values in df.values.tolist()),
                        page_size=chunksize
                        )
                else:
                    execute_values(
                        cur,
                        f'INSERT INTO {schema}.{table_name} VALUES %s;',
                        (values for values in df.values.tolist()),
                        page_size=chunksize
                        )
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as e:
            print ('Error while insert...',e)
            conn=None
            
        finally:
            if conn is not None:
                conn.close()

def map_type(var):
    numpy_to_psql = {
        'int64' :'INT',
        'object':'TEXT',
        'float64':'NUMERIC',
        'bool': 'BOOLEAN',
        'datetime64[ns]':'TIMESTAMP',
        'timedelta[ns]':'NUMERIC',
        }
    if var.name in numpy_to_psql.keys():
        return numpy_to_psql[var.name]
    else:
        return 'TEXT'

def map_column_types(data_types: dict):
    return [f'{key}  {map_type(value)}' for key,value in data_types.items() if key!='Unnamed: 0']

if __name__=='__main__':    
    
    
    pass
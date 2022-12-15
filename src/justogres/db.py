import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import register_adapter,AsIs
import numpy as np
import pandas as pd
from .utils import map_column_types

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
        register_adapter(pd._libs.missing.NAType, lambda i: AsIs('NULL'))


    def exec_query(
        self,
        query,
        chunksize=1000
        ):
        column_name = None
        response = None
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
                if cur.description:
                    column_name = [desc[0] for desc in cur.description]
                    response = cur.fetchall()
                conn.commit()


        except (Exception, psycopg2.DatabaseError) as e:
            print ('Error executing query: ',e)
            conn = None
        finally:
            if conn is not None:
                conn.close()
            if column_name is not None:
                try:
                    return pd.DataFrame(np.array(response),columns=column_name)
                except: 
                    return pd.DataFrame(columns=column_name)
    
    def create_staging_table(
        self,
        cursor,
        table_name:str, 
        schema:str='public',
        data_types=dict,
        column_types = {}
        ) -> None:

        query = f"""CREATE UNLOGGED TABLE IF NOT EXISTS {schema}.{table_name}
        ({','.join(map_column_types(data_types,column_types))});"""
        cursor.execute(query)
    
    def insert (
        self,
        df, 
        table_name:str, 
        schema:str='public', 
        chunksize:int = 1000,
        column_types = {}
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
                    data_types=df.dtypes.to_dict(),
                    column_types=column_types
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

    ############## PANDAS METHODS #####################
    def get_engine(self):
        return psycopg2.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.database,
                )

    def read_with_pandas(self,query,**kwargs):
        return pd.read_sql(query,self.get_engine(),**kwargs)

if __name__=='__main__':    
    pass
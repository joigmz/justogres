import pandas as pd
from sqlalchemy import create_engine

def connection(dbname,user,password,host,port,schema):
    options=f"-c search_path={schema}"

    engine = create_engine('postgresql+psycopg2://'+user+':'+password+'@'+host+':'+port+'/'+dbname, echo=False,
                        connect_args={'options': options})
    return engine

def read(query, engine):
 return pd.read_sql(query, engine)

def load(df,table_name, engine, schema):
    return df.to_sql(table_name, con=engine, if_exists='append', schema=schema, index=False)

def query_execution(query, engine):
    with engine.connect() as con:
        return con.execute(query)
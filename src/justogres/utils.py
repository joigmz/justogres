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

def map_column_types(data_types: dict,column_type={}):
    result=[]
    for key,value in data_types.items():
        if key=='Unnamed: 0':
            pass
        else:
            if key in list(column_type.keys()):
                result.append(f'{key}  {column_type[key]}')
            else:
                result.append(f'{key}  {map_type(value)}')

    return result
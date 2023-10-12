import psycopg2
from datetime import datetime
import json
from shree_cement.local_settings import *

def connect_db():
    
    cnxn = psycopg2.connect(
        host=SERVER,
        database=DATABASE_NAME,
        user=USERNAME,
        password=PASSWORD)

    return cnxn

def createorupdate(df,table,condition_col,pk,cnxn):
    
    cols_dt = df.select_dtypes('datetime64').columns.tolist()
    cols_str = df.select_dtypes('object').columns.tolist()

    for col_str in cols_str:
        df[col_str] = df[col_str].str.replace("\\", '')
        df[col_str] = df[col_str].str[:200]
    
    for col_dt in cols_dt:
        df[col_dt] = df[col_dt].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
    
    df = df.to_dict('split')
    
    val = ','.join(str(tuple(i)) for i in df['data'])
    # with open('val_json.json','w') as fp:
    #     json.dump({'val':val},fp)

    col = ','.join(f'"{i}"' for i in df['columns'])

    col_update = []
    col_select = []
    col_ins = []

    for i in df['columns']:
        if i != condition_col:
            if i in cols_dt:
                col_update.append(f'"{i}"=nv."{i}"::timestamp')
            else:
                col_update.append(f'"{i}"=nv."{i}"')

    for i in df['columns']:
        if i != pk:
            col_ins.append(f'"{i}"')
            if i in cols_dt:
                col_select.append(f'"{i}"::timestamp')
            else:
                col_select.append(f'"{i}"')
    
    col_update = ','.join(col_update)
    col_select = ','.join(col_select)
    col_ins = ','.join(col_ins)

    # col_update = ','.join(f'"{i}"=nv."{i}"' if i != condition_col else '' for i in df['columns']).strip(',')

    sql = f'''
        WITH new_values ({col}) as (
        values 
            {val}
        ),
        upsert as
        ( 
            update etl_zone."{table}" m 
                set {col_update}
            FROM new_values nv
            WHERE m."{condition_col}" = nv."{condition_col}"
            RETURNING m.*
        )
        INSERT INTO etl_zone."{table}" ({col_ins})
        SELECT {col_select}
        FROM new_values
        WHERE NOT EXISTS (SELECT 1 
                        FROM upsert up 
                        WHERE up."{condition_col}" = new_values."{condition_col}")
    '''

    sql = sql.replace('None','NULL')
    sql = sql.replace('nan','NULL')
    
    crsr = cnxn.cursor()

    crsr.execute(sql)
    crsr.close()

    cnxn.commit()

    return 0

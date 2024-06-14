import pandas as pd
from sqlalchemy import inspect
import numpy as np
import traceback
from utils import html_render,get_global,staff_kyntus_dir,high_red,high_red_evo,grouping,df_cleaning
from db import create_engine_
def onemonth_table(group):
    db_name = 'ind'
    engine = engine = create_engine_(db_name)
    inspector = inspect(engine)
    #query="SELECT * FROM `satcli` WHERE YEAR(STR_TO_DATE(`Visit date`, %s)) = YEAR(NOW()) and `GROUP` = %s;"

    query='SELECT * FROM `satcli` WHERE STR_TO_DATE(`Visit date`, %s) BETWEEN DATE_SUB((SELECT MAX(STR_TO_DATE(`Visit date`, %s)) FROM `satcli`) , INTERVAL 2 MONTH) AND (SELECT MAX(STR_TO_DATE(`Visit date`, %s)) FROM `satcli`) and DATE(STR_TO_DATE(`Visit date`, %s)) < Date(NOW()) AND `GROUP` = %s;'
    params = ('%d/%m/%Y %H:%i:%s','%d/%m/%Y %H:%i:%s','%d/%m/%Y %H:%i:%s','%d/%m/%Y %H:%i:%s',group)
    satcli_res = pd.read_sql(query, con=engine, params=params)


    db_name = 'contrat_q'
    engine = engine = create_engine_(db_name)
    inspector = inspect(engine)


    #query="SELECT * FROM `list_int`  WHERE YEAR(STR_TO_DATE(`Début du RDV`, %s)) = YEAR(NOW()) and `list_int`.`Typologie RDV` LIKE %s; "

    query='SELECT * FROM `list_int` WHERE STR_TO_DATE(`Début du RDV`, %s) BETWEEN DATE_SUB((SELECT MAX(STR_TO_DATE(`Début du RDV`, %s)) FROM `list_int`) , INTERVAL 2 MONTH) AND (SELECT MAX(STR_TO_DATE(`Début du RDV`, %s)) FROM `list_int`) AND `Typologie RDV` LIKE %s;'
    params = ('%Y-%m-%d %H:%i:%s','%Y-%m-%d %H:%i:%s','%Y-%m-%d %H:%i:%s',f'{group}%')

    #params = ('%Y-%m-%d %H:%i:%s',f'{group}%')
    tecnow_res = pd.read_sql(query, con=engine, params=params)
    merged = pd.merge(satcli_res, tecnow_res, left_on='ID RDV', right_on='Id RDV', how='outer')
    merged['Date'] = merged['Visit date'].fillna(merged['Début du RDV'])
    merged['ID RDV'].fillna(merged['Id RDV'],inplace=True)
    merged['Département'].fillna(merged['Department'],inplace=True)
    merged['Date'] = pd.to_datetime(merged['Date'], format="%d/%m/%Y %H:%M",dayfirst=True, errors='coerce')
    #merged['Date'] = pd.to_datetime(merged['Date'], format="%Y-%m-%d %H:%M",dayfirst=True, errors='coerce')

    merged['Month_Num'] = merged['Date'].dt.strftime('%m')
    grouped=merged.groupby('Month_Num')
    # Reset the index if needed
    #grouped.reset_index(inplace=True)


    staff_kyntus = pd.read_excel(staff_kyntus_dir)
    res = pd.DataFrame()
    res = grouping(grouped,"Month")
    

    res=df_cleaning(res)
    return html_render(res)
    # Print the modified HTML
    #print(modified_html)



#onemonth_table('RACC')
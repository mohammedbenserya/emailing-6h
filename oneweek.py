import pandas as pd
from sqlalchemy import inspect
import numpy as np
from utils import html_render,get_global,staff_kyntus_dir,high_red,high_red_evo,grouping,df_cleaning
from db import create_engine_
def oneweek_table(group):
    db_name = 'ind'
    engine = create_engine_(db_name)
    inspector = inspect(engine)
    query="SELECT * FROM `satcli` WHERE ((STR_TO_DATE(`Visit date`, %s))) >= DATE_SUB((SELECT MAX(STR_TO_DATE(`Visit date`, %s)) FROM `satcli`), INTERVAL 4 WEEK) and DATE(STR_TO_DATE(`Visit date`, %s)) < Date(NOW()) and `GROUP` = %s;"
    params = ('%d/%m/%Y %H:%i:%s','%d/%m/%Y %H:%i:%s','%d/%m/%Y %H:%i:%s',group)
    satcli_res = pd.read_sql(query, con=engine, params=params)
    db_name = 'contrat_q'
    engine = create_engine_(db_name)
    inspector = inspect(engine)
    query="SELECT * FROM `list_int`  WHERE (STR_TO_DATE(`Début du RDV`, %s)) >= DATE_SUB((SELECT MAX(STR_TO_DATE(`Début du RDV`, %s)) FROM `list_int`), INTERVAL 4 WEEK) and `list_int`.`Typologie RDV` LIKE %s; "
    params = ('%Y-%m-%d %H:%i:%s','%Y-%m-%d %H:%i:%s',f'{group}%')
    tecnow_res = pd.read_sql(query, con=engine, params=params)
    merged = pd.merge(satcli_res, tecnow_res, left_on='ID RDV', right_on='Id RDV', how='outer')
    merged['Date'] = merged['Visit date'].fillna(merged['Début du RDV'])
    merged['ID RDV'].fillna(merged['Id RDV'],inplace=True)
    merged['Département'].fillna(merged['Department'],inplace=True)
    merged['Date'] = pd.to_datetime(merged['Date'], format="%d/%m/%Y %H:%M",dayfirst=True, errors='coerce')
    #merged['Date'] = pd.to_datetime(merged['Date'], format="%Y-%m-%d %H:%M",dayfirst=True, errors='coerce')
    #merged['Date'] = merged['Date'].dt.date

    #first_day_of_month = merged['Date'].min().replace(day=1)
    # Find the first day of the month
    #first_monday_of_month = first_day_of_month + pd.DateOffset(days=(7 - first_day_of_month.dayofweek) % 7)
    # Group by week, starting from the first day of the month
    grouped = merged.groupby(pd.Grouper(key='Date', freq='W-SUN'))#, origin=first_day_of_month))


    
    staff_kyntus = pd.read_excel(staff_kyntus_dir)


    res=pd.DataFrame()
    res = grouping(grouped,"Semaine")

    res=df_cleaning(res)

    return html_render(res)
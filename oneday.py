import pandas as pd
from sqlalchemy import inspect
import numpy as np
import traceback
from utils import html_render,get_global,staff_kyntus_dir,add_missing_ce,grouping,df_cleaning
from datetime import datetime, timedelta
from env import config
from db import create_engine_
def oneday_table(group):

    db_name = 'ind'
    engine = create_engine_(db_name)
    inspector = inspect(engine)
    # Check if today is Monday
    today = datetime.today()
    if today.weekday() == 0:  # Monday is 0 in the Python weekday() function
        # If today is Monday, subtract 1 week from the current date
        one_week_ago = today - timedelta(weeks=1)
        one_week_ago =  one_week_ago.strftime('%Y-%m-%d %H:%M:%S')
    else:
        one_week_ago = '(SELECT MAX(STR_TO_DATE(`Visit date`, %s)) AS max_date FROM `satcli`)'
        params = ('%d/%m/%Y %H:%i:%s',)
        maxdate=pd.read_sql(one_week_ago, con=engine, params=params)
        one_week_ago=maxdate.iloc[0]['max_date']
    # Define your SQL query and parameters
    query = "SELECT * FROM `satcli` WHERE YEARWEEK(STR_TO_DATE(`Visit date`, %s)) = YEARWEEK(%s)  and DATE(STR_TO_DATE(`Visit date`, %s)) < Date(NOW()) and `GROUP` = %s;"
    params = ('%d/%m/%Y %H:%i:%s',one_week_ago, '%d/%m/%Y %H:%i:%s', group)

    # Update the last parameter in the params tuple to use one_week_ago

    # Assuming you have the database connection engine defined as 'engine'
    satcli_res = pd.read_sql(query, con=engine, params=params)



    db_name = 'contrat_q'
    engine = engine = create_engine_(db_name)
    inspector = inspect(engine)
    query="SELECT * FROM `list_int` where  YEARWEEK(STR_TO_DATE(`Début du RDV`, %s)) = YEARWEEK((SELECT MAX(STR_TO_DATE(`Début du RDV`, %s)) FROM `list_int`)) and `list_int`.`Typologie RDV` LIKE %s;"
    params = ('%Y-%m-%d %H:%i:%s','%Y-%m-%d %H:%i:%s',f'{group}%')
    tecnow_res = pd.read_sql(query, con=engine, params=params) 

    merged = pd.merge(satcli_res, tecnow_res, left_on='ID RDV', right_on='Id RDV', how='outer')
    merged['Date'] = merged['Visit date'].fillna(merged['Début du RDV'])
    merged['ID RDV'].fillna(merged['Id RDV'],inplace=True)
    merged['Département'].fillna(merged['Department'],inplace=True)
    merged['Date'] = pd.to_datetime(merged['Date'], format="%d/%m/%Y %H:%M",dayfirst=True, errors='coerce')
    merged['Date'] = pd.to_datetime(merged['Date'], format="%Y-%m-%d %H:%M",dayfirst=True, errors='coerce')
    merged['Date'] = merged['Date'].dt.date
    grouped = merged.groupby('Date')
    

    staff_kyntus = pd.read_excel(staff_kyntus_dir)
    res = grouping(grouped,"Date")
    groups,missing_departments=add_missing_ce(merged,one_week_ago)
    week_sum=pd.DataFrame()
    groups = merged.groupby('Département')
    for name, group in groups:
        nan_count = group['Review'].isna().sum()
        total_count = len(group)
        ratio = (total_count - nan_count) / total_count if total_count > 0 else 0

        greater_than_4_count = (group['Review'] >= 4).sum()
        total_count = len(group)

        if total_count > 0:
            satcli_ratio = greater_than_4_count / (total_count - nan_count)
        else:
            satcli_ratio = 0

        try:
            cont = staff_kyntus[staff_kyntus['Département'] == int(name)]['Conducteur']
            #print(cont)
            
            cont = cont.iloc[0] if not cont.empty else ""
            if str(cont)==""  or str(cont) not in staff_kyntus['Conducteur'].values:
                continue
            ce = staff_kyntus[staff_kyntus['Département'] == int(name)]["Chef d'équipe"]
            ce = ce.iloc[0] if not ce.empty else ""
            data = {
                'Conducteur': [cont],
                "Chef d'équipe": [ce],
                'Département': [ f"{int(name)}"],
                'Nbr réponses': ["-" if name in missing_departments['Département'].values else  f"{int(total_count - nan_count)}" if not (total_count - nan_count)==0 and not np.isnan((total_count - nan_count)) else '-'],
                '%SATCLI': ["-" if name in missing_departments['Département'].values else  f"{satcli_ratio:.2%}" if not np.isnan(satcli_ratio) and not str(satcli_ratio)=='nan' else '-'],
                "Nbr d'inter": ["-" if name in missing_departments['Département'].values else  f"{int(total_count)}" if not total_count==0 and not np.isnan((total_count))  else '-'],
                "Tx de réponse": ["-" if name in missing_departments['Département'].values else  f"{ratio:.2%}" if not np.isnan(ratio) and not str(ratio)=='nan' else '-'],}

            # Apply conditional formatting to highlight '% SATCLI' values greater than 80
            #one_day = pd.DataFrame(data).drop_duplicates()
            temp = pd.DataFrame(data)
            week_sum = pd.concat([week_sum, temp], ignore_index=True)
            week_sum = week_sum.dropna(subset=['Conducteur'])
        except Exception as e:
                    traceback.print_exc()
                    pass
    if "Evolution" in week_sum.columns:
        week_sum = week_sum.drop('Evolution', axis=1)
    temp=get_global(merged)
    temp = temp.drop('Evolution', axis=1)
    week_sum = pd.concat([week_sum, temp], ignore_index=True)
    if not res.empty :
        week_sum.drop(columns=['Conducteur',"Chef d'équipe",'Département'], axis=1, inplace=True)
    else:
        first_three=week_sum[week_sum.columns[:3]]
        first_three.columns = [["Date"]*(len(first_three.columns)),first_three.columns]
        week_sum.drop(columns=['Conducteur',"Chef d'équipe",'Département'], axis=1, inplace=True)
        res = pd.concat([res, first_three], axis=1, sort=False)
    week_sum.columns = [["Cumul Semaine en cours"]*(len(week_sum.columns)),week_sum.columns]
    res = pd.concat([res, week_sum], axis=1, sort=False)
    res=df_cleaning(res)
    return html_render(res)

from bs4 import BeautifulSoup
import traceback
import pandas as pd
import numpy as np
from db import create_engine_
from pathlib import Path,os
from env import config
HOME_DIR=config('HOME_DIR',default=None)
home_dir = Path.home() / HOME_DIR
staff_kyntus_dir=home_dir /"resources"/"staff_kyntus.xlsx"
cc_path=home_dir /"resources"/"cc.txt"
to_path=home_dir /"resources"/"to.txt"
staff_kyntus = pd.read_excel(staff_kyntus_dir)


def html_render(res):
    html=res.to_html(classes='table-auto w-full border-collapse border border-gray-300',index=False)
    html = html.replace('<table', '<table class="w-full text-xs text-left" style="border-collapse: collapse;width: 100%;" ')
    html = html.replace('<tr>', '<tr style=" padding: 2px 2px; font-size: 12px; text-align: center;">')
    html = html.replace('<th', '<th style="border: 1px solid black; padding: 2px 2px; font-size: 14px; text-align: center;" ')
    html = html.replace('<td', '<td style="border: 1px solid black; padding: 2px 2px; font-size: 12px; text-align: center;" ')
    
    html=html.replace('<th style="border: 1px solid black; padding: 2px 2px; font-size: 14px; text-align: center;" ead>','<thead>')
    #html = html.replace('<tbody>', '</thead><tbody>" ')
    html=html.replace('</th></table>','</table>')
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody')
    total_rows = len(tbody.find_all('tr'))


    # Loop through each <tr> in the <tbody>
    for idx, tr in enumerate(tbody.find_all('tr')):
        if idx == total_rows - 1:
            # Skip the last <tr> entirely
            continue
        td_list = tr.find_all('td')
        existing_style = td_list[0].get('style', '')
        td_list[0]['style'] = f'{existing_style} ; border-left: 2px solid black; '
        existing_style = td_list[2].get('style', '')
        td_list[2]['style'] = f'{existing_style} ; border-right: 2px solid black; '
        existing_style = td_list[-1].get('style', '')
        td_list[-1]['style'] = f'{existing_style} ; border-right: 2px solid black;'
        for i in range(7, len(td_list), 5):
            existing_style = td_list[i].get('style', '')
            td_list[i]['style'] = f'{existing_style} ; border-left: 2px solid black; '
        

        
        
    # Find and remove all 'th' elements with class 'row_heading'
    for th in soup.find_all('th', class_=['row_heading', 'blank']):
        th.extract()
    for th in soup.find_all('th', ead=True):
        tr = th.find_parent('tr')
        if tr:
            tr.extract()
            th.extract()
    # Get the cleaned HTML table as a string
    style_element = soup.find('style')
    if style_element:
        css_rules = style_element.string.strip().split('}')
        css_dict = {}
        for rule in css_rules:
            if '{' in rule:
                selector, styles = rule.split('{')
                selector = selector.strip()
                styles = styles.strip()
                css_dict[selector] = styles

        # Find elements and apply CSS styling from the <style> element
        for selector, styles in css_dict.items():
            for element in soup.select(selector):
                element['style'] = styles

    # Get the modified HTML as a string
    tbody = soup.find('tbody')
    tr_elements = tbody.find_all('tr')

    for td in tr_elements[-1].find_all('td'):
            #border-left: 2px solid black;
            existing_style = td.get('style', '')
            td['style'] = f'{existing_style} ;border-width: 2px;'
    # Check if there are <tr> elements
    if tr_elements:
        # Get the last <tr> element
        last_tr = tr_elements[-1]

        # Get the first three <td> elements
        first_three_tds = last_tr.find_all('td', limit=3)

        # Extract all of the <td> elements from the last <tr> element except for the first one
        for td in first_three_tds[1:]:
            td.extract()

        # Set the colspan attribute of the first <td> element to 3
        first_three_tds[0]['colspan'] = 3

        # Append the text Total to the first <td> element
        first_three_tds[0].string.replace_with('Total')

        # Append the style to the existing style of the last <tr> element
        existing_style = last_tr.get('style', '')
        last_tr['style'] = f'{existing_style} font-size: 14px;'

        # Find all elements inside the last <tr> and append the style to their existing styles
        for element in last_tr.find_all():
            existing_element_style = element.get('style', '')
            element['style'] = f'{existing_element_style} font-size: 14px;'
        
    ''''''

    ##########################################################################################################

    soup =rowspaning(soup)
    


    thead = soup.find('thead')

    for tr in thead.find_all('tr'):
        for th in tr.find_all('th'):
            #border-left: 2px solid black;
            existing_style = th.get('style', '')
            th['style'] = f'{existing_style} ;border-width: 2px;'
    
    
    for idx, tr in enumerate(tbody.find_all('tr')):
        td_list = tr.find_all('td')
        existing_style = td_list[-1].get('style', '')
        td_list[-1]['style'] = f'{existing_style} ; border-right: 2px solid black;'



    modified_html = str(soup)
    

    return modified_html


def rowspaning(soup):
    groups = []
    # Iterate through the table rows.
    group=[]
    for tr in soup.find_all('tr'):

        td=tr.find_all('td')
        if td is None or len(td)<=1:
            continue
        td=td[1]
        #print(td)
        if len(group) > 0 and td.text == groups[-1][-1].text:
            # Add the current table cell to the current group.
            group.append(td)
        else:
            # Create a new group and add the current table cell to the new
            # group.
            group = [td]
            if len(group) > 0:
                groups.append(group) 
            

        # Add the current group to the list of groups.
    #pprint.pprint(groups)
    # Iterate through the list of groups.
    for group in groups:
        # Set the rowspan attribute of the first table cell in the group to
        # the number of table cells in the group.
        #group[0]['rowspan'] = str(len(group))
        #print(group[0].text,str(len(group)))
        first_td = soup.find('td', text=group[0].text)
        first_td['rowspan'] = str(len(group))
        # Remove all of the table cells in the group after the first table
        # cell.
        for td in group[1:]:
            td.extract()


    groups = []
    # Iterate through the table rows.
    group=[]
    for tr in soup.find_all('tr'):

        td=tr.find('td')
        if td is None:
            continue
        if len(group) > 0 and td.text == groups[-1][-1].text:
            # Add the current table cell to the current group.
            group.append(td)
        else:
            # Create a new group and add the current table cell to the new
            # group.
            group = [td]
            if len(group) > 0:
                groups.append(group) 
            

        # Add the current group to the list of groups.
    # Iterate through the list of groups.
    for group in groups:
        # Set the rowspan attribute of the first table cell in the group to
        # the number of table cells in the group.
        #group[0]['rowspan'] = str(len(group))
        first_td = soup.find('td', text=group[0].text)
        first_td['rowspan'] = str(len(group))
        # Remove all of the table cells in the group after the first table
        # cell.
        for td in group[1:]:
            td.extract()
    return soup

def get_global(groups,old_evo=None):
    nan_count = groups['Review'].isna().sum()
    total_count = len(groups)
    ratio = (total_count - nan_count) / total_count if total_count > 0 else 0

    greater_than_4_count = (groups['Review'] >= 4).sum()
    total_count = len(groups)

    if total_count > 0:
        satcli_ratio = greater_than_4_count / (total_count - nan_count)
    else:
        satcli_ratio = 0
    
    try:
        evo_val='-'

        if old_evo is not None:
            evo_val=round(satcli_ratio*100,2) - old_evo
            evo_val = '-' if evo_val == 0 or evo_val == 0 or np.isnan(evo_val) or str(
                        evo_val) == 'nan' else f"{round(evo_val,2)}%"

        data = {
            'Conducteur': ["Total"],
            "Chef d'équipe": [''],
            'Département': [ f""],
            'Nbr réponses': [f"{int(total_count - nan_count)}" if not (total_count - nan_count)==0 and not np.isnan((total_count - nan_count)) else '-'],
            '%SATCLI': [f"{satcli_ratio:.2%}" if not np.isnan(satcli_ratio) and not str(satcli_ratio)=='nan' else '-'],
            "Nbr d'inter": [f"{int(total_count)}" if not total_count==0 and not np.isnan((total_count))  else '-'],
            "Tx de réponse": [f"{ratio:.2%}" if not np.isnan(ratio) and not str(ratio)=='nan' else '-'],
            'Evolution': [evo_val]}

        # Apply conditional formatting to highlight '% SATCLI' values greater than 80
        #one_week = pd.DataFrame(data).drop_duplicates()
        temp = pd.DataFrame(data)
        return temp
    except Exception as e:
            traceback.print_exc()
            pass

def get_lastDate():
    db_name = 'contrat_q'
    
    engine = create_engine_(db_name)
    query = "SELECT DATE_FORMAT(MAX(STR_TO_DATE(`Début du RDV`, %s)), '%%d/%%m') FROM `list_int`"
    params = ('%Y-%m-%d %H:%i:%s',)
    last_date = pd.read_sql(query, con=engine, params=params)
    return last_date.values[0][0]


def high_red(val, value_max, value2, value3):
        if val == '-':
            return ' border: 1px solid black; text-align: center;'   # Add border styling
        if isinstance(val, float):
            val = 0
        else:
            val = float(val.replace('%', ''))
        
        if val >= value_max:
            return 'background-color: lightskyblue; border: 1px solid black; text-align: center;'  # Add border styling
        if (val >= value2) and (val < value_max):
            return 'background-color: green; border: 1px solid black; text-align: center;'  # Add border styling
        if (val >= value3) and (val < value2):
            return 'background-color: orange; border: 1px solid black; text-align: center;'  # Add border styling
        if val < value3:
            return 'background-color: red; border: 1px solid black; text-align: center;'
def high_red_evo(val):
        if val == '-':
            return ' border: 1px solid black; text-align: center;'   # Add border styling
        if isinstance(val, float):
            val = 0
        else:
            val = float(val.replace('%', ''))
        
        if val > 0:
            return 'color: green; border: 1px solid black; text-align: center;'  # Add border styling
        if val < 0:
            return 'color: red; border: 1px solid black; text-align: center;' 


def grouping(grouped,col_name):
    res=pd.DataFrame()
    is_first=True
    old_ratios={}
    old_g_evo=None
    staff_kyntus = pd.read_excel(staff_kyntus_dir)
    staff_kyntus['Département'] = staff_kyntus['Département'].astype(float)

    if col_name=='Month':
        #grouped = [group.sort_values(by='Date', ascending=False) for name, group in grouped]
        grouped=sort_months(grouped)
        grouped = list(grouped)[-2:]
    elif col_name=='Semaine':
        grouped = list(grouped)[-4:]
    for group_start, groups in grouped:
        if col_name =='Semaine':
            week_number = group_start.isocalendar()[1]
            key_s = f"S{week_number}" 
        elif col_name =='Month':
            french_month_names = [
                    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
                ]

            # Month number (1 for January, 2 for February, etc.)
            month_number = int(group_start)  # Change this to the desired month number

            # Get the French month name
            french_month = french_month_names[month_number - 1]

            month=french_month
            key_s=month
        else:
            key_s=group_start
        groups,missing_departments=add_missing_ce(groups,group_start)
        one_day = pd.DataFrame()
        total_grp = groups
        
        groups = groups.groupby('Département')
        old_evo = '-'
        
        print(key_s)
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

                cont = cont.iloc[0] if not cont.empty else ""
                if str(cont) == "" or str(cont) not in staff_kyntus['Conducteur'].values:
                    print(name,key_s)
                    continue

                ce = staff_kyntus[staff_kyntus['Département'] == int(name)]["Chef d'équipe"]
                ce = ce.iloc[0] if not ce.empty else ""
                evo_val='-'
                if str(name) in old_ratios.keys():
                    evo_val=satcli_ratio - old_ratios[str(name)]
                    evo_val = '-' if evo_val == 0 or np.isnan(evo_val) or str(
                        evo_val) == 'nan' else f"{round(evo_val*100,2)}%"

                    old_ratios[str(name)] = satcli_ratio
                else:
                    old_ratios[str(name)] = satcli_ratio
                
                data = {
                    'Conducteur': [cont],
                    "Chef d'équipe": [ce],
                    'Département': [f"{int(name)}"],
                    'Nbr réponses': ["-" if name in missing_departments['Département'].values else  f"{int(total_count - nan_count)}" if not (total_count - nan_count) == 0 and not np.isnan(
                        (total_count - nan_count)) else '-'],
                    '%SATCLI': ["-" if name in missing_departments['Département'].values else  f"{satcli_ratio:.2%}" if not np.isnan(satcli_ratio) and not str(
                        satcli_ratio) == 'nan' else '-'],
                    "Nbr d'inter":["-" if name in missing_departments['Département'].values else  f"{int(total_count)}" if not total_count == 0 and not np.isnan(total_count) else '-'],
                    "Tx de réponse": ["-" if name in missing_departments['Département'].values else  f"{ratio:.2%}" if not np.isnan(ratio) and not str(
                        ratio) == 'nan' else '-'],
                    'Evolution': [evo_val]
                }
                
                temp = pd.DataFrame(data)

                    
                one_day = pd.concat([one_day, temp], ignore_index=True)
                one_day = one_day.dropna(subset=['Conducteur'])

                # Update old_evo for the next iteration
                

            except Exception as e:
                traceback.print_exc()
                pass
        
        #one_day=add_missing_ce(one_day)
        temp = get_global(total_grp,old_g_evo)
        satcli_ratio_g=temp.iloc[0]['%SATCLI'].replace('%','')
        if satcli_ratio_g =='-':
            satcli_ratio_g=0
        old_g_evo=float(satcli_ratio_g)


        one_day = pd.concat([one_day, temp], ignore_index=True)
        
        if is_first:
            one_day = one_day.drop('Evolution', axis=1)
            is_first=False

        #one_day.to_excel(f'{key_s}.xlsx',index=False)
        if not res.empty:
            one_day.drop(columns=['Conducteur', "Chef d'équipe", 'Département'], axis=1, inplace=True)
        else:
            first_three = one_day[one_day.columns[:3]]
            first_three.columns = [[col_name] * (len(first_three.columns)), first_three.columns]
            one_day.drop(columns=['Conducteur', "Chef d'équipe", 'Département'], axis=1, inplace=True)
            res = pd.concat([res, first_three], axis=1, sort=False)

        one_day.columns = [[key_s] * (len(one_day.columns)), one_day.columns]
        res = pd.concat([res, one_day], axis=1, sort=False)
    

    return res



def df_cleaning(res):
    res = res.dropna(subset=[res.columns[0]])
    res = res.fillna('-')
    res = res.sort_values(by=[res.columns[0],res.columns[1]])
    res = pd.concat([res[res[res.columns[0]] != 'Total'], res[res[res.columns[0]] == 'Total']])
    cols= [col for col in res.columns if  '%SATCLI' in col]
     # Add border styling
    res=res.style.applymap(high_red,subset=cols,value_max = 95,value2 = 91,value3 = 87)
    cols = [col for col in res.columns if 'Evolution' in col]
    res = res.applymap(high_red_evo, subset=cols)
    return res



def add_missing_ce(groups,date):
    staff_kyntus['Département'] = staff_kyntus['Département'].astype(float)
    missing_departments=pd.DataFrame()
        
    missing_departments = staff_kyntus[~staff_kyntus['Département'].isin(groups['Département'])]

    # If missing departments exist, add them to the current group with all values set to 0
    
    if not missing_departments.empty:
        missing_data = pd.DataFrame({'Date': [date] * len(missing_departments),
                                    'Département': missing_departments['Département'],
                                    'Review': [0] * len(missing_departments)})
        groups = pd.concat([groups, missing_data], ignore_index=True)
    return groups,missing_departments



def sort_months(grouped):
    group_dfs = {}
    last_dates = pd.DataFrame()
    for name, group in grouped:
        last_date = group['Date'].iloc[-1]  # Get the last date of the group
        last_dates = pd.concat([last_dates, pd.DataFrame({'group': [name], 'last_date': [last_date]})], ignore_index=True)
        group_dfs[name] = group
    sorted_groups = last_dates.sort_values(by='last_date')
    sorted_list = sorted_groups['group'].tolist()
    groups_sorted = {group_name: group_dfs[group_name] for group_name in sorted_list}
    return groups_sorted.items()
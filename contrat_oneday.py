from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
# create ChromeOptions object and set headless mode
from selenium.webdriver.chrome.service import Service
from pathlib import Path,os

import time,pandas as pd
import os
script_dir = os.path.dirname(os.path.abspath(__file__)) 
print(script_dir)

from db import db
import random
from env import config

#input()
# create a ChromeOptions object
def tecnow_up():
    import os,shutil
    HOME_DIR=config('HOME_DIR',default=None)
    home_dir = Path.home() / HOME_DIR
    script_dir = home_dir
    print(script_dir)
    def empty_folder(folder):
        if os.path.isdir(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            os.mkdir(folder)
    folder_path = home_dir /"data"
    empty_folder(folder_path)
    empty_folder(home_dir /"results")
    # create a ChromeOptions object
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_settings.popups": 0,
                    "download.default_directory": str(script_dir / "data/"), # IMPORTANT - ENDING SLASH V IMPORTANT
                    "directory_upgrade": True}
    # set the default download directory to the script directory
    language = "en-US"
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--lang=" + language)
    chrome_options.add_experimental_option("prefs",prefs )
    def enable_download_in_headless_chrome(driver, download_dir):
        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)
    # create a ChromeDriver instance with the specified options


    import os
    from selenium.webdriver.chrome.service import Service

    PATH=home_dir /'chromedriver.exe'
    service = Service(executable_path=PATH)
    driver = webdriver.Chrome(options=chrome_options,service=service)
    enable_download_in_headless_chrome(driver,str(home_dir / "data"))
    #enable_download_in_headless_chrome(driver,script_dir + r"\data\\")
    driver.get('https://tecnow.service-now.com/navpage.do')

    driver.switch_to.frame("gsft_main")
    time.sleep(random.uniform(1, 3))
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"user_name")
    )) 
    TECNOW_EMAIL=config('TECNOW_EMAIL',default=None)
    TECNOW_PASSWORD=config('TECNOW_PASSWORD',default=None)
    email_field.send_keys(TECNOW_EMAIL)
    time.sleep(random.uniform(1, 3))
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"user_password")
    ))  
    password_field.send_keys(TECNOW_PASSWORD)
    time.sleep(random.uniform(1, 3))
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(( By.ID, 'sysverb_login')))
    time.sleep(random.uniform(1, 3))
    login_button.click()
    script = '''
        return document.readyState === 'complete' && !window.jQuery.active;
    '''

    #input()
    WebDriverWait(driver, 10).until(
            lambda x: driver.execute_script(script)
        ) 
    time.sleep(5)
    base_url = 'https://tecnow.service-now.com/nav_to.do?uri=%2Fx_bote_parcourstec_intervention_list.do%3Fsysparm_query%3Du_idrdvSTARTSWITHEPS%5Eu_typordvINracco,sav%5Eactive%3Dfalse%5Eu_datedebutON{date}@javascript:gs.dateGenerate(%27{date}%27,%27start%27)@javascript:gs.dateGenerate(%27{date}%27,%27end%27)%5Eu_prestationNOT%20LIKEASSIST%5Eu_statutNOT%20INa_planifier%26sysparm_first_row%3D1%26sysparm_view%3D'
    import datetime
    # Define the start date as today
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    formatted_date = yesterday.strftime('%Y-%m-%d')
    empty_folder('data')
    url = base_url.format(date=formatted_date)

    driver.get(url)
    driver.switch_to.frame("gsft_main")
    Burger2  = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/span/div/div[5]/table/tbody/tr/td/div/table/thead/tr[1]/th[3]/span/i')))
    Burger2.click()
    #/html/body/div[1]/div[1]/span/div/div[7]/div[1]/table/thead/tr[1]/th[3]/span/i

    Export  = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(( By.XPATH, '//div[@data-context-menu-label="Export"]')))
    Export.click()

    Excelin  = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(( By.XPATH, '/html/body/div[5]/div[2]')))
    Excelin.click()


    Dowwnload  = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(( By.ID, 'download_button')))
    attribute_to_check = "disabled"  # Attribute to check for disabled state
    wait = WebDriverWait(driver, 10)
    # Continuously check if the button is disabled
    while True:
        # Wait for the button to be present
        
        # Check if the button is disabled
        if Dowwnload.get_attribute(attribute_to_check) == "true":
            print("Button is disabled, sleeping for 5 seconds...")
            time.sleep(5)  # Sleep for 5 seconds
        else:
            # Button is clickable, click it
            Dowwnload.click()
            break 
    file_name='x_bote_parcourstec_intervention.xlsx'


    while True:
        file_list = os.listdir(folder_path)

        df=None
        
        # Loop through each file in the folder
        for file_name in file_list:
            # Check if the file is a CSV file
            if file_name.endswith(".xlsx"):
                #driver.quit()
                print(os.path.join(folder_path, file_name))
                # Read the CSV file into a pandas DataFrame
                df = pd.read_excel(f"{folder_path}\\{file_name}",sheet_name='Page 1')
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                df.columns = [col.replace('\t', '') for col in df.columns]
                if 'Statut du RDV ' in df.columns:
                    df.rename(columns={'Statut du RDV ': 'Statut du RDV'}, inplace=True)
                print(df)
                # Exit the loop after the first CSV file is read
                break
        print(df)
        if df is not None:
            break
        time.sleep(5)
    #df=df[['FYT',"N° Ticket","Id RDV","Type d'intervention","Technicien","Typologie RDV","Prestation","Statut du RDV","Code clôture","Début INTER","Ville","Département","Début du RDV","Commentaire 1","Commentaire 2","Commentaire 3","GEM","Dernier CheckMonitoring","Closed","Closed by","Diagnostique Wifi","Nombre de voisins KO","Nombre de voisins dégradés","Opérateur d'immeuble","Opérateur horizontal","Générateur du code de décharge CA","Référence PM technique","N° Voie","Type de Voie","Nom Voie","Code INSEE","Ville.1","GEM cause","GEM commentaire","GEM date"]]
    res=db.insert_data(df)
    print(res)


    # Close the WebDriver when done
    driver.quit()

#tecnow_up()
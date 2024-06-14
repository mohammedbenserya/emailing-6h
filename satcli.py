from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
# create ChromeOptions object and set headless mode
from pathlib import Path,os
home_dir = Path.home()
import time,pandas as pd
import os

from sqlalchemy import inspect
from selenium.webdriver.chrome.service import Service
from db import create_engine_
from env import config
def satcli_uto():
    table_name='satcli'
    db_name = 'ind'
    engine = create_engine_(db_name)
    inspector = inspect(engine)

        # Check if the table exists
    id_list=pd.DataFrame()
    if  inspector.has_table(table_name):
            id_list = pd.read_sql('SELECT ID FROM satcli', con=engine)  # read data from MySQL table


    #hada howa

    HOME_DIR=config('HOME_DIR',default=None)
    home_dir = Path.home() / HOME_DIR

    print(home_dir)
    import os,shutil
    script_dir = home_dir
    print(script_dir)
    table_name='satcli'
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
    driver.get('https://bytel.smartfix30.com/#/login')

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"inputEmail3")
    )) 
    SMARTFIX_EMAIL=config('SMARTFIX_EMAIL',default=None)
    SMARTFIX_PASSWORD=config('SMARTFIX_PASSWORD',default=None)
    email_field.send_keys(SMARTFIX_EMAIL)

    # fill in the password field
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"inputPassword3")
    ))  
    password_field.send_keys(SMARTFIX_PASSWORD)

    # click on the login button
    login_button = driver.find_element(By.CSS_SELECTOR, '.e2e-login-button')
    login_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,"//a[@href='/#/app/dashboardNew']")
    ))  
    time.sleep(5)
    driver.get('https://bytel.smartfix30.com/#/app/ratings')
    time.sleep(5)

    #input()

    #datepicker
    datepicker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"datepicker")
    )) 
    actions = ActionChains(driver)
    actions.move_to_element(datepicker)
    driver.execute_script("arguments[0].click();", datepicker)

    range_ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/ul/li[2]")
    )) 
    actions = ActionChains(driver)
    actions.move_to_element(range_)
    driver.execute_script("arguments[0].click();", range_)
    applyBtn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/div/button[1]")
    )) 
    actions = ActionChains(driver)
    actions.move_to_element(applyBtn)
    driver.execute_script("arguments[0].click();", applyBtn)
    download = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//button[@ng-if="$root.requiresClaim(\'EXCEL_EXPORT_SERVER_SIDE\')"]')
    ))
    time.sleep(5)
    actions = ActionChains(driver)
    actions.move_to_element(download)
    driver.execute_script("arguments[0].click();", download)
    time.sleep(5)

    # Get the list of files in the folder
    while True:
        file_list = os.listdir(folder_path)

        df=None
        
        # Loop through each file in the folder
        for file_name in file_list:
            # Check if the file is a CSV file
            if file_name.endswith(".xlsx"):
                driver.quit()
                print(os.path.join(folder_path, file_name))
                # Read the CSV file into a pandas DataFrame
                df = pd.read_excel(f"{folder_path}\\{file_name}",sheet_name='Ratings')
                print(df)
                # Exit the loop after the first CSV file is read
                break
        print(df)
        if df is not None:
            break
        time.sleep(5)


    #ranges
    #data-range-key="Les 30 derniers jours"

    #applyBtn btn btn-sm btn-green
    #df.to_sql('ratings', engine, if_exists='replace', index=False)
    if not id_list.empty:
        df=df[~df['ID'].isin(id_list['ID'])]
    print(len(df))
    def Repondu(x):
        if (x['Review'] == 4):
            return 1
        if (x['Review'] == 5):
            return 1
        else:
            return 0
    df['satisfication'] = df.apply(lambda x: Repondu(x),axis=1)
    if  not df.empty:
        inspector = inspect(engine)

        # Check if the table exists
        if not inspector.has_table(table_name):
            # Create the table if it doesn't exist
            df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=10000)
            print("New table created.")
        else:
            # Append the data to the existing table
            df.to_sql(table_name, engine, if_exists='append', index=False, chunksize=10000)
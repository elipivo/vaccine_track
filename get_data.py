from datetime import datetime
from datetime import timedelta
from datetime import date

import pandas as pd

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data():

    browser = Chrome()
    wait = WebDriverWait(browser, 20)

    URL = 'https://covid.cdc.gov/covid-data-tracker/?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fcases-updates%2Fcases-in-us.html'
    browser.get(URL)

    vaccine_button = wait.until(EC.element_to_be_clickable((By.ID, 'prntVaccinations')))
    vaccine_button.click()

    wait.until(EC.presence_of_element_located((By.ID, 'vaccinations-banner-wrapper')))

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'card-category')))
    vaccine_data_kind = browser.find_elements(By.CLASS_NAME,"card-category")
    vaccine_data_kind = [element.text for element in vaccine_data_kind]

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'card-number')))
    vaccine_data = browser.find_elements(By.CLASS_NAME,"card-number")
    vaccine_data = [element.text for element in vaccine_data]
    vaccine_data = [num.replace(',','') for num in vaccine_data]
    vaccine_data = list(map(int,vaccine_data))

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'card-updated')))
    vaccine_data_date = browser.find_elements(By.CLASS_NAME,"card-updated")
    vaccine_data_date = [element.text for element in vaccine_data_date]
    vaccine_data_date = vaccine_data_date[0]

    vaccine_data_date = vaccine_data_date.split(' |',2)[1]
    vaccine_data_date = datetime.strptime(vaccine_data_date, 'Data as of: %b %d %Y 6:00am ET')
    vaccine_data_date = vaccine_data_date.date()

    browser.close()

    data_df = pd.DataFrame({vaccine_data_kind[i]: [vaccine_data[i]] for i in range(len(vaccine_data))})

    data_df.insert(0,"Date",[vaccine_data_date])

    return data_df
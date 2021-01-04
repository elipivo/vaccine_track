
from datetime import datetime
from datetime import timedelta
from datetime import date
from time import sleep

import pandas as pd

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_data():

    browser = Chrome()
    browser.implicitly_wait(20)

    URL = 'https://covid.cdc.gov/covid-data-tracker/?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fcases-updates%2Fcases-in-us.html'
    browser.get(URL)

    vaccine_button = browser.find_element(By.ID, "prntVaccinations")
    vaccine_button.click()

    vaccine_data_section = browser.find_element(By.ID,"vaccinations-banner-wrapper")

    vaccine_data_kind = vaccine_data_section.find_elements(By.CLASS_NAME,"card-category")
    vaccine_data_kind = [element.text for element in vaccine_data_kind]

    vaccine_data = vaccine_data_section.find_elements(By.CLASS_NAME,"card-number")
    vaccine_data = [element.text for element in vaccine_data]
    vaccine_data = [num.replace(',','') for num in vaccine_data]
    vaccine_data = list(map(int,vaccine_data))

    vaccine_data_date = vaccine_data_section.find_elements(By.CLASS_NAME,"card-updated")
    vaccine_data_date = [element.text for element in vaccine_data_date]
    vaccine_data_date = vaccine_data_date[0]
    vaccine_data_date = datetime.strptime(vaccine_data_date, 'CDC | Updated: %b %d %Y As of 9:00am ET')
    vaccine_data_date = vaccine_data_date.date()

    browser.close()

    data_df = pd.DataFrame({vaccine_data_kind[i]: [vaccine_data[i]] for i in range(len(vaccine_data))})

    data_df.insert(0,"Date",[vaccine_data_date])

    return data_df

# Record today's data when program begins, then record at 9:30 AM every subsequent day
d = datetime.now()

while(True):

    # try to get data, if it fails report the error and continue
    try:

        data_df = get_data()

        excel_data_df = pd.read_excel('vaccine_data.xlsx',sheet_name='Data',parse_dates=True)

        if not(data_df["Date"][0] in [d.date() for d in excel_data_df['Date']]):
            excel_data_df = excel_data_df.append(data_df,ignore_index=True)
            writer = pd.ExcelWriter('vaccine_data.xlsx',datetime_format='mm/dd/yyyy',date_format='mm/dd/yyyy')
            excel_data_df.to_excel(writer,sheet_name='Data',index=False)
            writer.save()
            print(f"{d}: SUCCESS [new data]")
        else:
            print(f"{d}: SUCCESS [no new data]")

    except:
        print(f"{d}: ERROR")

    # calculate sleep time
    d = datetime.now()
    d_next = d + timedelta(days=1)
    d_next = d_next.replace(hour = 18, minute = 0, second=0)
    sleep_secs = (d_next-d).total_seconds()

    # wait until update time
    sleep(sleep_secs)
    d = d_next
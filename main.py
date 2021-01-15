
from datetime import datetime
from datetime import timedelta
from datetime import date
from time import sleep

import pandas as pd

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from get_data import get_data

# Record today's data when program begins, then record at 6:00 PM every day
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
    d_next = d.replace(hour = 18, minute = 0, second=0)
    sleep_secs = (d_next-d).total_seconds()
    if (sleep_secs < 0):
        d_next = d_next+timedelta(days=1)
        sleep_secs = (d_next-d).total_seconds()

    # wait until update time
    sleep(sleep_secs)
    d = d_next
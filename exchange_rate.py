import requests
import urllib3
import json
import pandas as pd
import numpy as np

urllib3.disable_warnings()

# header configuration
headers = {
    'accept': 'application/json',
    'Authorization': }

def get_response():
    response = requests.get('https://api.oip.tmrnd.com.my/app/t/opendata.oip.tm.com.my/bnm/1.0.0/exchange-rate', headers=headers, verify=False)
    data = response.json()
    # takes only usable data and not meta data
    usable_data = data['data']
    return usable_data
    

def country_code_pulls(data):
    # date is similar, only one value is needed
    date_of_exchange = data[0]['rate']['date']
    codes = ['date']
    rates = []
    for i in range(len(data)):
        # simplified structure
        dt = data[i]

        code = dt["currency_code"]
        codes.append(code)

        rate = dt["rate"]["middle_rate"]
        unit = dt["unit"]
        # get RM per unit of measurement
        rates.append(rate/unit)
    rates.insert(0, date_of_exchange)
    return (codes, rates)

def data_formatting(data):
    output = country_code_pulls(data)
    columns = output[0]
    rows = np.array([output[1]])

    # output as DataFrame
    df = pd.DataFrame(rows, columns = columns)
    df.set_index('date')

    return df

print(data_formatting(get_response()))

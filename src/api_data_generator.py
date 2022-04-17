import requests
import json
import numpy as np
from datetime import  datetime

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"

querystring = {"symbol":"GLD","region":"US"}

headers = {
    'x-rapidapi-key': "7dc35e8588mshee200a9fe44d126p15ff82jsn66898b126811",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response.text)
for index in np.arange(len(json_data["prices"])):
    for key in json_data["prices"][index].keys():
        if key == "date":
            timestamp = json_data["prices"][index]["date"]
            json_data["prices"][index]["date"] = datetime.fromtimestamp(timestamp)

import csv
csv_columns = ['date','open','high', 'low', 'close', 'volume', 'adjclose']

csv_file = "gldstock.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for d in json_data["prices"]:
            for key in d.keys():
                if key == "adjclose":
                    writer.writerow(d)
except IOError:
    print("I/O error")
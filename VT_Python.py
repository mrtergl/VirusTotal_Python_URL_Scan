from browser_history import get_history
from pathlib import Path
import requests
import time
import base64
import json
import os
import pandas as pd

home = str(Path.home())

outputs = get_history()
his = outputs.histories
outputs.save(home+"\history.csv")


current_directory = os.getcwd()

liste =[]
col_list = ["URL", "Timestamp"]
df = pd.read_csv(home+'\history.csv', usecols=col_list)
for i in range(len(df.index)):
    
    liste.append(df["URL"].iloc[i])
    

      
    
headers = {

    "Accept": "application/json",

    "x-apikey": "0f901f14014fb58f6ea58e0ea143366e519c015182329999c89eda8066eb855c"

}


i=0

for site in liste:
    url = "https://www.virustotal.com/api/v3/urls/"
    url_id = base64.urlsafe_b64encode(site.encode()).decode().strip("=")
    url = url+url_id
    response = requests.get(url, headers=headers)
    c = response.text
    x = json.loads(response.content)
    if "data" in x:
        data = x["data"]["attributes"]["last_analysis_stats"]["malicious"]
        if data <= 0:
            with open(home+'/vt_results.txt','a') as vt:
                vt.write(site) and vt.write (' -\tNOT MALICIOUS\n')
                print(liste[i], "DONE")
        elif 1 <= data >= 3:
            with open(home+'/vt_results.txt','a') as vt:
                vt.write(site) and vt.write (' -\tMAYBE MALICIOUS\n')
                print(liste[i], "DONE")
        elif data >= 4:
            with open(home+'/vt_results.txt','a') as vt:
                vt.write(site) and vt.write (' -\tMALICIOUS\n')
                print(liste[i], "DONE")
        else:
            print("url not found")
    else:
        print("url not found")
        
    i = i+1    
    time.sleep(15)

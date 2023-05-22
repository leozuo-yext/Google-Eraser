import pandas as pd
import streamlit as st
import requests
import csv
import sys
import time
import json


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

"""
### Please Pick a Google Endpoint
"""
google_endpoint = st.selectbox('Google Endpoint', options = ['Business Info','Place Actions','Attributes','Media'])
if google_endpoint == 'Business Info':
    """
    ### Please enter the updateMasks, seperated by commas
    """
    params_str = '?updateMask=' + st.text_input('Google Update Masks')

else:
    params_str = ""


"""
### Please Pick An Operation
"""
google_operation = st.selectbox('Google Operation', options = ['GET','POST','PATCH','DELETE'])


"""
### Please Enter the Google Access Token
"""
token = st.text_input('Google Access Token')
headers = {"Authorization" : "Bearer " + token}

"""
### Please Upload the Google Entities
"""
google_file = st.file_uploader('Google Prep File Upload', type = 'csv')



def prepGoogleEraser(file):
    prep = []
    inputCSV = pd.read_csv(file, encoding = 'utf-8')
    inputCSV['Yext ID'] = inputCSV['Yext ID'].astype(str)
    for row, r in inputCSV.iterrows():
        info = {}
        info["location"] = r["Yext ID"]
        info["url"] = "https://mybusinessplaceactions.googleapis.com/v1/locations/%s/placeActionLinks" % r["GBP Location ID"][1:] 
        try:
            info["payload"] = r["payload"]
        except:
            pass
        prep.append(info)
    return prep

def deleteOperation(prep):
    for row in prep:
        r = requests.get(row["url"],headers=headers)
        print("GET Status: " + str(r.status_code))
        data = json.loads(r.content)
        #print(data['placeActionLinks'][0]["createTime"])
        if len(data) == 0:
            #add_req = requests.post(row["url"],headers = headers, data = row["payload"])
            #print("Add Status: " + str(add_req.status_code))
            pass
        elif len(data['placeActionLinks']) > 0:
            for link in data['placeActionLinks']:
                placeActionLinks_name = link['name']
                #print(placeActionLinks_name)
                delete_req = requests.delete("https://mybusinessplaceactions.googleapis.com/v1/" + placeActionLinks_name, headers=headers)
                #print("https://mybusinessplaceactions.googleapis.com/v1/" + placeActionLinks_name)
                print("Delete Status: " + str(delete_req.status_code))


if google_file is not None:
    results = prepGoogleEraser(google_file)
    st.write(results[0])



















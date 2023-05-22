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
        info["url"] = "https://mybusinessbusinessinformation.googleapis.com/v1/locations/%s?%s" % (r["GBP Location ID"][1:],params_str)
        prep.append(info)
    return prep

def deleteOperation(prep):
    payload = "{}"
    for row in prep:
        r = requests.patch(row["url"],headers=headers, data = payload)
        print("Delete Status: " + str(r.status_code))

if google_file is not None:
    results = prepGoogleEraser(google_file)
    st.write("Example Call")
    st.write("Removing Contents for " + results[0]['url'])
    st.write('Should I run the script?')
    st.write('You are hereby claiming full responsbility of the outcome of the script, please select I agree to continue')
    agreement_checkbox = st.checkbox('I agree')
    if agreement_checkbox:
        run_script = st.button('Run the script')
        if run_script:
            deleteOperation(results)



















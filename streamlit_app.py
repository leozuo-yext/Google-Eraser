import pandas as pd
import streamlit as st
import requests
import csv
import sys
import time
import json
from concurrent.futures import ThreadPoolExecutor

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


"""
### Please enter the updateMasks, seperated by commas
"""
params_str = '?readMask=' + str(st.text_input('Google Update Masks'))


"""
### Please Enter the Google Access Token
"""
token = str(st.text_input('Google Access Token'))
headers = {"Authorization": "Bearer " + token}

"""
### Please Upload the Google Entities
"""
google_file = st.file_uploader('Google Prep File Upload', type='csv')


def prepGoogleEraser(file):
    prep = []
    inputCSV = pd.read_csv(file, encoding='utf-8')
    inputCSV['Yext ID'] = inputCSV['Yext ID'].astype(str)
    for row, r in inputCSV.iterrows():
        info = {}
        info["Yext ID"] = r["Yext ID"]
        info["url"] = "https://mybusinessbusinessinformation.googleapis.com/v1/locations/%s%s" % (str(r["GBP Location ID"])[1:], params_str)
        prep.append(info)
    return prep


def http_request(prep_chunks):
    r =  requests.get(prep_chunks['url'], headers = headers)
    return prep_chunks['Yext ID'],r

def deleteOperation(prep,chunksize):
    my_bar = st.progress(0, text= "Operation in progress. Please wait...")
    payload = "{}"
    chunks = [prep[x:x+int(chunksize)] for x in range(0, len(prep), chunksize)]
    num_chunks = len(chunks)
    total_responses = []
    perc_done = 0
    for count, prep_chunks in enumerate(chunks):
        with ThreadPoolExecutor() as pool:
            response_list = list(pool.map(http_request,prep_chunks))
        for response_row in response_list:
            r = response_row[1]
            Yext_ID = response_row[0]
            if r.status_code == 400:
                st.write("Bad Request")
                st.write("Last Yext Location: " + str(Yext_ID))
                st.write("Reason: " + r.text)
                sys.exit("Bad Request")
                st.stop()
            if r.status_code == 401:
                st.write("Expired Token")
                st.write("Last Yext Location: " + str(Yext_ID))
                sys.exit("unauthenticated")
                st.stop()
            total_responses.append([Yext_ID, r.status_code, r.text])
        perc_done = round(count/num_chunks * 100)
        my_bar.progress(perc_done, text="Operation in progress. Please wait...")
        st.write("{:.2%}".format(count/num_chunks) + " completed")
        st.write(total_responses)
        time.sleep(1)

if google_file is not None and token != "":
    prepFile = prepGoogleEraser(google_file)
    st.write("Example Call")
    st.write("Removing Contents for " + prepFile[0]['url'])
    st.write('Does this example call look right?')
    st.write('You are hereby claiming full responsbility of the outcome of the script, please select I agree to continue')
    agreement_checkbox = st.checkbox('I agree')
    if agreement_checkbox:
        run_script = st.button('Run the script')
        if run_script:
            st.write("SCRIPT IS STARTING")
            deleteOperation(prepFile,100)
elif token == "":
    st.write("Please input a Token!")








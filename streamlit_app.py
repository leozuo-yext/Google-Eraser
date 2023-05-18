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



google_file = st.file_uploader('Upload a CSV', type = 'csv')
google_operation = st.selectbox('Pick one', ['GET','POST','PATCH','DELETE'])

headers = {"Authorization" : "Bearer " + 'token'}




def prepGoogleEraser(file):
    prep = []
    inputCSV = pd.read_csv(file, encoding = 'utf-8')
    inputCSV['Yext ID'] = inputCSV['Yext ID'].astype(str)

    st.write(inputCSV)
    for row, r in inputCSV.iterrows():
        st.write(r)
        info = {}
        info["location"] = r["Yext ID"]
        #info["appointment_url"] = r["appointment_url"]
        info["url"] = "https://mybusinessplaceactions.googleapis.com/v1/locations/%s/placeActionLinks" % r["GBP Location ID"][1:] 
        #info["payload"] = payload.replace("PAYLOAD_URL",r["appointment_url"])
        prep.append(info)
        st.write(prep)
        return prep


if google_file is not None:
    results = prepGoogleEraser(google_file)
    st.write(results)




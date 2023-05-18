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

if google_file is not None:
    inputCSV = google_file.read().decode("utf-8-sig").encode("utf-8")
    st.write(inputCSV)
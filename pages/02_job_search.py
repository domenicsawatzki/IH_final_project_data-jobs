import streamlit as st  
from st_pages import Page, show_pages, add_page_title  


import json  
import pickle  
import pandas as pd  
import numpy as np  
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode  
from src.myModules import transformer as myBib  
import altair as alt  
import seaborn as sns  

from datetime import date  

import matplotlib.pyplot as plt  

import os  


import streamlit as st  

st.set_page_config(
    page_title='Data Job App',
    layout='wide'
    
)

add_page_title()






with open("config/config.json", 'r') as f:
    config = json.load(f)
    
NLP_data_path = config['NLP_data_path']
input_name = "skills_df"

with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
    data = pickle.load(f)

data = myBib.skill_df(data)




    
yes_jobs = []
no_jobs = []

st.sidebar.header("Search Filter")

search_term = st.sidebar.text_input("Enter a city:")

date_filter = st.sidebar.radio(
    "Select Date Range",
    options=["Last Week", "Last 2 Weeks", "Last 3 Weeks",
        "Last Month", "Last 2 Months"]
)


if date_filter == "Last Week":
    time_filter = date.today() - pd.Timedelta(days=7)
elif date_filter == "Last 2 Weeks":
    time_filter = date.today() - pd.Timedelta(days=14)
elif date_filter == "Last 3 Weeks":
    time_filter = date.today() - pd.Timedelta(days=21)   
elif date_filter == "Last Month":
    time_filter = date.today() - pd.Timedelta(days=30)

elif date_filter == "Last 2 Months":
    time_filter = date.today() - pd.Timedelta(days=60)

filtered_df = pd.DataFrame()




if search_term:
    filtered_df = data[data['city'].str.contains(search_term, case=False, na=False)]
    yes_jobs, no_jobs = myBib.top_jobs(filtered_df, yes_jobs, no_jobs)
else:
        yes_jobs, no_jobs = myBib.top_jobs(data, yes_jobs, no_jobs)





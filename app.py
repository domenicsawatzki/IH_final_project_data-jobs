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

import matplotlib.pyplot as plt

import os


import streamlit as st

# setup page config
st.set_page_config(
    page_title='Data Job App',
    layout='wide'
)
add_page_title()

# load config for path management
with open("config/config.json", 'r') as f:
    config = json.load(f)
    
NLP_data_path = config['NLP_data_path']
input_name = "skills_df"

# create sidebar 
st.sidebar.success('Select a page above')

# add page names
show_pages(
    [
        Page("app.py", "Today's top jobs", ''),
        Page("pages/02_skills.py", "Top skills", ""),
        Page("pages/03_Trainer.py", "Model Training", "")
    ]
)

# open and load dataframe
with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
    data = pickle.load(f)




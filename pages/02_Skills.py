import streamlit as st 
from st_pages import Page, show_pages, add_page_title
import json 
import pickle
import altair as alt
import pandas as pd 
import numpy as np
from src.myModules import transformer as myBib

import streamlit as st



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

# open and load dataframe
with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
    data = pickle.load(f)


filter_list = ['data_analyst', 'analytics_engineer','bi_analyst', 'ml_engineer', 'business_analyst', 'bi_analyst', 'data_scientist', 'data_engineer']

# pre filter for dataset
job_filter_dict = { 'All':filter_list, 'Data Analyst':'data_analyst', 'Data Engineer':'data_engineer', 'Data Scientist':'data_scientist', 'Business Analyst':'business_analyst','Bi Analyst':'bi_analyst' ,
                   'Analytics Engineer':'analytics_engineer', 'Machine Learning Engineer':'ml_engineer'}


job_selection = st.selectbox('Select a Job Title:', list(job_filter_dict.keys()))


if job_selection == 'All':
    filtered_df = data
    counter = len(filtered_df)
if job_selection != 'All':
    filtered_df = data[data['new_job_title'].apply(lambda x: job_filter_dict[job_selection] in x)]
    counter = len(filtered_df)

st.write(f"{counter} jobs found in dataset.")
skill_data = myBib.agg_skill_data(filtered_df) #prepare dataframe for top list

df_sorted = skill_data.sort_values('percentage', ascending=False)

# st.write(f"{counter} jobs found")

chart = alt.Chart(df_sorted).mark_bar().encode(
    x='percentage',
    y=alt.X('keywords', sort=None)
).properties(
    width=1000,  # Width in pixels

)

labels = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(
    text='percentage'
)

final_chart = chart + labels 





st.altair_chart(final_chart, use_container_width=True)


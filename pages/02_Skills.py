import streamlit as st 
from st_pages import Page, show_pages, add_page_title
import json 
import pickle
import altair as alt
import pandas as pd 
import numpy as np
from src.myModules import transformer as myBib

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


prep_data = myBib.prepare_dataset(data)
skill_data = myBib.agg_skill_data(prep_data)


# interactive_plot(skill_data)   
st.dataframe(skill_data)

st.bar_chart(data=skill_data, x = 'keywords', y = 'percentage')

df_sorted = skill_data.sort_values('percentage', ascending=False)


chart = alt.Chart(df_sorted).mark_bar().encode(
    x='percentage',
    y=alt.X('keywords', sort=None)
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


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
        Page("app.py", "Top jobs", ''),
        Page("pages/02_skills.py", "Top skills", ""),
        Page("pages/03_Trainer.py", "Model Training", "")
    ]
)

# open and load dataframe
with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
    data = pickle.load(f)




# filtered_df = data[['company','title', 'job_description', 'url']].head(50)


# # Create a text input box for capturing search term
# st.sidebar.header("Search Filter")
# search_term = st.sidebar.text_input("Enter a city:")

# # Filter DataFrame based on search term

# if st.sidebar.button("Apply filters"):
#     if search_term:
#         filtered_df = data[data['city'].str.contains(search_term, case=False)]


#     else:
#         st.write("Please enter a search term.")

# st.dataframe(filtered_df)

# # edited_df = st.experimental_data_editor(df)
# # favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
# # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")


# Create a text input box for capturing search term
# Create a text input box for capturing search term
st.sidebar.header("Search Filter")
search_term = st.sidebar.text_input("Enter a city:")

# Initialize an empty DataFrame for filtered data
filtered_df = pd.DataFrame()

yes_jobs = []
maybe_jobs = []
no_jobs = []

def top_jobs(df):
    for index, row in df.head(50).iterrows():
        col1, col2 = st.columns([4, 1])
        # if col1.button('Yes', key=f"yes_{index}"):
        #     yes_jobs.append(row.to_dict())
        # if col1.button('Maybe', key=f"maybe_{index}"):
        #     maybe_jobs.append(row.to_dict())
        # if col1.button('No', key=f"no_{index}"):
        #     no_jobs.append(row.to_dict())
            
        with col1.expander(f"{row['company']} - {row['title']}"):
            # col1, col2 = st.columns(2)

            # if col1.button('Like', key=f"like_{index}"):
            #     liked_jobs.append(row.to_dict())
            # if col2.button('Dislike', key=f"dislike_{index}"):
            #     disliked_jobs.append(row.to_dict())
            st.header(f"{row['title']}")
            st.write(f"{row['company']} - {row['city']}")
            
            time = date.today() - row['calc_posting_date']
            st.write(time)
            st.write(f"{row['skills']}")
            st.write(f"URL: [Link]({row['url']})")
            st.write(f"Preview: {row['job_description'][:1000]}...")
            
        empty1, col2_1, empty2, col2_2, empty3 = col2.columns([1, 1, 1, 1, 1])

        if col2_1.button('Y', key=f"yes_{index}"):
            yes_jobs.append(row.to_dict())
        if col2_2.button('N', key=f"no_{index}"):
            no_jobs.append(row.to_dict())


# Filter DataFrame based on search term
if st.sidebar.button("Apply filters"):
    if search_term:
        filtered_df = data[data['city'].str.contains(search_term, case=False)]

        if filtered_df.empty:
            st.write("No matches found.")
        else:
            top_jobs(filtered_df)

    else:
        st.write("Please enter a search term.")
else:
    top_jobs(data)


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

# # load config for path management
# with open("config/config.json", 'r') as f:
#     config = json.load(f)
    
# NLP_data_path = config['NLP_data_path']
# input_name = "skills_df"

# # add page names
show_pages(
    [
        Page("app.py", "Searching Profil", ''),
        Page("pages/02_job_search.py", "Job Search", ""),
        Page("pages/03_skills.py", "Top skills", ""),
        Page("pages/04_Trainer.py", "Premium Job Search", ""),
    ]
)

# load config for path management
with open("config/config.json", 'r') as f:
    config = json.load(f)
    
NLP_data_path = config['NLP_data_path']
input_name = "skills_df"

# open and load dataframe
with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
    data = pickle.load(f)


# st.dataframe(data)


# # Sidebar for the Search Profile Page
# st.header("Set Up Your Search Profile")


# # Initialize session state if it's not already initialized
# if 'search_profile' not in st.session_state:
#     st.session_state.search_profile = {
#         'keywords': [],
#         'location': 'Berlin',
#         'experience_level': 'Any',
#         'job_type': 'Any',
#         'top_n': 20
#     }

# skill_data = myBib.agg_skill_data(data, top_n=20)
# skill_options = skill_data["keywords"].tolist()
# # Keywords

# selected_skills = [st.sidebar.checkbox(skill, value=st.session_state.get(skill, False)) for skill in skill_options]

# # st.session_state.search_profile['keywords'] = st.multiselect(
# #     'What skills/keywords are you interested in?',
# #     options=skill_options,  # Replace with actual skills from your data
# #     default=st.session_state.search_profile['keywords']
# # )
# Save button to save profile


# Function to save settings to a JSON file
def save_settings(settings):
    
    settings_dict = {k: v for k, v in settings.items()}
    
    with open("search_profile.json", "w") as f:
        json.dump(settings_dict, f)

# Function to load settings from a JSON file
def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("settings.json not found, creating an empty dictionary.")
        return {}
    except json.JSONDecodeError:
        print("Failed to decode settings, returning an empty dictionary.")
        return {}

# Initialize session state variables if they do not exist
settings = load_settings()


# Update session state with loaded settings
for key, value in settings.items():
    st.session_state[key] = value

job_filter_dict = {'Data Analyst':'data_analyst', 'Data Engineer':'data_engineer', 'Data Scientist':'data_scientist', 'Business Analyst':'business_analyst','Bi Analyst':'bi_analyst' ,
                   'Analytics Engineer':'analytics_engineer', 'Machine Learning Engineer':'ml_engineer'}
filter_list = list(job_filter_dict.keys())


if st.button("Save Profile"):
    save_settings(st.session_state)

if st.button("load Profile"):
    settings = load_settings()
    
    for key, value in settings.items():
        st.session_state[key] = value

# Initialize session state for selected_titles if not already done
if 'selected_titles' not in st.session_state:
    st.session_state.selected_titles = []

st.sidebar.header("Select Job Titles")

# Create checkboxes for each job title and update session state accordingly
for title in filter_list:
    checked = st.sidebar.checkbox(title, key=title)
    
    if checked:
        if title not in st.session_state.selected_titles:
            st.session_state.selected_titles.append(title)
    else:
        if title in st.session_state.selected_titles:
            st.session_state.selected_titles.remove(title)

if not st.session_state.selected_titles:
    st.write("Please select a job title.")
else:
    # Create a list of keys to search for in the DataFrame based on session state
    search_list = [job_filter_dict[key] for key in st.session_state.selected_titles]

    # Filter the DataFrame
    filtered_df = data[data['new_job_title'].apply(lambda x: any(key in x for key in search_list))]

    # Your additional code to aggregate skill data and so on
    skill_data = myBib.agg_skill_data(filtered_df, top_n=20)
    skill_options = skill_data["keywords"].tolist()

if st.session_state.selected_titles:
    # 3 columns
    col1, col2, col3 = st.columns(3)

    # Column 1: hard skills
    with col1:
        st.write("Select Hard Skills:")
        selected_skills = [st.checkbox(skill, value=st.session_state.get(skill, False)) for skill in skill_options]
        for skill, selected in zip(skill_options, selected_skills):
            st.session_state[skill] = selected
    # Column 2: soft skills
    with col2:
        st.write("Select Soft Skills:")
        st.write("Coming soon!😊 ")

    # Column 3: language
    with col3:
        st.write("select languages:")
        st.write("Coming soon!😊 ")
        # st.session_state.language = st.selectbox(
        #     "Preferred Language:",
        #     ["English", "German", "French"],
        #     index=["English", "German", "French"].index(st.session_state.get("language", "English"))
        # )


    # Display saved search profile
    st.write("Your Search Profile")
    # st.write(f"Selected Skills: {[skill for skill in skills_list if st.session_state[skill]]}")
    # st.write(f"Preferred Language: {st.session_state.language}")





























# # open and load dataframe
# with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
#     data = pickle.load(f)
    
# yes_jobs = []
# no_jobs = []

# # # Create a text input box for capturing search term
# st.sidebar.header("Search Filter")
# # use_default_city = st.sidebar.checkbox("Berlin", value=True)
# # use_other_city = st.sidebar.checkbox("Other")

# # if use_other_city:
# #     use_default_city = False  # Disable the default city (Berlin)
# search_term = st.sidebar.text_input("Enter a city:")

# date_filter = st.sidebar.radio(
#     "Select Date Range",
#     options=["Last Week", "Last 2 Weeks", "Last 3 Weeks",
#         "Last Month", "Last 2 Months"]
# )

# if date_filter == "Last Week":
#     time_filter = date.today() - pd.Timedelta(days=7)
# elif date_filter == "Last 2 Weeks":
#     time_filter = date.today() - pd.Timedelta(days=14)
# elif date_filter == "Last 3 Weeks":
#     time_filter = date.today() - pd.Timedelta(days=21)   
# elif date_filter == "Last Month":
#     time_filter = date.today() - pd.Timedelta(days=30)

# elif date_filter == "Last 2 Months":
#     time_filter = date.today() - pd.Timedelta(days=60)


# # Initialize an empty DataFrame for filtered data
# filtered_df = pd.DataFrame()




# if st.sidebar.button("Apply filters"):
#     if search_term:
#         filtered_df = data[data['city'].str.contains(search_term, case=False, na=False)]
#         yes_jobs, no_jobs = myBib.top_jobs(filtered_df, yes_jobs, no_jobs)
#     else:
#         st.write(f"No match for {search_terms}.")
# else:
#     yes_jobs, no_jobs = myBib.top_jobs(data, yes_jobs, no_jobs)


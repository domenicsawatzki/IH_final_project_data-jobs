import os
import pandas as pd 
import numpy as np
import pickle
import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from datetime import datetime
from datetime import date

with open("config/config.json", 'r') as f:
    config = json.load(f)
    
NLP_data_path = config['NLP_data_path']
input_name = "skills_df"


# # open and load dataframe
# with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
#     data = pickle.load(f)


# print(data.head(10))

def agg_skill_data(data, top_n=20):
    
    all_skills = []
    for skill_list in data['skills']:
        all_skills.extend(skill_list)
    feature_list = list(set(all_skills))
    
    for skill in feature_list:
        data[skill] = False 
        
    for idx, row in data.iterrows():
        for skill in row['skills']:
            data.at[idx, skill] = True
    
    for index, row in data.iterrows():
        for i, token in enumerate(row['skills']):
            if token.lower() in feature_list:
                row['skills'][i] = token.lower()
        data.at[index, 'skills'] = row['skills']
        
    skill_data = pd.DataFrame(data.skills.sum()).value_counts().rename_axis('keywords').reset_index(name='counts')
    skill_data = skill_data[skill_data.keywords != '']
    skill_data['percentage'] = round(skill_data['counts'] / len(data) * 100, 1)
    
    if top_n is not None:
        skill_data = skill_data.nlargest(top_n, 'counts')
        
    
    return skill_data


def agg_top_job(data):
    
    
    return new_data


def top_jobs(df, yes_jobs, no_jobs):
    
    
    #     # Handle non-datetime values
    # df['calc_posting_date'] = pd.to_datetime(df['calc_posting_date'], errors='coerce')
    
    # # Drop NaT values
    # df.dropna(subset=['calc_posting_date'], inplace=True)

    # # st.write(type(df['calc_posting_date'].iloc[0]))
    # # st.write(type(date_filter))
    
    # # st.write(df['calc_posting_date'].head())
    # # st.write(date_filter)

    # # st.write(df['calc_posting_date'].iloc[0] > date_filter)

    # # date_filter = pd.Timestamp(date_filter)
    
    # # df = df.loc[df['calc_posting_date'] > date_filter]
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
                
    page_size = 50  # Number of rows per page
    total_pages = -(-len(df) // page_size)
    start_idx = st.session_state.current_page * page_size  # Starting index of the page
    end_idx = start_idx + page_size  # Ending index of the page

    page_data = df.iloc[start_idx:end_idx]

    # Create columns for navigation buttons and page info
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4.5])

    # Place buttons in the first and second columns
    with col_nav1:
        if st.button('Previous'):
            st.session_state.current_page -= 1  # Move to the previous page
            st.session_state.current_page = max(0, st.session_state.current_page)  # Don't go below 0

    with col_nav2:
        if st.button('Next'):
            st.session_state.current_page += 1  # Move to the next page
            st.session_state.current_page = min(total_pages-1, st.session_state.current_page)  # Don't exceed max pages

    # Display page info in the third column
    with col_nav3:
        st.write(f"Page {st.session_state.current_page + 1} of {total_pages}  -  Total results: {len(df)}")

    # if st.button('Next'):
    #     st.session_state.current_page += 1  # Move to the next page
    # if st.button('Previous'):
    #     st.session_state.current_page -= 1  # Move to the previous page
    #     st.session_state.current_page = max(0, st.session_state.current_page)  # Don't go below 0
    
    df.reset_index(drop=True, inplace=True)
    for index, row in page_data.iterrows():
        col1, col2 = st.columns([4, 1])            
        with col1.expander(f"{row['company']} - {row['title']}"):

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


    
            
    return yes_jobs, no_jobs


def compare_skills_count(row_skills):
    my_skills = ["python", "sql", 'tableau', "r", "pandas"]
    return len(set(row_skills) & set(my_skills))




def skill_df(df):
    df['skills_match_count'] = df['skills'].apply(compare_skills_count)
    df = df.sort_values(by='skills_match_count', ascending=False)
    return df


# def prepare_dataset(data):
#     data = data.apply(time_to_weeks, axis=1) # add transform posting date to date format
#     data.fillna("", inplace=True)
#     # data['skills'] = data['skills'].progress_apply(lambda x: list(set(x))) # remove duplicates from skills
#     data['skills'] = data['skills'].apply(remove_duplicates_and_lower) # lower
#     return data 


# def time_to_weeks(row):
#     scrap_date = row['scraping_date']
#     posting_date = row['posting_date']    
    

#     if 'minute' in posting_date or 'hour' in posting_date or 'Just now' in posting_date:
#         new_date = posting_date
#     if 'day' in posting_date:
#         days = int(posting_date.split(' ')[0])
#         new_date = scrap_date - timedelta(days=days)
#     if 'week' in posting_date:
#         weeks = int(posting_date.split(' ')[0])
#         new_date = scrap_date - timedelta(weeks=weeks)
#     if 'month' in posting_date:
#         months = int(posting_date.split(' ')[0])
#         new_date = pd.to_datetime(scrap_date) - pd.DateOffset(months=months)
#     if 'year' in posting_date:
#         years = int(posting_date.split(' ')[0])
#         new_date = pd.to_datetime(scrap_date) - pd.DateOffset(years=years)
    
    
#     if isinstance(new_date, datetime):    
#         row['calc_posting_date'] = new_date.date()
#     else:
#         row['calc_posting_date'] = new_date
        
        
#     return row

# def remove_duplicates_and_lower(skill_list):
#     return list(set([skill.lower() for skill in skill_list]))
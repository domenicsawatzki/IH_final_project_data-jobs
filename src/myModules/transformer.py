import os
import pandas as pd 
import numpy as np
import pickle
import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from datetime import datetime


with open("config/config.json", 'r') as f:
    config = json.load(f)
    
NLP_data_path = config['NLP_data_path']
input_name = "skills_df"


# # open and load dataframe
# with open(f"{NLP_data_path}{input_name}.pkl", "rb") as f:
#     data = pickle.load(f)


# print(data.head(10))

def agg_skill_data(data):
    
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
    
    return skill_data










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
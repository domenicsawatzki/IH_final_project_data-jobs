from bs4 import BeautifulSoup, NavigableString
import requests
from time import sleep
from random import randint
import math
from tqdm import tqdm
import pickle
import pandas as pd
from datetime import date
from datetime import datetime
import json
import pymysql                        # for getting data from a SQL database
from sqlalchemy import create_engine, text  # for establishing the connection and authentication

from webscraper.scrap_modules import scraper_ds as mybib
from IPython.display import display
import streamlit as st 




keyword_list = mybib.import_keyword_list()
st.text(f"Following keywords are used to scrap data from linkedIn: {keyword_list}")


sql_data = mybib.connect_sql_database()
scraper_df = mybib.initialize_empty_df()

st.write("Overview SQL Database")
st.write(sql_data.head(5))
st.write(sql_data.tail(5))

st.write("Empty Dataframe")
st.write(scraper_df)

st.write("Overview ID control")
id_control = sql_data['id'].tolist()
id_control

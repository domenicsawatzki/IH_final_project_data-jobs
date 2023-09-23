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


keyword_list = mybib.import_keyword_list()
print(f"Following keywords are used to scrap data from linkedIn: {keyword_list}")


sql_data = mybib.connect_sql_database()
scraper_df = mybib.initialize_empty_df()

print("Overview SQL Database")
display(sql_data.head(5))
display(sql_data.tail(5))

print("Empty Dataframe")
display(scraper_df)

print("Overview ID control")
id_control = sql_data['id'].tolist()
id_control

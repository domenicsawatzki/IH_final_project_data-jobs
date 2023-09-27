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
import pymysql                        
from sqlalchemy import create_engine
import sqlalchemy
import zlib
import numpy as np
import json

import os 

os.chdir('c:/Users/Domen/IronHack/01_projects/IH_final_project_data-jobs')
print(os.getcwd())

print(os.getcwd())
with open("config/config.json", 'r') as f:
    config = json.load(f)
    
temp_data_path = config["temp_data_path"]
webscrap_data_path = config["webscrap_data_path"]    


soup_file =  'soup_dictV2'
keyword_file = 'keyword_dictV2'


def total_loop_rough_keywords(keyword_list, scraper_df, id_control, soup_dict, keyword_dict): 

    # links = {}
    for key in keyword_list:
        first_url = f"https://www.linkedin.com/jobs/search?keywords={key}&location=Berlin%2C%20Berlin%2C%20Germany&locationId=&geoId=104944500&f_TPR=&distance=25&f_E=2%2C3%2C4&position=1&pageNum=0"
        key_name = key.replace('%20', " ")
            
        response = requests.get(first_url) # first request for keyword
        response.status_code # 200 status code means OK!
        soup = BeautifulSoup(response.content, "html.parser")
        
        number_of_results = soup.find('span', class_="results-context-header__job-count").text # check number of searching results
        numb = int(number_of_results.replace(",", "").replace("+", ""))

        backend_call_url_list = []
        backend_call_url_list = create_backend_links(first_url, numb, key_name) # create list with sublinks to select different pages 
        
        
        # with open(f'{key_name}_backend_urls.pkl', 'wb') as file:
        #     pickle.dump(backend_call_url_list, file)
        
        id_list = get_id_dict(backend_call_url_list) # get job id's from all pages
        
        with tqdm(total=len(id_list), desc="Starting") as pbar:
            for id in id_list:
                dynamic_text = f"Progressing id: {id}" # text for tqdm progress bar status
                pbar.set_description(dynamic_text) # change text
                pbar.update(1)
                
                if id not in id_control:
                    try:
                        # print(f"scrap data from {id}")
                        # print(f"keyname: {key_name}")
                        # print(f"df: {scraper_df}")
                        # print(f"id_control: {id_control}")
                        new_row_dict, id_control, response = get_all_job_information(id, id_control) # 

                        wait_time = randint(1,3000)
                        pbar.set_description(f"Sleep {wait_time} seconds")
                        sleep(wait_time/1000)
                        try: 
                            
                            soup_dict[id] = response
                            # If the key 'id' doesn't exist, initialize it with a list containing the new key
                        except Exception as e:
                            # Handle any exceptions and provide informative error messages
                            raise ValueError(f"Error occurred: {e}")  
                        
                        try: 
                            if id in keyword_dict:
                                keyword_dict[id].append(key_name)
                            # If the key 'id' doesn't exist, initialize it with a list containing the new key
                            else:
                                keyword_dict[id] = [key_name]

                        except Exception as e:
                            # Handle any exceptions and provide informative error messages
                            raise ValueError(f"Error occurred: {e}")                         
                        # display(soup_dict)
                        
                        try:
                            new_row_df = pd.DataFrame([new_row_dict])
                            scraper_df = pd.concat([scraper_df, new_row_df], ignore_index=True)
                            # display(dataframe)
                        except Exception as e:
                            # Handle any exceptions and provide informative error messages
                            raise ValueError(f"Error occurred: {e}")  
                        
                        try: 
                            id_control.append(id)
                        except Exception as e:
                            # Handle any exceptions and provide informative error messages
                            raise ValueError(f"Error occurred: {e}")  

                    except Exception as e:
                    
                        
                        with open(f'webscraper/temp_data/back_up_df.pkl', 'wb') as file:
                            json.dump(scraper_df, file=file)
                        with open('webscraper/temp_data/soup_dict_backup.pkl', 'w') as f:
                            json.dump(soup_dict, f)
                        with open('webscraper/temp_data/keyword_dict.pkl', 'w') as f:
                            json.dump(keyword_dict, f)
                        with open('webscraper/temp_data/id_list_backup.pkl', "wb") as file:
                            pickle.dump(id_list, file=file)
                        raise ValueError(f"Error occurred: {e}")
                else:
                    pbar.set_description(f"Will skip {id} because is already in the dataset.")
                
    

    
    # try:
    #     add_scrapped_df_to_sql_database(scraper_df)
    #     display(scraper_df.tail(5))
        
    #     with open("webscraper/temp_data/soup_dict.pkl", "wb") as file:
    #         pickle.dump(soup_dict, file=file)
            
    #     with open("webscraper/temp_data/keyword_dict.pkl", "wb") as file:
    #         pickle.dump(keyword_dict, file)
        
    # except Exception as e:
    #     # Handle any exceptions and provide informative error messages
    #     raise ValueError(f"Error occurred: {e}")            
    
    wait_time = randint(1,3000)
    print("I will sleep for " + str(wait_time/1000) + " seconds.")
    sleep(wait_time/1000)
    return scraper_df, soup_dict, keyword_dict 


def import_keyword_list():
    with open("keyword_list.csv", "r") as file:
        keywords = pd.read_csv(file, delimiter = ";")
    keywords["Keywords"] = keywords["Keywords"].str.replace(" ", "%20") # replace all spaces with %20 for thr URL
    keyword_list = keywords['Keywords'].tolist() # creating a list
    return keyword_list

def connect_sql_database():
    try:
        with open("webscraper/sql_secret.txt", "r") as secret:
            secret = secret.read()
        connection_string = 'mysql+pymysql://root:'+secret+'@localhost/bank'
        engine = create_engine(connection_string)
        data = pd.read_sql_query('SELECT * FROM final_project.linked_in_scrap', engine)
        return data 
    except: 
        print("Error connecting to mysql database.")
        return None
    
def add_scrapped_df_to_sql_database(df):
    try:
        with open("webscraper/sql_secret.txt", "r") as secret:
            secret = secret.read()
        connection_string = 'mysql+pymysql://root:'+secret+'@localhost/bank'
        engine = create_engine(connection_string)
        df.to_sql('linked_in_scrap', engine, if_exists='append', index=False)
    except: 
        print("Error connecting to mysql database.")

def initialize_empty_df():
    columns = ['id','title', 'company', 'city', 'posting_date', 'job_description', 'seniority_level', 'job_function', 'industries', 'scraping_date', 'url', 'keyword']
    scraper_df = pd.DataFrame(columns=columns)
    return scraper_df

def get_job_information(soup):    
    class_soup = soup.find("ul", {"class":"description__job-criteria-list"}).find_all('span')
    list = []
    for x in class_soup:
        list.append(x.text.strip())
    
    return list

def get_job_description(soup):
    counter = 1
    description_list = []
    qualification_list = []
    information_list = []
    
    class_soup = soup.find("div", {"class":"description__text"}).find_all('ul')
    for x in class_soup:
        list_items = x.find_all('li')
        # print(list_items)
        list = []
        for item in list_items:
            list.append(item.text.strip())
            
        # print(counter)
        # print(list)
        if counter == 1:
            description_list = list
        if counter == 2: 
            qualification_list = list       
        if counter == 3: 
            information_list = list 
        counter += 1 
    
    return description_list, qualification_list, information_list

def get_all_job_information(id, id_control):

    response = requests.get(f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}')
    soup = BeautifulSoup(response.content, "html.parser")
    job_dict = {}
    job_dict['id'] = id
    try:
        job_dict['title'] = soup.find('h2', class_='top-card-layout__title').text.strip()
    except:
        job_dict['title'] = None
        print("Error: in 'title'")
        
    try:    
        job_dict['company'] = soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        job_dict['company'] = None
        print("Error: in 'company'")
        
    try:    
        job_dict['city'] = soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text.strip()
    except:
        job_dict['city'] = None
        print("Error: in 'city'")
    try:
        job_dict['posting_date'] = soup.find("span", {"class":"posted-time-ago__text"}).text.strip()
    except:
        job_dict['posting_date'] = None
        print("Error: in 'posting date'")
        
    try:    
        job_dict['job_description'] = soup.find("section",{"class":"show-more-less-html"}).text.strip()

    except:
        job_dict['job_description'] = None
        print("Error: in 'job description'")
        
    # try:
    #     job_dict['seniority_level'] = soup.find("span", {"class":"description__job-criteria-text"}).text.strip()
    # except: 
    #     job_dict['seniority_level'] = None
    #     print("Error: in 'seniority level'")

    try:    
        x = get_job_information(soup)        
        job_dict['seniority_level'] = x[0]
        job_dict['job_function'] = x[1]
        job_dict['industries'] = x[3]
    except:
        print(f"Error: get job information in id {id}")
        job_dict['seniority_level'] = None
        job_dict['job_function'] = None
        job_dict['industries'] = None
    
    try:    
        job_dict['scraping_date'] = date.today()
    except:
        job_dict['scraping_date'] = None 
    
    try:
        name = job_dict['title']
        name = name.replace(" ", "%20")
        company = job_dict['company']
        company = company.replace(" ", "%20")
        job_dict['url'] = f"https://www.linkedin.com/jobs/search?keywords={name}%20{company}&location=Berlin%2C%20Berlin%2C%20Germany&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    except:
        job_dict['url'] = None 
    
                        
    try: 
        id_control.append(id)
    except Exception as e:
        # Handle any exceptions and provide informative error messages
        raise ValueError(f"Error occurred: {e}")
    return job_dict, id_control, response

# create links for backend calls and return a list with URLS
def create_backend_links(link, number_of_results, key_name):
    
    # check the number of results and calc the amounts of pages
    
    # if number_of_results > 50: # for testing 
    #     number_of_loops = 2
    
    number_of_loops = math.ceil(number_of_results/25)
    # counter 
    start = 0
    
    print(f"Start creating backend links for {key_name}. Total of found pages: {number_of_loops}\n")
    
    #extract the main body of the link with information about the search settings (title, area, etc.)
    link_key = link.replace("pageNum=0","")
    link_key = link_key.split('jobs/')[1]

    # use the created link keys and counter to create backend_call URL    
    # backend_call = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/{link_key}start={start}"
    
    # initialize the list 
    backend_call_array = pd.array([])
    
    # loopt through number of pages and store the backend_call URL's 
    for i in range(number_of_loops):
        # print(start)
        
        # use the created link keys and counter to create backend_call URL   
        backend_call = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/{link_key}start={start}"
        backend_call_array = np.append(backend_call_array, backend_call)
        start += 25
        
    return backend_call_array 

def save_df_as_json_with_time_stamp(df):   
    current_date = datetime.now()
    time = current_date.strftime("%Y-%m-%d_%H-%M-%S")
    time
    
    scraper_df_json = scraper_df.to_json('dataframe.json', orient='split', date_format='iso', indent=4)

    with open(f'{webscrap_data_path}{str(time)}.json', 'wb') as file:
        json.dump(scraper_df_json, file=file)
        
# go through each page URL and extract the job id's 
def get_id_list(list):
    
    # dictionary to store id list for every page
    counter = 0
    id_array = pd.array([])
    for item in tqdm(list):
        response = requests.get(item)
        # print(f'Start extracting ids from {item}')
        soup = BeautifulSoup(response.content, "html.parser")
        
        alljobs_on_this_page=soup.find_all("li")
        len(alljobs_on_this_page)
        for x in range(0,len(alljobs_on_this_page)):
            job_div = alljobs_on_this_page[x].find("div", {"class": "base-card"})
            if job_div:
                jobid = job_div.get('data-entity-urn')
                if jobid:
                    jobid = jobid.split(":")[3]
                    # print(jobid)
                    id_array = np.append(id_array, jobid)
                else:
                    print("data-entity-urn attribute not found for this job.")
        # print(f"id_array len: {len(id_array)}")
        
        # wait_time = randint(500,1500)
        # print("I will sleep for " + str(wait_time/1000) + " seconds.\n")
        # sleep(wait_time/1000)
    counter +=1
    return id_array

def test():
    print('test')

def export_data(soup_dict, keyword_dict):
    try:
        # mybib.add_scrapped_df_to_sql_database(new_dataframe, con=engine, if_exists='replace', index=False))
        # display(new_scraper_df.tail(5))
        # new_dataframe = pd.concat([old_df, scrap_df], ignore_index=True)
        # mybib.add_scrapped_df_to_sql_database(Scrap_backup, con=engine, if_exists='replace', index=False))

        
        with open(f"{webscrap_data_path}{soup_file}.pkl", "wb") as file:
            pickle.dump(soup_dict, file=file)

        with open(f"{webscrap_data_path}{keyword_file}.pkl", "wb") as file:
            pickle.dump(keyword_dict, file)
            
        # with open("webscraper/webscrap_data/database.pkl", "wb") as file:
        #     pickle.dump(new_dataframe, file)

    except Exception as e:
        # Handle any exceptions and provide informative error messages
        raise ValueError(f"Error occurred: {e}")    
    return 
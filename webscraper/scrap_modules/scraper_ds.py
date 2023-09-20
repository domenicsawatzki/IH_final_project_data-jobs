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

def get_all_job_information(keyword, dataframe, id, id_control):

    response = requests.get(f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}')
    soup = BeautifulSoup(response.content, "html.parser")
    job_dict = {}
    job_dict['id'] = id
    try:
        job_dict['title'] = soup.find('h2', class_='top-card-layout__title').text.strip()
    except:
        job_dict['title'] = None
        
    try:    
        job_dict['company'] = soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        job_dict['company'] = None

    try:
        job_dict['posting_date'] = soup.find("span", {"class":"posted-time-ago__text"}).text.strip()
    except:
        job_dict['posting_date'] = None
        
    try:    
        job_dict['job_description'] = get_job_description(soup)

    except:
        job_dict['job_description'] = None
        
    try:
        job_dict['seniority_level'] = soup.find("span", {"class":"description__job-criteria-text"}).text.strip()
    except: 
        job_dict['seniority_level'] = None

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
        job_dict['job_url'] = f"https://www.linkedin.com/jobs/search?keywords={name}%20{company}&location=Berlin%2C%20Berlin%2C%20Germany&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    except:
        job_dict['job_url'] = None
    
    job_dict['keyword'] = keyword 
    small_soup = soup.find("div", {"class":"description__text"})
    
    try:
        new_row_df = pd.DataFrame([job_dict])
        dataframe = pd.concat([dataframe, new_row_df], ignore_index=True)
    except: 
        print(f"Error in id: {id}")
    try: 
        id_control.append(id)
    except:
        print(f"id_control error in id: {id}")
    
    return dataframe, id_control, small_soup

# create links for backend calls and return a list with URLS
def create_backend_links(link, number_of_results, key_name):
    
    # check the number of results and calc the amounts of pages
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
    backend_call_list = []
    
    # loopt through number of pages and store the backend_call URL's 
    for i in range(number_of_loops):
        # print(start)
        
        # use the created link keys and counter to create backend_call URL   
        backend_call = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/{link_key}start={start}"
        backend_call_list.append(backend_call)
        start += 25
        
    return backend_call_list 

def save_df_as_json_with_time_stamp(df):   
    current_date = datetime.now()
    time = current_date.strftime("%Y-%m-%d_%H-%M-%S")
    time
    
    scraper_df_json = scraper_df.to_json('dataframe.json', orient='split', date_format='iso', indent=4)

    with open(f'webscrap_data/webscrap{str(time)}.json', 'wb') as file:
        json.dump(scraper_df_json, file=file)
        
# go through each page URL and extract the job id's 
def get_id_dict(list):
    
    # dictionary to store id list for every page
    counter = 0
    id_list = []
    for item in list:
        response = requests.get(item)
        print(f'Start extracting ids from {item}')
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
                    id_list.append(jobid)
                else:
                    print("data-entity-urn attribute not found for this job.")
            else:
                print("base-card div not found for this job.")
        # print(f"ID_list len: {len(id_list)}")
        
        wait_time = randint(500,5000)
        print("I will sleep for " + str(wait_time/1000) + " seconds.\n")
        sleep(wait_time/1000)
    return id_list
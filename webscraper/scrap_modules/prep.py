from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from datetime import date
from datetime import datetime
from tqdm import tqdm
import pickle
import requests


cleaned_data_path = 'webscraper/cleaned_data/'
webscrap_data_path = 'webscraper/'


def get_all_job_information(id, response, scrap_date):

    soup = BeautifulSoup(response.content, "html.parser")
    job_dict = {}
    job_dict['id'] = id
    try:
        job_dict['title'] = soup.find('h2', class_='top-card-layout__title').text.strip()
    except:
        job_dict['title'] = None
        # print("Error: in 'title'")
        
    try:    
        job_dict['company'] = soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        job_dict['company'] = None
        # print("Error: in 'company'")
        
    try:    
        job_dict['city'] = soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text.strip()
    except:
        job_dict['city'] = None
        # print("Error: in 'city'")
    try:
        job_dict['posting_date'] = soup.find("span", {"class":"posted-time-ago__text"}).text.strip()
    except:
        job_dict['posting_date'] = None
        # print("Error: in 'posting date'")
        
    try:    
        job_dict['job_description'] = soup.find("section",{"class":"show-more-less-html"}).text.strip()

    except:
        job_dict['job_description'] = None
        # print("Error: in 'job description'")

    try:    
        x = get_job_information(soup)        
        job_dict['seniority_level'] = x[0]
        job_dict['employment_type'] = x[1]
        job_dict['job_function'] = x[2]
        job_dict['industries'] = x[3]
    except:
        # print(f"Error: get job information in id {id}")
        job_dict['seniority_level'] = None
        job_dict['employment_type'] = None
        job_dict['job_function'] = None
        job_dict['industries'] = None
    
    try:    
        job_dict['scraping_date'] = scrap_date
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
    
                        

    return job_dict

def transform_scrap_data_to_df(dict):
    columns = ['id','title', 'company', 'city', 'posting_date', 'job_description', 'seniority_level', 'employment_type', 'job_function', 'industries', 'scraping_date', 'url']
    df = pd.DataFrame(columns=columns)

    for key in tqdm(dict):
        id = key
        response = dict[key]['response']
        scrap_date = dict[key]["scrap_date"]
        new_dict = get_all_job_information(id, response, scrap_date)
        
        new_row_df = pd.DataFrame([new_dict])
        df = pd.concat([df, new_row_df], ignore_index=True)

    return(df)

def get_job_information(soup):    
    class_soup = soup.find("ul", {"class":"description__job-criteria-list"}).find_all('span')
    list = []
    for x in class_soup:
        list.append(x.text.strip())
    
    return list

def second_request_empty_values(df):
    nan_df = df[df["title"].isna()]
    second_requests = nan_df['id'].tolist()
    
    request_dict = {}
    for id in second_requests:
            response = requests.get(f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}')
            wait_time = randint(1,500)
            sleep(wait_time/1000)

            temp_dict = {}
            temp_dict["scrap_date"] = date.today()
            temp_dict["response"] = response
            request_dict[id] = temp_dict
    
    new_nan_df = transform_scrap_data_to_df(request_dict)
    
    temp_df = df[df["title"].notna()]
    final_df = pd.concat([temp_df, new_nan_df], ignore_index=True)
    
    save_cleaned_df(final_df)
    
    return final_df

def save_cleaned_df(df):
    with open(f"{cleaned_data_path}cleaned_dataframe.pkl", "wb") as file:
        pickle.dump(df, file)
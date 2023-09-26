from tqdm import tqdm
import pandas as pd 
from langdetect import detect
import nltk
from nltk.stem import WordNetLemmatizer 

from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
import re
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords

# nltk.download('omw-1.4')
# nltk.download('wordnet') # wordnet is the most well known lemmatizer for english
# nltk.download('punkt')
# nltk.download('stopwords')

import collections
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS



def check_language(x):
    try:
        return detect(x)
    except:
        return 'unknown'

def add_language_values_to_df(df, search_column, new_column = 'language'):
    df[search_column].fillna("", inplace=True)

    tqdm.pandas(desc="Processing")
    df[new_column] = df[search_column].progress_apply(check_language)
    return df

def title_pre_processing(x):
    return x


def clean_up(s):
    pattern_to_remove = r'\([a-z]/[a-z]/[a-z]\)'
    s = re.sub(pattern_to_remove, '', s)
    s = re.sub('all genders', '', s)
    s = re.sub('/', ' ', s)
    s = re.sub('& ', ' ', s)
    s = re.sub('– ', ' ', s)
    s = re.sub('- ', ' ', s)
    s = re.sub(': ', ' ', s)
    s = re.sub(', ', ' ', s)
    # s = re.sub('*', ' ', s)



    return s.lower().strip()

def tokenize(s):
    tokens = word_tokenize(s)
    return tokens



def get_wordnet_pos(word):
    tag_dict = {"J": wordnet.ADJ, 
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV}
    tag = nltk.pos_tag([word], lang='eng')[0][1][0].upper()
    return tag_dict.get(tag, wordnet.NOUN)

def stem_and_lemmatize(l):
    """
    Perform stemming and lemmatization on a list of words.

    Args:
        l: A list of strings.

    Returns:
        A list of strings after being stemmed and lemmatized.
    """
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in l]
    return lemmatized 


def remove_stopwords(l):
    """
    Remove English stopwords from a list of strings.

    Args:
        l: A list of strings.

    Returns:
        A list of strings after stop words are removed.
    """
    text_no_sw = [word for word in l if not word in stopwords.words('english')]
    text_no_sw = [word for word in l if not word in stopwords.words('german')]
    return text_no_sw

def re_blob(x):
    return " ".join(x)


def combine_keywords(s):

    s = re.sub('data analyst', ' data_analyst ', s)
    s = re.sub('data analyst', ' data_analyst ', s)
    
    
    s = re.sub('data engineer', ' data_engineer ', s)
    
    s = re.sub('business analyst', ' business_analyst', s)
    s = re.sub('business-analyst', ' business_analyst', s)
    
    s = re.sub('product analyst', 'product_analyst ', s)
    
    s = re.sub('business intelligence analyst', 'business_intelligence_analyst', s)
    s = re.sub('business intelligence', 'business_intelligence_analyst', s)
    s = re.sub('bi ', 'business_intelligence_analyst', s)
    
    s = re.sub('programm manager', 'programm_manager', s)
    
    s = re.sub('software engineer', 'software_engineer', s)
    s = re.sub('software_engin', 'software_engineer', s)

    
    s = re.sub('software developer', 'software_developer', s)
    s = re.sub('software entwickler', 'software_developer', s)
    s = re.sub('softwareentwickler', 'software_developer', s)
    s = re.sub('software_develop', 'software_developer', s)
    s = re.sub('software-entwickl', 'software_developer', s)
    s = re.sub('softwar develop', 'software_developer', s)
    s = re.sub('software_develop', 'software_developer', s)
    
    
    s = re.sub('system engineer', 'system_engineer', s)
    
    s = re.sub('analysis engineer', 'analysis_engineer', s)
    
    s = re.sub('data science', 'data_scientist', s)
    s = re.sub('data scientist', 'data_scientist', s)
    
    
    s = re.sub('machine learn engineer', 'machine_learn_engineer', s)
    s = re.sub('machine learn', 'machine_learn_engineer', s)
    s = re.sub('machine_learn', 'machine_learn_engineer', s)
    s = re.sub('ml ', 'machine_learn_engineer', s)
    
    s = re.sub('ai ', 'ai_engineer', s)
    s = re.sub('artificial intelligence', 'ai_engineer', s)
    
    s = re.sub('cloud', 'cloud_engineer', s)
    
    s = re.sub('devops engineer ', 'devops_engineer', s)
    s = re.sub('devops engin', 'devops_engineer', s)
    s = re.sub('devop engin', 'devops_engineer', s)
    
    
    s = re.sub('devolop engin ', 'develop_engineer', s)
    s = re.sub('entwicklungsingenieur', 'develop_engineer', s)
    
    
    
    s = re.sub('fp & a', 'fp&a_analyst', s)
    
    s = re.sub('deep learn', 'deep_learning', s)
    s = re.sub('reporting analyst', 'reporting_analyst', s)
    
    s = re.sub('sap ', 'sap_specialist', s)

    s = re.sub('data analytics', 'data_analytics', s)
    
    s = re.sub('control', 'controlling_', s)

    s = re.sub('test engin', 'test_engineer', s)
    s = re.sub('test engineer', 'test_engineer', s)
    
    s = re.sub('big data', 'big_data_engineer/specialist', s)
    
    s = re.sub('java', 'java_software_engineer', s)
    s = re.sub('java-', 'java_software_engineer', s)
    s = re.sub('java ', 'java_software_engineer', s)
    
    s = re.sub('backend ', 'backend_developer', s)
    
    s = re.sub('it ', 'it_systemadmin', s)
    
    s = re.sub('data manag ', 'data_management', s)
    
    s = re.sub('full stack ', 'full_stack', s)
    s = re.sub('full-stack ', 'full_stack', s)
    s = re.sub('fullstack ', 'full_stack', s)
    
    s = re.sub('database administr ', 'database_datawarehouse', s)
    s = re.sub('datenbankadministr ', 'database_datawarehouse', s)
    s = re.sub('datenbank-administr ', 'database_datawarehouse', s)
    s = re.sub('datenbank-administr ', 'database_datawarehouse', s)
    s = re.sub('datenbank-administr ', 'database_datawarehouse', s)
    s = re.sub('data warehous', 'database_datawarehouse', s)
    
    
    s = re.sub('research scientist ', 'research_scientist', s)
    s = re.sub('scientist', 'scientist_', s)
    
    s = re.sub('data architect', 'data_architect', s)
    
    
    
    
    return s

def drop_words(s):
    
    droplist = ['campus', 'online', 'remote', 'berlin', 'hamburg', 'frankfurt', 'duales', 'mitarbeiter', 
                'home office', 'teilzeit', 'vollzeit',  ]


def extract_keywords(row):
    
    s = row['cp2_title']
    
    keywords = ['data_analyst', 'software_developer','scientist_','research_scientist', 'data_architect','java_software_engineer','data_engineer', 'database_datawarehouse', 'business_analyst', 'product_analyst', 
                'business_intelligence_analyst', 'full_stack', 'database_administrator', 'fp&a_analyst', 'product_analyst'
                'programm_manager', 'data_analytics', 'big_data_engineer/specialist', 'sap_specialist', 'devops_engineer', 'backend_developer', 'data_management'
               'software_engineer', 'analysis_engineer', 'data_scientist', 'machine_learning_engineer', 'ai_engineer', 'controlling_', 'it_systemadmin'
               'cloud_engineer', 'deep_learning', 'reporting_analyst', 'test_engineer', 'system_engineer', 'specialist', 'sap_specialist']

    for word in keywords:
        if word in s.lower():
            row['new_job_title'] = word


    return row


def extract_level(row):
    student_list = ['werkstudent', 'praktikum','student', 'studium', 'wissenschaftlich', 'pflichtpraktikum', 'intern', 'masterarbeit', 'ausbildung'
                    'bachelorarbeit']
    junior_list = ['junior', 'young professional']
    senior_list = ['senior', 'lead']
    manager_list = ['manager', 'head of', 'head ']
    consultant_list = ['consultant']
    
    s = row['cp2_title']
    
    for word in student_list:
        if word in s.lower():
            row['job_level'] = 'student_level'
            s = re.sub(word, "", s)
            
    for word in junior_list:
        if word in s.lower():
            row['job_level'] = 'junior_level'
            s = re.sub(word, "", s)
    
    for word in consultant_list:
        if word in s.lower():
            row['job_level'] = 'consultant'
            s = re.sub(word, "", s)
            
    for word in senior_list:
        if word in s.lower():
            row['job_level'] = 'senior_level'
            s = re.sub(word, "", s)
            
    for word in manager_list:
        if word in s.lower():
            row['job_level'] = 'manager_level'
            s = re.sub(word, "", s)
            
    row['cp2_title'] = s
    return row
        


# nlp_df['level'] = nlp_df['cp1_title'].apply(lambda x: 'True' if any(word.lower() in x.lower() for word in words_to_find) else 'False')

def word_cloud(df, column):
    title_list = df[column].tolist()

    bag = []
    bag = " ".join(title_list)
    bag
       
    stopwords = STOPWORDS
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(bag)
    rcParams['figure.figsize'] = 10, 20
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    filtered_words = [word for word in bag.split() if word not in stopwords]
    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(10):
        words.append(letter)
        counts.append(count)
    colors = cm.rainbow(np.linspace(0, 1, 10))
    rcParams['figure.figsize'] = 20, 10
    plt.title('Top words in the headlines vs their count')
    plt.xlabel('Count')
    plt.ylabel('Words')
    plt.barh(words, counts, color=colors)
    plt.show()
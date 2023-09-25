from tqdm import tqdm
import pandas as pd 
from langdetect import detect

def check_language(x):
    return detect(x)

def add_language_values_to_df(df):
    final_df = pd.DataFrame(df)

    tqdm.pandas(desc="Processing")
    final_df['language'] = final_df['job_description'].progress_apply(check_language)
    return final_df
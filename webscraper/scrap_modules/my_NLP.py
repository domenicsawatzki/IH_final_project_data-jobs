from tqdm import tqdm
import pandas as pd 
from langdetect import detect

def check_language(x):
    return detect(x)

def add_language_values_to_df(df, search_column, new_column = 'language'):
    final_df = pd.DataFrame(df)

    tqdm.pandas(desc="Processing")
    final_df[new_column] = final_df[search_column].progress_apply(check_language)
    return final_df

def title_pre_processing(x):
    return x


def clean_up(s):
    pattern_to_remove = r'\([a-z]/[a-z]/[a-z]\)'
    s = re.sub(pattern_to_remove, '', s)
    
    s = re.sub('all genders', '', s)


    return s.lower().strip()
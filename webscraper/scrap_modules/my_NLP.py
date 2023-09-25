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
    s = re.sub('/', ' ', s)
    s = re.sub('& ', ' ', s)
    s = re.sub('– ', ' ', s)
    s = re.sub('- ', ' ', s)
    s = re.sub(': ', ' ', s)
    s = re.sub(', ', ' ', s)



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
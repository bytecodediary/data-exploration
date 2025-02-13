import pandas as pd 
import json
import re
import langdetect
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException


#  Making the landuage detector deterministic
DetectorFactory.seed = 0

# download the nltk resources if not available
nltk.download('punkt')

# this code reads the following datasets: .csv, .json, .txt, .xlsx/xls
def load_dataset(file_path):
    # loads the dataset based on its file type
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            with open(file_path, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        elif file_path.endswith('.txt'):
            return pd.read_csv(file_path, delimiter="\t", sep=' ', header=None, names=['Text'])
        elif file_path.endswith('.tsv'):
            return pd.read_csv(file_path, sep='\t', header=None)
        elif file_path.endswith('xlsx') or file_path.endswith('xls'):
            return pd.read_excel(file_path)
            # tokenize_dataset(df)
            # standardize_dataset(df)
            # detect_language_dataset(df)
        else:
            raise ValueError("SORRY! You Provided Unsupported file format.")
        
    except Exception as e:
        print(f"OOHH! NOO! There was An Error Loading the Dataset:{e}")
        return None
    
    # data loading
    dataset = load_dataset(file_path)
    dataset.head()
    
# function to check the whole dataset thoroughly to find any inconsistency 
def check_email_format(email):
    # validates the email format using regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool (re.match(pattern, email))

def detect_language(text):
    # this will detect the language of any given dataset
    try:
        lang = langdetect.detect(text)
        return lang
    except Exception as e:
        print(f"Error Occuring in Detecting Language: {e}")
        
        
def detect_issues(df):
    # checks if the dataset has some common issues and report them
    print("\n **Dataset Overview**")
    print(df.info())
    
    print("\n **Missing Values")
    print(df.isnull().sum())
    
    print("\n **Duplicate Rows**")
    print(f"The total number of duplicates is:{df.duplicated().sum()}")
    
    print("\n **Inconsistent Datatypes**")
    print(df.types)
    
    
    # checking for outliers 
    print("\n Checking for the outliers in the Dataset")
    for col in df.select_dtype(include=['number'].columns):
            outliers = df[df[col]]<df[col].quantile(0.05) | df[col]>df[col].quantile(0.95)
            print (f"Outliers in '{col}': {len(outliers.sum())}")
            
    # checking for inconsistent email format
    print("\n **Incorrect Email Format**")
    if any(df.columns.str.contains("email", case=False)):
        email_col = df.loc[:, df.columns.str.contains("email", case=False)].columns[0]
        invalid_emails = df[df[email_col].astype(str).apply(lambda x: not check_email_format(x))]
        print (f"Number of emails with incorrect format in '{email_col}': {len(invalid_emails)}")
        
    # end of email check
            

# tokenization of the dataset

def tokenize_dataset(df):
    print("\n Tokenizing the first five rows of text columns")
    for col in df.select_dtypes(include=['object']).columns:
        print(f"Tokenization for column:'{col}'")
        for i, text in enumerate(df[col].dropna().head(5), 1):
            words = word_tokenize(text)
            sentences = sent_tokenize(text)
            print (f"Row{i} -words: {words}")
            print (f"Row{i} -sentences: {sentences}")
            
        
# Standardization of the dataset

def standardize_dataset(df):
    print ("\n Standardization issues in the dataset")
    for col in df.select_dtypes(include=['object']).columns:
        mixed_case = df[col].apply(lambda x: x != x.lower() and x != x.upper() if isinstance(x, str) else False)
        print (f"Column '{col}' has mixed case: {mixed_case.sum()}")
        
        # Special characters
        special_chars = df[col].apply(lambda x: bool(re.search(r'[^a-zA-Z0-9\s]', str(x))) if isinstance(x, str) else False)
        print(f"Column'{col}'{special_chars.sum() }rows with special characters")
        
    # end of Standardization of the dataset
    
    
# Language Detect

def detect_language_dataset(df):
    print ("\n Language Detection of the first 5 rows of the dataset")
    for col in df.select_dtype(include=['object']).columns:
        print("\n Language detection for column: '{col}'")
        for i, text in enumerate(df[col].dropna().head(5), 1):
            lang = detect_language_dataset(text)
            print(f"Row{i} - Detected Language: {lang}")
        
# End of language detect


    # checking for invalid IDs (Non Numeric or Too Short)
        print("\n Invalid IDs (Non Numeric or Too Short)")
    if any (df.columns.str.contains("id", case=False)):
        id_col=df.loc[:, df.columns.str.contains ("id", case=False)].columns[0]
        invalid_ids = df[~df[id_col].astype(str).str.isdigit() | (df[id_col].str.len()<5)]
        print (f"Number of invalid IDs in '{id_col}': {len(invalid_ids)}")
    
    
    # formatting issues that leads to trailing spaces
    print ("\n Formatting issues that leads to trailing spaces")
    for col in df.select_types(include  =['object']).columns:
        spaces = df[col].str.startswith("")| df[col].str.endswith("")
        print(f"Column'{col}': {spaces.sum()} rows with extra spaces")
        
        
        
        
        
# data_clean/explore.py
def list_common_errors(dataset):
    errors = []
    # Example error checks
    if dataset.isnull().sum().sum() > 0:
        errors.append("Missing values")
    if dataset.duplicated().any():
        errors.append("Duplicate rows")
    # Add more checks as required
    return errors


def main (file_path):
    df = load_dataset(file_path)
    if df is not None:  
        detect_issues(df)

    else:
        print("Error: unable to load the dataset")
        return None
    
    # example usage:
    # detect_issues("path_to_your_dataset.csv")
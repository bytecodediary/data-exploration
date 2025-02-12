import pandas as pd 
import json
import re


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
            return pd.read_csv(file_path, delimeter="\t", sep=' ', header=None, names=['Text'])
        elif file_path.endswith('.tsv'):
            return pd.read_csv(file_path, sep='\t', header=None)
        elif file_path.endswith('xlsx') or file_path.endswith('xls'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("SORRY! You Provided Unsupported file format.")
        
    except Exception as e:
        print(f"An Error Occurred While Loading the Dataset:{e}")
        return None
    
# function to check the whole dataset thoroughly to find any inconsistency 
def check_email_format(email):
    # validates the email format using regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool (re.match(pattern, email))
def dectect_issues(df):
    # checks if the dataset has some common issues and report them
    print("\n **Dataset Overview**")
    print(df.info())
    
    print("\n **Missing Values")
    print(df.isnull().sum())
    
    print("\n **Duplicate Rows**")
    print(f"The total number of duplicates is:{df.duplicated().sum()}")
    
    print("\n ****")    
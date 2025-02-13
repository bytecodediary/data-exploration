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
            return pd.read_csv(file_path, delimiter="\t", sep=' ', header=None, names=['Text'])
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
    
    print("\n **Inconsistent Datatypes**")
    print(df.types)
    
    
        # checking for outliers 
    print("\n Checking for the outliers in the Dataset")
    for col in df.select_dtypes(include=['number'].columns):
            outliers = df[df[col]]<df[col].quantile(0.05) | df[col]>df[col].quantile(0.95)
            print (f"Outliers in '{col}': {len(outliers.sum())}")
            
    # checking for inconsistent email format
    print("\n **Incorrect Email Format**")
    if any(df.columns.str.contains("email", case=False)):
        email_col = df.loc[:, df.columns.str.contains("email", case=False)].columns[0]
        invalid_emails = df [~df[email_col].astype(str).apply(check_email_format)]
        print(f"Number of invalid emails in '{email_col}': {len(invalid_emails)}")
        
    
    # checking for invalid IDs (Non Numeric or Too Short)
    
    print("\n Invalid IDs (Non Numeric or Too Short)")
    if any (df.columns.str.contains("id", case=False)):
        id_col=df.loc[:, df.columns.str.contains ("id", case=False)].columns[0]
        invalid_ids = df[~df[id_col].astype(str).str.isdigit() | (df[id_col].str.len()<5)]
        print (f"Number of invalid IDs in '{id_col}': {len(invalid_ids)}")
    
    
    # formatting issues that leads to trailing spaces
    for col in df.select_types(include  =['object']).columns:
        spaces = df[col].str.startswith("")| df[col].str.endswith("")
        print(f"Column'{col}': {spaces.sum()} rows with extra spaces")


def main (file_path):
    df = load_dataset(file_path)
    if df is not None:  
        detect_issues(df)

    else:
        print("Error: unable to load the dataset")
        return None
    
    # example usage:
    # detect_issues("path_to_your_dataset.csv")
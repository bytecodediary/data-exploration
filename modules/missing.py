import pandas as pd

def read_file(file_path):
    """Reads any file format and returns a DataFrame."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    elif file_path.endswith('.parquet'):
        return pd.read_parquet(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV, Excel, JSON, or Parquet.")

def handle_missing_values(df, threshold=0.5):
    """
    Handles missing values in a dataset dynamically based on data type and threshold.
    - Drops columns with missing values above threshold.
    - Fills numeric columns using mean, median, or mode.
    - Fills categorical columns using mode, forward fill, or backward fill.
    - Uses interpolation for time-series data.
    """
    
    # Drop columns with missing values above threshold
    df = df.dropna(axis=1, thresh=int(threshold * len(df)))
    
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            print(f"Handling {missing_count} missing values in column: {col}")
            
            if df[col].dtype in ['int64', 'float64']:  # Numeric columns
                if df[col].is_monotonic_increasing or df[col].is_monotonic_decreasing:
                    df[col] = df[col].interpolate()  # Interpolation for time-series
                else:
                    df[col].fillna(df[col].mean(), inplace=True)  # Default: Fill with mean
                    
            elif df[col].dtype == 'object':  # Categorical columns
                if df[col].nunique() <= 5:  # Small unique values (likely categorical)
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    df[col].fillna(method='ffill', inplace=True)  # Forward fill
            
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)  # Default mode fill
    
    return df

# Example usage
if __name__ == "__main__":
    file_path = "your_dataset.csv"  # Update with your dataset file
    df = read_file(file_path)
    cleaned_df = handle_missing_values(df)
    cleaned_df.to_csv("cleaned_dataset.csv", index=False)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    print("Data cleaning complete. Saved as cleaned_dataset.csv") 
import pandas as pd
import requests
from io import StringIO

def download_csv(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text), delimiter='|', quotechar='"', on_bad_lines='skip')
    else:
        print("Failed to download the file. Status Code:", response.status_code)
        return None

def fill_empty_cells(df):
    df.ffill(inplace=True)
    print("Empty cells filled successfully!")

def filter_record_type(df, record_type):
    return df[df['RECORD_TYPE'] == record_type].copy()

def add_veznik_column(df):
    df['VEZNIK'] = df['SKU'].apply(lambda x: str(x).split('_')[0].split('-')[0])
    print("VEZNIK column added successfully!")

def transform_and_save_csv(df, output_file, record_type):
    try:
        # Print the original DataFrame for debugging
        print("First few rows of the original DataFrame:")
        print(df.head())

        # Fill empty cells
        fill_empty_cells(df)

        # Filter the DataFrame to keep only rows where RECORD_TYPE is the specified type
        df_filtered = filter_record_type(df, record_type)
        print(f"Filtered DataFrame to keep only rows where RECORD_TYPE is '{record_type}'")

        # Add VEZNIK column
        add_veznik_column(df_filtered)

        # List of columns to remove
        columns_to_remove = [
            'Titel_ITA', 'Description_ITA',
            'Titel_ES', 'Description_ES',
            'Titel_FR', 'Description_FR',
            'Titel_DE', 'Description_DE',
            'Titel_BG', 'Description_BG',
            'Titel_PL', 'Description_PL',
            'Titel_CZ', 'Description_CZ',
            'Titel_SK', 'Description_SK',
            'Titel_HU', 'Description_HU',
            'Titel_RO', 'Description_RO'
        ]
        df_filtered.drop(columns=columns_to_remove, errors='ignore', inplace=True)

        # Save the modified DataFrame to a new CSV file
        df_filtered.to_csv(output_file, index=False)
        print(f"Data transformation successful! Transformed file saved as '{output_file}'")

        # Print the transformed DataFrame for debugging
        print("First few rows of the transformed DataFrame:")
        print(df_filtered.head())
        
    except Exception as e:
        print("An error occurred:", str(e))

# URL of the CSV file
url = "https://feed.stockfirmati.com/csv/exportdropclang.csv"

# Output file name
output_file = "final_transformed_file.csv"

# Desired record type to keep
record_type_to_keep = "MODEL"

# Download the CSV file and load it into a DataFrame
df = download_csv(url)
if df is not None:
    # Call the function to transform and save the CSV file
    transform_and_save_csv(df, output_file, record_type_to_keep)

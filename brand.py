import pandas as pd
import requests
from io import StringIO

# List of brand names to filter
brands_to_filter = [
   "CALVIN KLEIN", "TOMMY HILFIGER", "U.S. POLO", "U.S. POLO BEST PRICE",
    "U.S. POLO ASSN.", "U.S. GRAND POLO", "NORTH SAILS", "GANT",
    "NORWAY 1963", "NAPAPIJRI", "NAPAPIJRI SHOES", "HARMONT & BLAINE",
    "LEVI'S", "SERGIO TACCHINI", "HARMONT & BLAINE", "GAS", "GIUESS JEANS",
    "KARL LAGERFELD BEACHWEAR", "LA MARTINA", "LEVI'S", "DESIGUAL", "MARES",
    "PIQUADRO", "PLEIN SPORT", "RALPH LAUREN", "TIMBERLAND", "VALENTINO BAGS",
    "VANS", "GUESS JEANS"
]

# URL of the CSV to manipulate
csv_url = 'https://raw.githubusercontent.com/Camarolli9979797/wp_all_import/main/final_transformed_file.csv'

# Output file path - This should be relative to your GitHub repository
output_file = 'new_filtered.csv' # Adjust the path as needed

# Function to filter CSV and save
def filter_and_save_csv(url, brands, output_path):
    # Download CSV from the specified URL
    response = requests.get(url)
    response.raise_for_status()

    # Read CSV into a DataFrame with ',' as delimiter and 'utf-8' encoding
    df = pd.read_csv(StringIO(response.text), delimiter=',', quotechar='"', on_bad_lines='skip', dtype=str, encoding='utf-8')

    # Check if 'BRAND' column exists in the DataFrame
    if 'BRAND' in df.columns:
        # Filter the DataFrame for the selected brands
        df_filtered = df[df['BRAND'].isin(brands)]

        # Select the required columns, ensuring they exist in the DataFrame
        columns_required = ['QUANTITY', 'ï»¿ORDERCODE']
        existing_columns = [col for col in columns_required if col in df_filtered.columns]
        if 'ORDERCODE' in df_filtered.columns:
            existing_columns.append('ORDERCODE')
        df_filtered = df_filtered[existing_columns]
        
        # Additional filtering: Remove rows containing specific strings
        strings_to_remove = ['Za djevojčice', 'Za dječake']
        df_filtered = df_filtered[~df_filtered.apply(lambda row: row.astype(str).str.contains('|'.join(strings_to_remove)).any(), axis=1)]

        # Write the filtered data to the specified output file
        df_filtered.to_csv(output_path, index=False)
        print(f"Filtered CSV saved to {output_path}")
    else:
        print("The 'BRAND' column does not exist in the CSV file.")

# Main function to run the script
def main():
    filter_and_save_csv(csv_url, brands_to_filter, output_file)

if __name__ == "__main__":
    main()

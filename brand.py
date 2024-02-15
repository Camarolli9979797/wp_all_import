import pandas as pd
import requests
from io import StringIO
import os

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

# Output file path
output_file = 'new_filtered.csv'  # Adjust the path as needed

# Path for last run's data for comparison
last_run_file = 'last_run.csv'  # Adjust the path as needed

# Function to filter CSV, compare with last run, and save if different
def filter_and_save_csv(url, brands, output_path, last_run_path):
    # Download CSV from the specified URL
    response = requests.get(url)
    response.raise_for_status()

    # Read CSV into a DataFrame
    df = pd.read_csv(StringIO(response.text), delimiter=',', quotechar='"', on_bad_lines='skip', dtype=str, encoding='utf-8')

    # Filter for selected brands if 'BRAND' column exists
    if 'BRAND' in df.columns:
        df_filtered = df[df['BRAND'].isin(brands)]

        # Ensure required columns exist
        columns_required = ['QUANTITY', 'SKU']
        existing_columns = [col for col in columns_required if col in df_filtered.columns]
        if 'ORDERCODE' in df_filtered.columns:  # Adjusting for potential column name discrepancy
            existing_columns.append('ORDERCODE')
        df_filtered = df_filtered[existing_columns]

        # Load last run's data for comparison, if it exists
        if os.path.exists(last_run_path):
            df_last_run = pd.read_csv(last_run_path, dtype=str)
            # Compare with last run to find changed rows
            df_changes = pd.concat([df_filtered, df_last_run]).drop_duplicates(keep=False)
        else:
            # If no last run data, consider all current rows as changed
            df_changes = df_filtered

        # If there are changes, update last run snapshot and write new output
        if not df_changes.empty:
            df_filtered.to_csv(last_run_path, index=False)  # Update snapshot
            df_changes.to_csv(output_path, index=False)  # Write only changed rows
            print(f"Changes detected and saved to {output_path}")
        else:
            print("No changes detected since last run.")
    else:
        print("The 'BRAND' column does not exist in the CSV file.")

# Main function to run the script
def main():
    filter_and_save_csv(csv_url, brands_to_filter, output_file, last_run_file)

if __name__ == "__main__":
    main()

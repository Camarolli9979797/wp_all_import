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

# Output file path
output_file = 'filtered_output.csv'  # Adjust the path as needed

# Function to filter CSV and save required columns
def filter_and_save_csv(url, brands, output_path):
    # Download CSV from the specified URL
    response = requests.get(url)
    response.raise_for_status()

    # Read CSV into a DataFrame
    df = pd.read_csv(StringIO(response.text), delimiter=',', quotechar='"', on_bad_lines='skip', dtype=str, encoding='utf-8')

    # Filter for selected brands if 'BRAND' column exists
    if 'BRAND' in df.columns:
        df_filtered = df[df['BRAND'].isin(brands)]
        
        # Select and rename columns
        if 'ORDERCODE' in df_filtered.columns:
            df_filtered = df_filtered[['ORDERCODE', 'QUANTITY']].rename(columns={'ORDERCODE': 'SKU'})
        elif 'ï»¿ORDERCODE' in df_filtered.columns:  # Handling potential encoding prefix
            df_filtered = df_filtered[['ï»¿ORDERCODE', 'QUANTITY']].rename(columns={'ï»¿ORDERCODE': 'SKU'})

        # Write output
        df_filtered.to_csv(output_path, index=False)
        print(f"Filtered data saved to {output_path}")
    else:
        print("The 'BRAND' column does not exist in the CSV file.")

# Main function to run the script
def main():
    filter_and_save_csv(csv_url, brands_to_filter, output_file)

if __name__ == "__main__":
    main()

import pandas as pd
import requests
from io import StringIO

# Brands to filter
brands_to_keep = [
    "CALVIN KLEIN", "TOMMY HILFIGER", "U.S. POLO", "U.S. POLO BEST PRICE",
    "U.S. POLO ASSN.", "U.S. GRAND POLO", "NORTH SAILS", "GANT", "NORWAY 1963",
    "NAPAPIJRI", "NAPAPIJRI SHOES", "HARMONT & BLAINE", "LEVI'S", "SERGIO TACCHINI",
    "GAS", "GIUESS JEANS", "KARL LAGERFELD BEACHWEAR", "LA MARTINA", "DESIGUAL",
    "MARES", "PIQUADRO", "PLEIN SPORT", "RALPH LAUREN", "TIMBERLAND", "VALENTINO BAGS",
    "VANS", "GUESS JEANS"
]

# Download CSV
def download_csv(url):
    response = requests.get(url)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    return pd.read_csv(StringIO(response.text), delimiter=';', quotechar='"', on_bad_lines='skip', dtype=str)

# Filter and save CSV
def filter_and_save_csv(df, brands, output_path):
    # Filter the DataFrame for the selected brands
    df_filtered = df[df['BRAND'].isin(brands)]

    # Select the required columns
    columns_required = ['SKU', 'QUANTITY', 'PICTURE_1', 'VEZNIK', 'BARCODE', 'Brand', 'ï»¿ORDERCODE', 'BRAND', 'SEX']
    df_filtered = df_filtered[columns_required]

    # Write the filtered data to a new CSV file
    df_filtered.to_csv(output_path, index=False)
    print("Filtered CSV saved to", output_path)

# Main function to run the script
def main(csv_url, output_file):
    df = download_csv(csv_url)
    filter_and_save_csv(df, brands_to_keep, output_file)

# Define the CSV path and output file
csv_url = 'https://feed.stockfirmati.com/csv/exportdropclang.csv'
output_file = 'filtered_stock_management.csv'

# Run the script
if __name__ == "__main__":
    main(csv_url, output_file)

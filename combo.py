import pandas as pd
import requests
from io import StringIO
import re

# Translation dictionary
translations = {
    "A spalla": "Na ramenu", "Sandals": "Sandale", "Scarves": "Šalovi", "Slippers": "Papuče",
    "Occhiali da Sole": "Sunčane naočale", "Ties": "Kravate", "Necklaces": "Ogrlice", "Cinture": "Remeni",
    "Body": "Tijelo", "Guanti": "Rukavice", "Zaini": "Ruksaci", "Sneakers": "Tenisice",
    "Classica": "Klasična", "Stivaletti": "Gležnjače", "Calzini": "Čarape", "Polo": "Polo majice",
    "Giubbotti e piumini": "Jakne", "Giacche": "Jakne", "Borse": "Torbe",
    "Portafogli": "Novčanici", "Felpe": "Veste i majice s kapuljačom", "Abiti": "Odjeća", "Accessori": "Dodaci",
    "Maglie": "Dresovi", "Gonne": "Suknje", "Camicie": "Košulje", "T-Shirt": "Majice", "Mare": "More",
    "Cappelli": "Kape", "Intimo": "Donje rublje", "Jeans": "Traperice", "Pantaloni": "Hlače",
    "Abbigliamento": "Odjeća", "Borse": "Torbe", "Accessori": "Dodaci", "Scarpe": "Obuća",
    "Blu": "Plavo", "Giallo": "Žuto", "Nero": "Crno", "Bianco": "Bijelo", "Rosso": "Crveno",
    "Azzurro": "Svijetloplavo", "Grigio": "Sivo", "Verde": "Zeleno", "Viola": "Ljubičasto",
    "Arancione": "Narančasto", "Beige": "Bež", "Rosa": "Ružičasto", "Marrone": "Smeđe",
    "Multicolore": "Višebojno", "Oro": "Zlatno", "Argento": "Srebrno", "Turchese": "Tirkizno",
    "Bronzo": "Brončano", "donna": "Žensko", "uomo": "Muško", "bambina": "Za djevojčice", "bambino": "Za dječake", 
  "COTONE": "Pamuk",
  "ELASTAN": "Elastan",
  "LINO": "Lan",
  "NYLON": "Najlon",
  "POLIESTERE": "Poliester",
  "MODAL": "Modal",
  "LANA": "Vuna",
  "ACRILICO": "Akril",
  "VISCOSA": "Viskoza",
  "ELASTOMERO": "Elastomer",
  "SETA": "Svila",
  "PELLE": "Koža",
  "TESSUTO": "Tkanina",
  "METALLO": "Metal",
  "LYCRA": "Likra",
  "CACHEMIRE": "Kašmir",
  "FODERA": "Podstava",
  "ACETATO": "Acetat",
  "POLIAMMIDE": "Poliamid",
  "IMBOTTITURA": "Punjenje",
  "PIUMA": "Perje",
  "PIUMETTA": "Paperje",
  "CUPRO": "Cupro",
  "POLIURETANO": "Poliuretan",
  "SPANDEX": "Spandex",
  "CUOIO": "Skriveno",
  "MATERIE": "Materijali",
  "SINTETICO": "Sintetičko",
  "GOMMA": "Guma",
  "MATERIALI SINTETICI": "Sintetički materijali",
  "ALTRI": "Ostalo",
  "VERO": "Pravi",
  "THERMOPLASTIC": "Termoplastika",
  "INIETTATO": "Injektirano",
  "CORPO": "Tijelo",
  "INFERIORE": "Donji",
  "MANICHE": "Rukavi",
  "RAYON": "Rajon",
  "SUPERIORE": "Gornji",
  "SUOLA": "Potplat",
  "NON DISPONIBILE": "Nije dostupno",
  "ECO": "Ekološki",
  "MERINO": "Merino",
  "DENIM": "Traper",
  "SUEDE": "Antilop",
  "PIUMINO D'ANATRA": "Duga jakna",
  "INSERTO": "Umetak",
  "VERGINE": "Djevičanski",
  "PARTE": "Dio",
  "EVA": "EVA",
  "FIBRA": "Vlakno",
  "METALLISED": "Metalizirano",
  "FIBER": "Vlakna",
  "ECOPELLE": "Ekokoža",
  "ELASTERELLE": "Elasterell",
  "ELASTIC FORCE": "Elastična sila",
  "RUBBER SUEDE": "Gumeni antilop",
  "RPET": "Rpet",
  "ECONYL": "Econyl",
  "PANTOGRAFATO": "Gravirano",
  "PLASTICA": "Plastika",
  "Poliuretano Poliestere": "Poliuretan Poliester",
  "Cotone": "Pamuk",
  "Poliammide": "Poliamid",
  "Elastan": "Elastan",
  "Tessuto": "Tkanina",
  "Cachemire": "Kašmir",
  "Sandali": "Sandale",
  "Sciarpe": "Šalovi",
  "Ciabatte": "Papuče/Japanke",   
  "Cravatte": "Kravate",
  "Gilet": "Prsluk"
  
}

def translate_substrings(df, columns):
    for col in columns:
        if col in df.columns:
            for key, value in translations.items():
                df[col] = df[col].str.replace(r'\b{}\b'.format(re.escape(key)), value, regex=True)
    print("Substrings translated successfully!")

def download_csv(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text), delimiter='|', quotechar='"', on_bad_lines='skip', dtype=str)
    else:
        print("Failed to download the file. Status Code:", response.status_code)
        return None

def fill_empty_cells(df):
    df.ffill(inplace=True)
    print("Empty cells filled successfully!")

def filter_record_type(df, record_type):
    return df[df['RECORD_TYPE'] == record_type].copy()

def add_veznik_column(df):
    df['VEZNIK'] = df['SKU'].apply(lambda x: x.split('_')[0] if "_" in x else x)
    print("VEZNIK column added successfully!")


def transform_and_save_csv(df, output_file, record_type):
    try:
        print("First few rows of the original DataFrame:")
        print(df.head())

        fill_empty_cells(df)

        df_filtered = filter_record_type(df, record_type)
        print(f"Filtered DataFrame to keep only rows where RECORD_TYPE is '{record_type}'")

        add_veznik_column(df_filtered)

        # Translate specific columns
        translate_substrings(df_filtered, ['CAT', 'SUBCAT', 'COLOR', 'MATERIAL', 'SEX'])

        # List of columns to remove


        df_filtered.to_csv(output_file, index=False)
        print(f"Data transformation successful! Transformed file saved as '{output_file}'")
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
    transform_and_save_csv(df, output_file, record_type_to_keep)

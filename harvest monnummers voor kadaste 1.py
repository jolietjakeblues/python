import pandas as pd
import requests
import os

# Functie om API aan te roepen en gegevens op te halen
def fetch_data_from_api(monnr):
    url = f"https://api.linkeddata.cultureelerfgoed.nl/queries/rce/Query-5-4-1/11/run?rm={monnr}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            return data  # Return alle items in de lijst
    return None

# Functie om het hoofdscript uit te voeren
def main():
    # Pad naar het oorspronkelijke CSV-bestand
    input_csv_path = r"C:\Users\linkeddata\Downloads\Albert\rm_alle.csv"
    
    # Pad voor het nieuwe CSV-bestand
    output_csv_path = r"C:\Users\linkeddata\Downloads\Albert\rm_alle_ingevuld.csv"

    # Laden van het CSV-bestand in een pandas DataFrame
    df = pd.read_csv(input_csv_path, delimiter=';')

    # Aanmaken van een lege DataFrame om alle gegevens op te slaan
    all_data = []

    # Aantal rijen in het dataframe voor de voortgangsindicator
    total_rows = len(df)

    # Voortgangsindicator initialiseren
    print("Verwerken van rijksmonumenten:")
    print("[", end="", flush=True)

    # Itereren over elk rijksmonumentnummer (Monnr.)
    for index, row in df.iterrows():
        monnr = row['Monnr.']
        
        # API aanroepen om gegevens op te halen
        api_data = fetch_data_from_api(monnr)

        if api_data:
            # Itereren over elk perceel en gegevens toevoegen aan de lijst
            for perceel_data in api_data:
                all_data.append({
                    'Monnr.': monnr,
                    'perceel': perceel_data.get('perceel', ''),
                    'sectie': perceel_data.get('sectie', ''),
                    'gemeentenaam': perceel_data.get('gemeentenaam', ''),
                    'origineleGemeentecode': perceel_data.get('kadastraleGemeentecode', ''),
                    'aangepasteGemeentecode': perceel_data.get('kadastraleGemeentecode', ''),
                    'cbscode': perceel_data.get('cbscode', '')
                })
        else:
            # Als er geen gegevens zijn, lege waarden toevoegen voor het monument
            all_data.append({
                'Monnr.': monnr,
                'perceel': '',
                'sectie': '',
                'gemeentenaam': '',
                'origineleGemeentecode': '',
                'aangepasteGemeentecode': '',
                'cbscode': ''
            })

        # Voortgangsindicator bijwerken
        if index % 10 == 0:  # Update elke 10 rijen
            print("=", end="", flush=True)

    # Voortgangsindicator afronden
    print("]")

    # Omzetten van de lijst met alle gegevens naar een DataFrame
    result_df = pd.DataFrame(all_data)

    # Opslaan van het dataframe naar een nieuw CSV-bestand
    result_df.to_csv(output_csv_path, sep=';', index=False)

    print(f"\nNieuw bestand opgeslagen op: {output_csv_path}")

# Uitvoeren van het hoofdscript als het bestand direct wordt uitgevoerd
if __name__ == "__main__":
    main()

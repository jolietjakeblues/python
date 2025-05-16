import pandas as pd
import requests
import os

# Functie om API aan te roepen en gegevens op te halen
def fetch_data_from_api(monnr):
    url = f"https://api.linkeddata.cultureelerfgoed.nl/queries/rce/Query-5-4-1/12/run?rm={monnr}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            return data  # Return alle items in de lijst
    return None

# Functie om een batch van gegevens op te slaan in een CSV-bestand
def save_batch_to_csv(batch_data, batch_index, output_dir):
    batch_df = pd.DataFrame(batch_data)
    batch_file_path = os.path.join(output_dir, f'rm_alle_ingevuld_batch_{batch_index}.csv')
    batch_df.to_csv(batch_file_path, sep=';', index=False)
    print(f"Batch {batch_index} opgeslagen op: {batch_file_path}")

# Functie om het hoofdscript uit te voeren
def main():
    # Pad naar het oorspronkelijke CSV-bestand
    input_csv_path = r"C:\Users\linkeddata\Downloads\Albert\rm_alle.csv"
    
    # Pad voor de output directory
    output_dir = r"C:\Users\linkeddata\Downloads\Albert"
    
    # Laden van het CSV-bestand in een pandas DataFrame
    df = pd.read_csv(input_csv_path, delimiter=';')

    # Aantal rijen in het dataframe voor de voortgangsindicator
    total_rows = len(df)
    
    # Batch grootte instellen
    batch_size = 10000
    batch_data = []
    batch_index = 1

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
                batch_data.append({
                    'Monnr.': monnr,
                    'perceel': perceel_data.get('perceel', ''),
                    'sectie': perceel_data.get('sectie', ''),
                    'gemeentenaam': perceel_data.get('gemeentenaam', ''),
                    'origineleGemeentecode': perceel_data.get('kadastraleGemeentecode', ''),
                    'GemeentecodeUri': perceel_data.get('kadastraleGemeenteUri', ''),
                    'cbscode': perceel_data.get('cbscode', '')
                })
        else:
            # Als er geen gegevens zijn, lege waarden toevoegen voor het monument
            batch_data.append({
                'Monnr.': monnr,
                'perceel': '',
                'sectie': '',
                'gemeentenaam': '',
                'origineleGemeentecode': '',
                'GemeentecodeUri': '',
                'cbscode': ''
            })

        # Voortgangsindicator bijwerken
        if index % 10 == 0:  # Update elke 10 rijen
            print("=", end="", flush=True)
        
        # Controleren of de batchgrootte is bereikt
        if (index + 1) % batch_size == 0 or (index + 1) == total_rows:
            save_batch_to_csv(batch_data, batch_index, output_dir)
            batch_data = []
            batch_index += 1

    # Voortgangsindicator afronden
    print("]")

    print(f"\nVerwerking voltooid. Tussentijdse resultaten zijn opgeslagen in batches in de directory: {output_dir}")

# Uitvoeren van het hoofdscript als het bestand direct wordt uitgevoerd
if __name__ == "__main__":
    main()

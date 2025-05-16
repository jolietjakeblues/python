import pandas as pd
import requests

# Functie om API aan te roepen en gegevens op te halen
def fetch_data_from_api(gemeente_uri, sectie, perceelnummer):
    try:
        perceelnummer = int(perceelnummer)  # Probeer perceelnummer naar integer te converteren
    except (ValueError, TypeError):
        print(f"Fout: Ongeldige perceelnummerwaarde: {perceelnummer}")
        return None
    # Monnr.;perceel;sectie;gemeentenaam;origineleGemeentecode;GemeentecodeUri;cbscode 
    url = f"https://api.linkeddata.cultureelerfgoed.nl/queries/rce/Percelen-bij-kadaster-1/7/run?sectie={sectie}&perceelnummer={perceelnummer}&gemeente={gemeente_uri}"
    print(f"API URL: {url}")  # Print de URL om te controleren of deze correct is
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"API Response: {data}")  # Print de volledige API-respons om te controleren
        if data and isinstance(data, list) and len(data) > 0:
            return data[0]  # Return eerste item in de lijst
        else:
            print("Geen gegevens gevonden in de API-respons.")
    else:
        print(f"Fout bij API-aanroep. Status code: {response.status_code}")
    return None

# Functie om het hoofdscript uit te voeren
def main():
    # Pad naar het oorspronkelijke CSV-bestand
    input_csv_path = r"C:\Users\linkeddata\Downloads\Albert\alle_perceel_csv\alle_perceelInformatie_kort.csv"
    
    # Pad voor het nieuwe CSV-bestand
    output_csv_path = r"C:\Users\linkeddata\Downloads\Albert\alle_perceel_csv\alle_perceelInformatie_kort_kad.csv"

    # Laden van het CSV-bestand in een pandas DataFrame
    df = pd.read_csv(input_csv_path, delimiter=';')

    # Aanmaken van lege lijsten om gegevens op te slaan
    oppervlakte_list = []
    aanduiding_list = []

    # Aantal rijen in het dataframe voor de voortgangsindicator
    total_rows = len(df)

    # Voortgangsindicator initialiseren
    print("Verwerken van gegevens:")
    print("[", end="", flush=True)

    # Itereren over elk rijksmonument om gegevens op te halen
    for index, row in df.iterrows():
        if index >= 100:  # Stop na 100 resultaten
            break
        
        sectie = row['sectie']
        perceelnummer = row['perceelnummer']
        gemeente_uri = row['gemeentecodeUri']
        
        # Controleer of perceelnummer een geldige numerieke waarde heeft
        if pd.notna(perceelnummer) and not pd.isnull(perceelnummer) and pd.notna(pd.to_numeric(perceelnummer, errors='coerce')):
            api_data = fetch_data_from_api(gemeente_uri, sectie, perceelnummer)
        else:
            print(f"Rij {index}: Ongeldige waarde voor perceelnummer: {perceelnummer}. Overslaan.")
            api_data = None

        if api_data:
            oppervlakte_list.append(api_data.get('oppervlakte', ''))
            aanduiding_list.append(api_data.get('aanduiding', 'Niet beschikbaar'))  # Voeg de aanduiding uit de API-respons toe
        else:
            oppervlakte_list.append('')
            aanduiding_list.append('Niet beschikbaar')

        # Voortgangsindicator bijwerken
        if index % 10 == 0:  # Update elke 10 rijen
            print("=", end="", flush=True)

    # Voortgangsindicator afronden
    print("]")

    # Toevoegen van oppervlakte en aanduiding aan het oorspronkelijke dataframe
    df['oppervlakte'] = oppervlakte_list
    df['aanduiding'] = aanduiding_list

    # Opslaan van het dataframe naar een nieuw CSV-bestand
    df.to_csv(output_csv_path, sep=';', index=False)

    print(f"\nNieuw bestand opgeslagen op: {output_csv_path}")

# Uitvoeren van het hoofdscript als het bestand direct wordt uitgevoerd
if __name__ == "__main__":
    main()

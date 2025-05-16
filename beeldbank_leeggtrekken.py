import requests
import csv
import time
import os

# Basis URL en API key voor het verzoek
BASE_URL = "https://webservices.picturae.com/mediabank/media"
API_KEY = "50cc410d-09d5-4874-ad11-edf41a0e8064"
LANG = "nl"

# Functie om een alternatieve nummerlijst in te lezen uit een CSV-bestand
def read_alternative_numbers_from_csv(file_name):
    alternative_numbers = []
    with open(file_name, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            alternative_numbers.append(row['identifier'])  # Neem de waarde uit de kolom 'identifier'
    return alternative_numbers

# Functie om resultaten direct toe te voegen aan een CSV-bestand (regel voor regel)
def write_row_to_csv(row_data, file_name):
    file_exists = os.path.isfile(file_name)
    with open(file_name, mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['label', 'id', 'entity_uuid', 'title', 'asset_uuid', 'Vervaardiger', 'Vervaardigingsdatum', 'Trefwoorden']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Schrijf de header alleen als het bestand nog niet bestaat

        writer.writerow(row_data)
        csv_file.flush()  # Flush de data naar de schijf om verlies te voorkomen

    print(f"Rij toegevoegd aan {file_name}")

# Functie om API-verzoeken uit te voeren voor elk alternatief nummer en data te verwerken
def fetch_data(alternative_numbers, output_file):
    for alt_num in alternative_numbers:
        params = {
            'apiKey': API_KEY,
            'lang': LANG,
            'fq[]': f'search_s_alternative_numbers_alternative_number:{alt_num}',
            'rows': 100,  # Aantal resultaten per pagina
            'page': 1     # Start op pagina 1
        }
        print(f"Bezig met het ophalen van data voor alternatief nummer: {alt_num}...")
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                media_data = response.json().get('media', [])
                if not media_data:
                    print(f"Geen resultaten voor alternatief nummer: {alt_num}")
                    continue

                for item in media_data:
                    creators = next((meta['value'] for meta in item['metadata'] if meta['field'] == 'creators'), None)
                    production_date = next((meta['value'] for meta in item['metadata'] if meta['field'] == 'production_date'), None)
                    trefwoorden = next((meta['value'] for meta in item['metadata'] if meta['field'] == 'trefwoorden'), None)
                    
                    for asset in item['asset']:
                        result = {
                            'label': alt_num,
                            'id': item['id'],
                            'entity_uuid': item['entity_uuid'],
                            'title': item.get('title', ''),
                            'asset_uuid': asset['uuid'],
                            'Vervaardiger': creators,
                            'Vervaardigingsdatum': production_date,
                            'Trefwoorden': trefwoorden
                        }
                        # Voeg elke regel direct toe aan het CSV-bestand
                        write_row_to_csv(result, output_file)
                
                print(f"Data voor alternatief nummer {alt_num} opgehaald.")
            else:
                print(f"Fout bij ophalen van data voor alternatief nummer {alt_num}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Er is een fout opgetreden bij het ophalen van data voor alternatief nummer {alt_num}: {str(e)}. Probeer opnieuw...")
            time.sleep(5)  # Wacht even voordat je het opnieuw probeert

        time.sleep(0.2)  # Kleine pauze tussen aanvragen om rate limiting te vermijden

# Vraag naar de bestandsnaam van de CSV met alternatieve nummers
input_file = input("Geef de naam van de CSV met alternatieve nummers: ")

# Controleer of het bestand bestaat
if not os.path.isfile(input_file):
    print(f"Bestand {input_file} bestaat niet. Zorg ervoor dat de juiste bestandsnaam is opgegeven.")
    exit()

# Lees alternatieve nummers uit de CSV
alternative_numbers = read_alternative_numbers_from_csv(input_file)

# Vraag naar de bestandsnaam voor de output CSV
output_file = input("Geef de naam voor de output CSV file: ")

# Probeer het proces te draaien en zorg dat resultaten direct worden toegevoegd aan het CSV-bestand
try:
    # Haal data op voor elk alternatief nummer en voeg deze direct toe aan de CSV
    fetch_data(alternative_numbers, output_file)

except KeyboardInterrupt:
    print("\nHet proces is handmatig onderbroken.")
finally:
    print(f"Het proces is voltooid. Alle tot nu toe verwerkte data is opgeslagen in {output_file}.")

import csv
import json
import os

def convert_json_to_csv(input_file, output_file):
    # Headers voor de CSV
    headers = [
        "Alternative Title",
        "Archis ID",
        "Archis Zaakidentificatie",
        "Audience",
        "Author",
        "Bag ID",
        "Collection",
        "Contributor",
        "Deposit Date",
        "Depositor",
        "Description",
        "Distribution Date",
        "DV PID Version",
        "DV PID",
        "Language Of Metadata",
        "Language",
        "License/Data Use Agreement",
        "Methods of Recovery (ABR Verwervingswijzen)",
        "NBN",
        "Other Identifier",
        "Persistent Identifier",
        "Personal Data In Dataset?",
        "Point of Contact",
        "Producer",
        "Production Date",
        "Production Location",
        "Publication Date",
        "Rapportnummer",
        "Report (ABR Rapporten)",
        "Rights Holder",
        "Series",
        "Spatial Coverage (Free Text)",
        "Spatial Coverage",
        "Spatial Point",
        "Subject",
        "Subtitle",
        "Title"
    ]

    # JSON-gegevens laden
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Gegevens schrijven naar CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        total_records = len(data)
        for index, record in enumerate(data.values(), start=1):
            # Alleen de velden schrijven die overeenkomen met de headers
            filtered_record = {key: record.get(key, '') for key in headers}
            writer.writerow(filtered_record)
            # Voortgangsindicator weergeven
            print(f'Voortgang: {index}/{total_records}', end='\r')

    print('\nConversie voltooid.')

# Invoer bestandsnaam vragen
input_file = input("Geef de bestandsnaam van het JSON-bestand: ")

# Uitvoer bestandsnaam vragen
output_file = input("Geef de gewenste bestandsnaam voor het CSV-bestand: ")

# Controleren of het invoerbestand bestaat
if not os.path.exists(input_file):
    print("Fout: Het opgegeven invoerbestand bestaat niet.")
else:
    # JSON naar CSV converteren
    convert_json_to_csv(input_file, output_file)

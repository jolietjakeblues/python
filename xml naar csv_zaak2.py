import csv
import xml.etree.ElementTree as ET

def extract_data(input_file):
    # Initialisatie van lijst met gegevensrijen
    rows = []

    # Begin met het lezen van het XML-bestand
    context = ET.iterparse(input_file, events=('start', 'end'))
    event, root = next(context)

    # Voor elke XML-element in de stroom
    for event, elem in context:
        if event == 'end' and elem.tag == 'zaak':
            # Informatie over de zaak
            zaak_id = elem.find('zaakId').text if elem.find('zaakId') is not None else ""
            zaak_nummer = elem.find('zaaknummer').text if elem.find('zaaknummer') is not None else ""
            zaak_type = elem.find('zaaktype').text if elem.find('zaaktype') is not None else ""

            # Informatie over zaakobject
            zaakobject = elem.find('.//zaakobject')
            cho_id = zaakobject.find('choId').text if zaakobject is not None and zaakobject.find('choId') is not None else ""
            type_cho = zaakobject.find('typeCho').text if zaakobject is not None and zaakobject.find('typeCho') is not None else ""

            # Informatie over eigenschappen
            eigenschappen = {}
            for eigenschap in elem.findall('.//eigenschap'):
                eigenschap_naam = eigenschap.find('eigenschapnaam').text if eigenschap.find('eigenschapnaam') is not None else ""
                eigenschap_waarde = eigenschap.find('eigenschapwaarde').text if eigenschap.find('eigenschapwaarde') is not None else ""
                eigenschappen[eigenschap_naam] = eigenschap_waarde

            # Voeg rij toe aan de lijst
            row = [zaak_id, zaak_nummer, zaak_type, cho_id, type_cho]
            for eigenschap_naam in eigenschappen:
                row.append(eigenschappen[eigenschap_naam])
            rows.append(row)

            # Verwijder verwerkte element om geheugen te besparen
            root.clear()

            # Print voortgangsindicator
            print(f"\r{len(rows)} regels verwerkt.", end='')

    return rows

def write_to_csv(data, output_file):
    # Schrijf gegevens naar CSV-bestand
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Schrijf koprij naar CSV-bestand
        header = ['Zaak ID', 'Zaak Nummer', 'Zaak Type', 'CHO ID', 'Type CHO', 'Type onderzoek', 'Archis veldwerk: startdatum', 'Archis veldwerk: einddatum gepland', 'Archis2onderzoeksmeldingsnummer', 'Archis2motief', 'Archis veldwerk: verwachte datum afronding rapport']
        writer.writerow(header)
        # Schrijf gegevensrijen naar CSV-bestand
        for i, row in enumerate(data, start=1):
            writer.writerow(row)

# Vraag om het invoer XML-bestand
input_file = input("Voer het pad in naar het invoer XML-bestand: ")

# Vraag om het uitvoer CSV-bestand
output_file = input("Voer het pad in naar het uitvoer CSV-bestand: ")

# Verwerk de XML-regel om gegevens te extraheren
data = extract_data(input_file)

# Schrijf de gegevens naar een CSV-bestand
write_to_csv(data, output_file)

print("\nHet XML-bestand is succesvol verwerkt en de gegevens zijn opgeslagen in het CSV-bestand.")

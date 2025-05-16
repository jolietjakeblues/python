import xml.etree.ElementTree as ET
import csv
import sys
import os.path

# Functie om voortgangsindicator af te drukken
def print_progress(current, total):
    progress = (current / total) * 100
    sys.stdout.write("\rProgress: [{:<50}] {:.2f}%".format('=' * int(progress / 2), progress))
    sys.stdout.flush()

# Functie om XML-gegevens te doorzoeken en de tekst binnen <omschrijving><tekst>...</tekst></omschrijving> te vinden
def find_description(kennisregistratienummer, root):
    for kennisregistratie in root.findall('.//kennisregistratie'):
        nummer = kennisregistratie.find('kennisregistratienummer').text
        if nummer == kennisregistratienummer:
            omschrijving = kennisregistratie.find('.//omschrijving/tekst').text
            return omschrijving
    return None

# Functie om XML-bestand te laden en te doorzoeken
def load_and_search_xml(xml_file, kennisregistratienummers):
    root = ET.parse(xml_file).getroot()
    results = []
    total = len(kennisregistratienummers)
    for i, nummer in enumerate(kennisregistratienummers):
        print_progress(i + 1, total)
        description = find_description(nummer, root)
        results.append((nummer, description))
    return results

# Functie om resultaten op te slaan in een CSV-bestand
def save_to_csv(output_file, results):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['kennisregistratienummer', 'omschrijving'])
        for row in results:
            writer.writerow(row)

# Hoofdprogramma
def main():
    # Vraag om input- en outputbestanden
    input_file = input("Geef het pad naar het CSV-bestand met kennisregistratienummers: ")
    output_file = input("Geef het pad naar het CSV-bestand waarin de resultaten moeten worden opgeslagen: ")
    xml_file = input("Geef het pad naar het XML-bestand dat moet worden doorzocht: ")

    # Controleer of het XML-bestand bestaat
    if not os.path.isfile(xml_file):
        print("XML-bestand niet gevonden.")
        return

    # Laad kennisregistratienummers uit CSV-bestand
    kennisregistratienummers = []
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            kennisregistratienummers.extend(row)

    # Laad XML-bestand en doorzoek het
    results = load_and_search_xml(xml_file, kennisregistratienummers)

    # Sla resultaten op in CSV-bestand
    save_to_csv(output_file, results)

    print("\nSuccesvolle conversie! Resultaten zijn opgeslagen in", output_file)

if __name__ == "__main__":
    main()

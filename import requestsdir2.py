import requests
from bs4 import BeautifulSoup
import csv

from bs4 import BeautifulSoup

def extract_doi(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    doi_element = soup.find('a', href=lambda href: href and href.startswith('https://doi.org/'))
    if doi_element:
        return doi_element['href']
    else:
        return None


def process_uris(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['identifier', 'relatedIdentifiers', 'DOI']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            identifier = row['identifier']
            related_identifier = row['relatedIdentifiers']
            print(f"Verwerken URI: {related_identifier}")

            try:
                response = requests.get(related_identifier)
                if response.status_code == 200:
                    doi = extract_doi(response.text)
                    if doi:
                        print(f"DOI gevonden voor URI {related_identifier}: {doi}")
                        writer.writerow({'identifier': identifier, 'relatedIdentifiers': related_identifier, 'DOI': doi})
                    else:
                        print(f"Geen DOI gevonden voor URI {related_identifier}")
                        writer.writerow({'identifier': identifier, 'relatedIdentifiers': related_identifier, 'DOI': ''})
                else:
                    print(f"Fout bij het ophalen van URI {related_identifier}: Statuscode {response.status_code}")
            except Exception as e:
                print(f"Fout bij het verwerken van URI {related_identifier}: {e}")

# Voorbeeld invoer- en uitvoerbestanden
input_file = "input.csv"
output_file = "output.csv"

# Verwerk URI's en schrijf resultaten naar uitvoerbestand
process_uris(input_file, output_file)

print("Klaar! Resultaten zijn geschreven naar", output_file)

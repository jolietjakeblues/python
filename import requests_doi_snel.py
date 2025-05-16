import requests
from bs4 import BeautifulSoup
import csv

def extract_doi_uri(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        doi_uri = None
        for link in soup.find_all('a'):
            if link.get('href') and "doi.org" in link.get('href'):
                doi_uri = link.get('href')
                break
        return doi_uri
    except Exception as e:
        print(f"Fout bij het extraheren van DOI-URI: {e}")
        return None

def process_uris(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['identifier', 'relatedIdentifiers', 'DOI-URI', 'DOI']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Schrijf de koppen van de kolommen
        writer.writeheader()

        for row in reader:
            identifier = row['identifier']
            related_identifier = row['relatedIdentifiers']
            response = requests.get(related_identifier)
            if response.status_code == 200:
                doi_uri = extract_doi_uri(response.text)
                doi = doi_uri.split('/')[-1] if doi_uri else ''
                writer.writerow({'identifier': identifier, 'relatedIdentifiers': related_identifier, 'DOI-URI': doi_uri, 'DOI': doi})
            else:
                print(f"Fout bij het ophalen van URI {related_identifier}: Statuscode {response.status_code}")

# Voorbeeld invoer- en uitvoerbestanden
input_file = "input.csv"
output_file = "output.csv"

# Verwerk URI's en schrijf resultaten naar uitvoerbestand
process_uris(input_file, output_file)

print("Klaar! Resultaten zijn geschreven naar", output_file)

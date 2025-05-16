import csv
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# Pad naar het ChromeDriver-bestand
chrome_driver_path = 'E:/pythoncursus/chromedriver.exe'

# Opties voor ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Voer Chrome uit zonder GUI

# Start de ChromeDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Functie om DOI te vinden voor een gegeven URI
def find_doi(uri):
    driver.get(uri)
    # Wacht tot de DOI wordt geladen
    try:
        doi_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'doi.org')]"))
        )
        doi = doi_element.get_attribute("href")
        return doi
    except Exception as e:
        print(f"Fout bij het vinden van DOI voor {uri}: {e}")
        return None

# Pad naar input CSV-bestand
input_csv_path = 'input.csv'
# Pad naar output CSV-bestand
output_csv_path = 'output.csv'

# Open het input CSV-bestand en lees de URI's
with open(input_csv_path, mode='r') as input_file:
    csv_reader = csv.DictReader(input_file)
    total_uris = sum(1 for row in csv_reader)
    input_file.seek(0)  # Ga terug naar het begin van het bestand
    next(csv_reader)  # Sla de headers over
    # Schrijf de headers naar het output CSV-bestand
    with open(output_csv_path, mode='w', newline='') as output_file:
        fieldnames = ['identifier', 'relatedIdentifiers', 'DOI']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        # Loop door elke rij in het input CSV-bestand
        for i, row in enumerate(csv_reader, start=1):
            uri = row['relatedIdentifiers']
            print(f"Verwerken URI: {uri}")
            doi = find_doi(uri)
            # Schrijf de resultaten naar het output CSV-bestand
            csv_writer.writerow({'identifier': row['identifier'], 'relatedIdentifiers': uri, 'DOI': doi})
            print(f"DOI gevonden voor URI {uri}: {doi}")
            # Update de voortgangsindicator
            progress = (i / total_uris) * 100
            print(f"Voortgang: {progress:.2f}%")
            print("-" * 50)

# Sluit de ChromeDriver
driver.quit()

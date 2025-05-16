from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.chrome.options import Options

def main():
    # Setup Chrome opties
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")

    # Initialiseer de WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Basis URL van de lijstpagina's
    base_url = "https://www.monumenten.nl/specialistenwijzer?size=n_12_n&sort-field=title&sort-direction=true&page={}"

    total_pages = 88  # Aantal pagina's
    bedrijf_urls = []

    try:
        # Fase 1: Verzamel alle "Bekijk bedrijf" links
        for page in range(1, total_pages + 1):
            url = base_url.format(page)
            print(f"Navigeren naar pagina {page}: {url}")
            driver.get(url)
            time.sleep(3)  # Wacht op de pagina om te laden

            # Scroll naar de onderkant om ervoor te zorgen dat alle elementen geladen zijn
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Zoek alle "Bekijk bedrijf" links op de pagina
            bedrijf_links = driver.find_elements(By.XPATH, "//a[contains(@class,'full-click-link') and contains(@href,'/specialistenwijzer/')]")
            print(f"Pagina {page}: {len(bedrijf_links)} bedrijven gevonden.")
            for link in bedrijf_links:
                bedrijf_url = link.get_attribute('href')
                if bedrijf_url:
                    bedrijf_urls.append(bedrijf_url)

            print(f"Pagina {page} volledig verwerkt. Totaal gevonden bedrijven: {len(bedrijf_urls)}")

        print(f"Totaal gevonden bedrijven: {len(bedrijf_urls)}")

        # Fase 2: Bezoek elke bedrijfsdetailpagina en haal de gewenste informatie op
        collected_data = []
        total_bedrijven = len(bedrijf_urls)
        for idx, bedrijf_url in enumerate(bedrijf_urls, start=1):
            print(f"Verwerken {idx}/{total_bedrijven}: {bedrijf_url}")
            driver.get(bedrijf_url)
            time.sleep(2)  # Wacht op de pagina om te laden

            # Scroll naar de onderkant om ervoor te zorgen dat alle elementen geladen zijn
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Haal de bedrijfsnaam op
            try:
                bedrijf_naam = driver.find_element(By.XPATH, "//h1[@class='page-title']").text.strip()
            except Exception as e:
                print(f"    Fout bij het ophalen van de bedrijfsnaam: {e}")
                bedrijf_naam = "Onbekend"

            # Haal de contactinformatie op
            try:
                adres = driver.find_element(By.CSS_SELECTOR, "div.contact-information").text.strip()
                contact_info = adres.split("\n")
                straat_adres = contact_info[0] if len(contact_info) > 0 else ''
                postcode = contact_info[1] if len(contact_info) > 1 else ''
                telefoon = next((line for line in contact_info if line.startswith('0')), '')
                email = next((line for line in contact_info if '@' in line), '')
                website = next((line for line in contact_info if line.startswith('http')), '')
                kvk = next((line for line in contact_info if 'KvK:' in line), '').replace('KvK:', '').strip()
            except Exception as e:
                print(f"    Fout bij het ophalen van contactinformatie: {e}")
                straat_adres, postcode, telefoon, email, website, kvk = "Fout bij ophalen", "", "", "", "", ""

            # Haal de specialisaties op
            try:
                specialisatie_elements = driver.find_elements(By.XPATH, "//li/a[contains(@class,'pill')]/span[@class='text']")
                specialisaties = " | ".join([spec.text.strip() for spec in specialisatie_elements])
            except Exception as e:
                print(f"    Fout bij het ophalen van specialisaties: {e}")
                specialisaties = "Geen specialisaties gevonden"

            # Voeg de verzamelde informatie toe aan de lijst
            collected_data.append([bedrijf_naam, bedrijf_url, straat_adres, postcode, telefoon, email, website, kvk, specialisaties])
            print(f"    Bedrijf: {bedrijf_naam}, Adres: {straat_adres}, Postcode: {postcode}, Tel: {telefoon}, E-mail: {email}, Website: {website}, KvK: {kvk}, Specialisaties: {specialisaties}")

            # Optioneel: voeg een kleine vertraging toe om overbelasting van de server te voorkomen
            time.sleep(1)

        # Schrijf alle verzamelde gegevens naar een CSV-bestand
        print(f"Schrijven van {len(collected_data)} bedrijfsgegevens naar CSV...")
        with open('alle_bedrijven.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Bedrijfsnaam', 'Bedrijfs-URL', 'Straat en Huisnummer', 'Postcode', 'Telefoonnummer', 'E-mail', 'Website', 'KvK', 'Specialisaties'])  # Schrijf de header
            for data in collected_data:
                writer.writerow(data)
        print("Alle bedrijfsgegevens zijn succesvol opgeslagen in alle_bedrijven.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import time

def scrape_page(page_number, output_file):
    url = f"https://archaeology.datastations.nl/dataverse/root?q=&types=dataverses%3Adatasets&page={page_number}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        dois = soup.find_all('a', href=lambda href: href and "doi.org" in href)
        dois = list(set([doi['href'].split("doi.org/")[1] for doi in dois]))
        if dois:
            print(f"DOI's gevonden op pagina {page_number}:")
            with open(output_file, 'a') as f:
                for doi in dois:
                    f.write(f"{doi}\n")
                    print(doi)
            return True
        else:
            print(f"Geen DOI's gevonden op pagina {page_number}.")
            return False
    else:
        print(f"Fout bij het openen van de pagina {page_number}. Status code: {response.status_code}.")
        return False

def main():
    start_page = 6214
    end_page = 14467
    found_dois = 0
    output_file = "gevonden_dois.txt"  # naam van het uitvoerbestand
    
    print(f"Scannen van pagina {start_page} tot pagina {end_page}...")
    for page_number in range(start_page, end_page + 1):
        if scrape_page(page_number, output_file):
            found_dois += 1
        print(f"Voortgang: {page_number}/{end_page}")
        time.sleep(1)  # Om de server niet te overbelasten
    
    print(f"Totaal aantal pagina's met DOI's gevonden: {found_dois}")
    print(f"Gevonden DOI's zijn opgeslagen in het bestand: {output_file}")

if __name__ == "__main__":
    main()

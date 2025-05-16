import requests
import rdflib
from rdflib import Graph, URIRef
from tqdm import tqdm  # Voor voortgangsindicator

# Basisinstellingen
url = "https://api.linkeddata.cultureelerfgoed.nl/queries/joop-van-der-heiden/Query-16/3/run"
graph_uri = URIRef("https://linkeddata.cultureelerfgoed.nl/graph/ruben")
output_file = "output.trig"
page_size = 10

# Initialiseer de grafiek
g = Graph()

# Functie om data op te halen en aan de grafiek toe te voegen
def fetch_data(page):
    params = {"page": page, "pageSize": page_size}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.text
        # Parse de RDF data in N-Triples formaat en voeg toe aan de gewenste grafiek
        g.parse(data=data, format="nt", publicID=graph_uri)
        return True  # Geeft aan dat er data was
    else:
        print(f"Fout bij het ophalen van pagina {page}: {response.status_code}")
        return False  # Geeft aan dat er geen data was

# Hoofdfunctie om alle pagina's op te halen en op te slaan
def main():
    page = 1
    with tqdm(desc="Data ophalen", unit="pagina") as pbar:
        while True:
            success = fetch_data(page)
            if not success:
                break  # Stop met ophalen als er geen data meer is
            page += 1
            pbar.update(1)  # Update de voortgangsbalk bij elke opgehaalde pagina
    
    # Schrijf de grafiek naar een .trig bestand
    with open(output_file, "wb") as f:
        g.serialize(destination=f, format="trig")
    
    print(f"Data succesvol opgeslagen in {output_file}")

if __name__ == "__main__":
    main()

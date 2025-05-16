import rdflib
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# Basis-URL voor monumentenquery
base_query_url = "https://kennis-staging.cultureelerfgoed.nl/index.php?title=Speciaal:Vragen&q=%5B%5BCategorie%3AMonumenten%5D%5D&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3D...-20meer-20resultaten%2Fclass%3Dsortable-20wikitable-20smwtable%2Fprefix%3Dnone&po=%3FBegrip%0A&sort=&order=asc&eq=yes&offset={offset}&limit=1000&debug=true#search"

# Basis-URL voor RDF-export
base_rdf_url = "https://kennis-staging.cultureelerfgoed.nl/index.php/Special:ExportRDF/Monumenten/"

# Functie om monumentnummers op te halen van de querypagina
def get_monument_ids():
    monument_ids = []
    offset = 0
    while True:
        query_url = base_query_url.format(offset=offset)
        response = requests.get(query_url)
        
        if response.status_code != 200:
            print(f"Fout bij het ophalen van monumentenlijst: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Zoek naar links naar monumenten in de HTML-pagina
        found_monuments = 0
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "/Monumenten/" in href:  # Zoek naar de URL-structuur van monumenten
                monument_id = href.split("/Monumenten/")[-1]
                if monument_id not in monument_ids:  # Vermijd duplicaten
                    monument_ids.append(monument_id)
                    found_monuments += 1
        
        if found_monuments == 0:
            # Stop als er geen monumenten meer worden gevonden
            break

        offset += 1000  # Verhoog de offset voor de volgende pagina met resultaten
    
    return monument_ids

# Functie om RDF-data op te halen voor elk monument
def fetch_rdf_data(monument_ids):
    graph = rdflib.ConjunctiveGraph()

    # Gebruik tqdm voor een voortgangsindicator
    for monument_id in tqdm(monument_ids, desc="Ophalen RDF-gegevens"):
        rdf_url = f"{base_rdf_url}{monument_id}"
        response = requests.get(rdf_url)

        if response.status_code == 200:
            try:
                graph.parse(data=response.content, format="xml")
                time.sleep(0.1)  # Voorkom overbelasting van de server
            except Exception as e:
                print(f"Fout bij het parsen van RDF voor monument {monument_id}: {e}")
        else:
            print(f"Fout bij het ophalen van RDF voor monument {monument_id}: {response.status_code}")

    return graph

# Hoofdscript
if __name__ == "__main__":
    print("Monumentnummers ophalen...")
    
    # Stap 1: Haal de monumentnummers op
    monument_ids = get_monument_ids()
    print(f"Aantal monumenten gevonden: {len(monument_ids)}")

    if not monument_ids:
        print("Geen monumentnummers gevonden. Script wordt beëindigd.")
    else:
        print("RDF-gegevens ophalen voor de monumenten...")
        
        # Stap 2: Haal de RDF-data op voor elk monument
        rdf_graph = fetch_rdf_data(monument_ids)

        # Stap 3: Sla de volledige RDF-graaf op in TriG-formaat
        with open("monumenten_data.trig", "w") as trig_file:
            rdf_graph.serialize(destination=trig_file, format="trig")

        print("TriG-bestand opgeslagen als 'monumenten_data.trig'")

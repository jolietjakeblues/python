import aiohttp
import asyncio
from rdflib import Graph, URIRef
from tqdm.asyncio import tqdm  # Asynchrone voortgangsindicator

# Basisinstellingen
url = "https://api.linkeddata.cultureelerfgoed.nl/queries/joop-van-der-heiden/Query-16/4/run"
graph_uri = URIRef("https://linkeddata.cultureelerfgoed.nl/graph/ruben")
output_file = "output.trig"
page_size = 500
concurrent_requests = 5  # Aantal gelijktijdige requests

# Initialiseer de grafiek
g = Graph()

# Asynchrone functie om data op te halen en aan de grafiek toe te voegen
async def fetch_data(session, page):
    params = {"page": page, "pageSize": page_size}
    async with session.get(url, params=params) as response:
        if response.status == 200:
            data = await response.text()
            # Parse de RDF data in N-Triples formaat en voeg toe aan de gewenste grafiek
            g.parse(data=data, format="nt", publicID=graph_uri)
            return True  # Geeft aan dat er data was
        else:
            print(f"Fout bij het ophalen van pagina {page}: {response.status}")
            return False  # Geeft aan dat er geen data was

# Hoofdfunctie om alle pagina's op te halen en op te slaan
async def main():
    async with aiohttp.ClientSession() as session:
        page = 1
        tasks = []
        with tqdm(desc="Data ophalen", unit="pagina") as pbar:
            while True:
                tasks = [fetch_data(session, page + i) for i in range(concurrent_requests)]
                results = await asyncio.gather(*tasks)
                if not any(results):
                    break  # Stop met ophalen als er geen data meer is
                page += concurrent_requests
                pbar.update(concurrent_requests)  # Update de voortgangsbalk bij elke batch opgehaalde pagina's
    
    # Schrijf de grafiek naar een .trig bestand
    with open(output_file, "wb") as f:
        g.serialize(destination=f, format="trig")
    
    print(f"Data succesvol opgeslagen in {output_file}")

if __name__ == "__main__":
    asyncio.run(main())

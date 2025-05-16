import pandas as pd
import requests
from rdflib import Graph
from tqdm import tqdm

# Vragen om de CSV-bestandsnaam
csv_file = input("Geef de naam van uw CSV-bestand (inclusief .csv): ")

# Vragen om de naam van het uitvoerbestand
output_file = input("Geef de naam voor het uitvoerbestand (inclusief .ttl): ")

# Lezen van de CSV
df = pd.read_csv(csv_file)

# Zorg ervoor dat de kolom met URI's juist is aangegeven
# (pas dit aan naar de juiste kolomnaam als nodig)
uri_column = "Monumenten_URI"

# Functie om RDF/XML op te halen en om te zetten naar TTL
def fetch_and_convert_rdf(uri):
    try:
        # RDF/XML ophalen
        response = requests.get(uri)
        response.raise_for_status()  # Controleer of de aanvraag succesvol was
        
        # Check of de response het juiste content-type heeft
        if 'xml' not in response.headers.get('Content-Type', ''):
            print(f"Fout: Ongeldig content-type voor {uri}")
            return None

        # RDF/XML data laden in een RDFLib Graph
        g = Graph()
        g.parse(data=response.content, format='xml')
        
        # Converteren naar Turtle (TTL)
        return g.serialize(format='turtle')  # Verwijderde .decode('utf-8')
    except Exception as e:
        print(f"Fout bij ophalen of verwerken van {uri}: {e}")
        return None

# Voortgangsindicator instellen
with open(output_file, 'w', encoding='utf-8') as ttl_output:
    # Voor elke URI in de CSV, RDF ophalen en converteren
    for uri in tqdm(df[uri_column], desc="Bezig met ophalen en converteren van RDF naar TTL"):
        ttl_data = fetch_and_convert_rdf(uri)
        
        if ttl_data:
            ttl_output.write(ttl_data)
            ttl_output.write('\n')  # Scheiding tussen datasets
        else:
            print(f"Geen data gevonden voor {uri}")

print(f"Alle RDF-data is verwerkt en opgeslagen in {output_file}")

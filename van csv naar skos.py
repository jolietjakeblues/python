import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, SKOS

# Lees het CSV-bestand
csv_file = input("Voer het CSV-bestand in: ")
df = pd.read_csv(csv_file)

# Maak een RDF-graf
g = Graph()

# Definieer namespaces
ceo = Namespace('https://linkeddata.cultureelerfgoed.nl/def/ceo#')
cht = Namespace('https://data.cultureelerfgoed.nl/term/id/cht/')
ceox = Namespace('https://linkeddata.cultureelerfgoed.nl/def/ceox#')  # Voeg je eigen namespace toe

# Loop door de rijen van het CSV-bestand
for index, row in df.iterrows():
    # Maak URI voor de Omschrijving van het Rijksmonument
    monument_uri = URIRef(row['standpunt_omschrijving'])
    g.add((monument_uri, RDF.type, ceo.Omschrijving))
    
    # Loop door de kolommen van Preflabels en URI's
    for i in range(1, 8):
        prefLabel = row[f'prefLabel {i}']
        uri = row[f'uri {i}']
        
        # Voeg SKOS:Concept en SKOS:prefLabel toe
        if not pd.isnull(prefLabel) and not pd.isnull(uri):
            concept_uri = URIRef(uri)
            g.add((concept_uri, RDF.type, SKOS.Concept))
            g.add((concept_uri, SKOS.prefLabel, Literal(prefLabel)))
            
            # Koppel het Rijksmonument aan het concept met ceox:heeftOmschrijvingOnderwerp
            g.add((monument_uri, ceox.heeftOmschrijvingOnderwerp, concept_uri))

# Sla het RDF-graf op als Turtle-bestand
turtle_file = input("Voer de naam van het Turtle-bestand in om op te slaan: ")
g.serialize(destination=turtle_file, format='turtle')

print(f"Het Turtle-RDF is opgeslagen in {turtle_file}")

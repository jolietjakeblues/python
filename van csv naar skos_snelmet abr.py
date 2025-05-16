import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, SKOS
from tqdm import tqdm

# Vraag om het CSV-bestand
csv_file_path = input("Voer het pad naar het CSV-bestand in: ")
df = pd.read_csv(csv_file_path)

# Maak een RDF-graaf
g = Graph()

# Definieer namespaces
ceo = Namespace('https://linkeddata.cultureelerfgoed.nl/def/ceo#')
ceox = Namespace('https://linkeddata.cultureelerfgoed.nl/def/ceox#')
abr = Namespace('https://data.cultureelerfgoed.nl/term/id/abr/')
cht = Namespace('https://data.cultureelerfgoed.nl/term/id/cht/')

# Bind namespaces aan de graaf voor leesbaarheid in de output
g.bind("ceo", ceo)
g.bind("ceox", ceox)
g.bind("abr", abr)
g.bind("cht", cht)

# Loop door de rijen van het CSV-bestand
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
    # Maak URI voor de Omschrijving van het Rijksmonument
    if not pd.isnull(row['heeftOmschrijving']):
        monument_uri = URIRef(row['heeftOmschrijving'])
        g.add((monument_uri, RDF.type, ceo.Omschrijving))
        
        # Loop door de kolommen om concepten toe te voegen
        for col in df.columns:
            if (col.startswith('abr') or col.startswith('cht')) and not pd.isnull(row[col]):
                value = row[col]
                
                # Controleer of de waarde een URI lijkt te zijn of een label
                if value.startswith('https'):
                    concept_uri = URIRef(value)
                    g.add((concept_uri, RDF.type, SKOS.Concept))
                    # Koppel het Rijksmonument aan het concept met ceox:heeftOmschrijvingOnderwerp
                    g.add((monument_uri, ceox.heeftOmschrijvingOnderwerp, concept_uri))
                else:
                    # Als het een label is, voeg een prefLabel toe aan het concept
                    # Zoek naar de meest recent toegevoegde concept URI om hieraan het label te koppelen
                    if 'concept_uri' in locals():
                        g.add((concept_uri, SKOS.prefLabel, Literal(value)))

# Vraag om de naam van het Turtle-bestand
turtle_file = input("Voer de naam van het Turtle-bestand in om op te slaan: ")
g.serialize(destination=turtle_file, format='turtle')

print(f"Het Turtle-RDF is opgeslagen in {turtle_file}")

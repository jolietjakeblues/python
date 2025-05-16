from rdflib import Graph, URIRef, RDF

# Functie om alle labels van een concept op te halen
def get_labels(concept_uri):
    labels = []
    for label_type in [skos.prefLabel, skos.altLabel]:
        labels.extend(g.preferredLabel(URIRef(concept_uri), label_type, lang="nl"))
    return labels

# Functie om de voortgang weer te geven
def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print()

# Vraag om invoer- en uitvoerbestanden
input_file = input("Geef het pad naar het Turtle-bestand op: ")
output_file = input("Geef het pad voor het CSV-uitvoerbestand op: ")

# Laad het Turtle-bestand
g = Graph()
g.parse(input_file, format="turtle")

# Datastructuur voor CSV
csv_data = []

# SKOS-prefixes
skos = URIRef("http://www.w3.org/2004/02/skos/core#")


# Verzamelde SKOS-eigenschappen
skos_properties_uris = [
    skos + "Collection", skos + "Concept", skos + "ConceptScheme", skos + "prefLabel",
    skos + "altLabel", skos + "hiddenLabel", skos + "notation", skos + "broader",
    skos + "narrower", skos + "related", skos + "semanticRelation", skos + "topConceptOf",
    skos + "inScheme", skos + "hasTopConcept"
]

# Itereer over de triples en vul de datastructuur in
total_triples = len(list(g.triples((None, RDF.type, skos.Concept))))
current_iteration = 0

for subject, _, object_ in g.triples((None, RDF.type, skos.Concept)):
    hierarchy = [subject]
    labels = get_labels(subject)

    # Voeg eventuele bredere concepten toe aan de hiërarchie
    for broader in g.objects(subject, skos.broader):
        hierarchy.insert(0, broader)

    # Verzamel alle eigenschappen van het concept die in de lijst staan
    pproperties = {str(prop): str(value) for prop, value in g.predicate_objects(subject) if str(prop) in skos_properties_uris}

    # Voeg regel toe aan de CSV-data
    csv_data.append({
        "Hierarchy": hierarchy,
        "Label": labels[0] if labels else "",
        "AltLabels": labels[1:] if len(labels) > 1 else [],
        "Properties": properties
    })

    # Update voortgangsindicator
    current_iteration += 1
    print_progress(current_iteration, total_triples, prefix='Voortgang:', suffix='Compleet', length=50)

# Schrijf naar CSV
import csv

csv_columns = ["Hierarchy", "Label", "AltLabels", "Properties"]
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in csv_data:
        writer.writerow(data)

print("CSV-bestand is succesvol gegenereerd op:", output_file)

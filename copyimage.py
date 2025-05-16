from rdflib import Graph, Namespace, Literal, URIRef

# Load the RDF file
rdf_file = "am_clean6.rdf"
g = Graph()
g.parse(rdf_file, format="xml")

# Define the namespaces used in the RDF file
edm = Namespace("http://www.europeana.eu/schemas/edm/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

# Iterate through each ProvidedCHO element and modify it
for provided_cho in g.subjects(predicate=URIRef(edm.type), object=Literal("IMAGE")):
    depictions = list(g.objects(subject=provided_cho, predicate=foaf.depiction))
    if depictions:
        # Remove the old depiction elements
        for depiction in depictions:
            g.remove((provided_cho, foaf.depiction, depiction))
        # Add the new depiction element under the edm:type element
        g.add((provided_cho, edm.type, Literal("IMAGE")))
        for depiction in depictions:
            g.add((provided_cho, edm.type, Literal(depiction)))

# Save the modified RDF to a new file
modified_rdf_file = "am_clean6_modified.rdf"
g.serialize(destination=modified_rdf_file, format="xml")

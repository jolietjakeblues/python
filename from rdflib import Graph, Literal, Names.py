from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DC, DCTERMS, RDF, SKOS

# Create the RDF graph
g = Graph()

# Define namespaces
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
nave = Namespace("http://schemas.delving.eu/nave/terms/")
ore = Namespace("http://www.openarchives.org/ore/terms/")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

# Bind the prefixes to the graph
g.bind("dc", dc)
g.bind("dcterms", dcterms)
g.bind("edm", edm)
g.bind("nave", nave)
g.bind("ore", ore)
g.bind("skos", skos)
g.bind("foaf", foaf)

# Define the RDF triples
aggregation_uri = URIRef("http://data.collectienederland.nl/resource/aggregation/zuiderzeemuseum/007140")
cho_uri = URIRef("http://data.collectienederland.nl/resource/document/zuiderzeemuseum/007140")
web_resource_uri = URIRef("http://images.memorix.nl/zzm/download/fullsize/b34f22e8-e714-f4d8-9321-fcd58b189174")

g.add((aggregation_uri, RDF.type, ore.Aggregation))
g.add((aggregation_uri, edm.aggregatedCHO, cho_uri))
g.add((aggregation_uri, edm.dataProvider, Literal("Zuiderzeemuseum")))
g.add((aggregation_uri, edm.isShownAt, URIRef("http://hdl.handle.net/21.12111/zzm-collect-2")))
g.add((aggregation_uri, edm.isShownBy, web_resource_uri))
g.add((aggregation_uri, edm.object, web_resource_uri))
g.add((aggregation_uri, edm.provider, Literal("Rijksdienst voor het Cultureel Erfgoed")))
g.add((aggregation_uri, edm.rights, URIRef("http://creativecommons.org/licenses/by-sa/4.0/")))

g.add((cho_uri, RDF.type, edm.ProvidedCHO))
g.add((cho_uri, dc.coverage, Literal("Marken")))
g.add((cho_uri, dc.description, Literal("Bauw voor een vrouw")))
g.add((cho_uri, dc.identifier, Literal("007140")))
g.add((cho_uri, dc.subject, Literal("Zuiderzee")))
g.add((cho_uri, dc.title, Literal("Bauw")))
g.add((cho_uri, dcterms.created, Literal("1800 - 1900")))
g.add((cho_uri, dcterms.extent, Literal("hoogte 30.0 cm, breedte 23.0 cm")))
g.add((cho_uri, dcterms.provenance, Literal("aankoop, Huidige eigenaar: Rijkscollectie")))
g.add((cho_uri, dcterms.spatial, Literal("Marken")))
g.add((cho_uri, dcterms.tableOfContents, Literal("2")))
g.add((cho_uri, foaf.depiction, web_resource_uri))
g.add((cho_uri, dcterms.subject, Literal("katoen, baaf, bauw")))
g.add((cho_uri, edm.type, Literal("IMAGE")))

g.add((web_resource_uri, RDF.type, edm.WebResource))
g.add((web_resource_uri, dc.creator, Literal("Zandbergen, Wim")))
g.add((web_resource_uri, nave.thumbSmall, web_resource_uri))
g.add((web_resource_uri, nave.thumbMedium, web_resource_uri))
g.add((web_resource_uri, nave.thumbLarge, web_resource_uri))
g.add((web_resource_uri, nave.allowDeepZoom, Literal("true")))
g.add((web_resource_uri, nave.allowSourceDownload, Literal("true")))
g.add((web_resource_uri, nave.allowPublicWebView, Literal("true")))

# Serialize the new graph to the Turtle format
# Serialize the graph to RDF Turtle format
rdf_output = g.serialize(format="turtle")

# Write the RDF output to a file named "output.ttl"
with open("output.ttl", "wb") as file:
    file.write(rdf_output)

print("RDF data has been written to output.ttl")
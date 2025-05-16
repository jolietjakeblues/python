import json
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, DCTERMS
import uuid

DEP = Namespace("https://linkeddata.cultureelerfgoed.nl/erfgeo/departementen/id/")
HG = Namespace("https://rdf.histograph.io/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")

g = Graph()
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("dcterms", DCTERMS)
g.bind("hg", HG)
g.bind("geo", GEO)

filename = "Dep1812.geojson.txt"

with open(filename, encoding="utf-8") as f:
    data = json.load(f)

for feature in data["features"]:
    properties = feature["properties"]
    geometry = feature["geometry"]
    dep_id = properties["amco-depar"]
    identifier = "dcterms:" + dep_id
    uri = URIRef(DEP + str(uuid.uuid4()))
    g.add((uri, RDF.type, HG.PlaceInTime))
    g.add((uri, DCTERMS.identifier, Literal(dep_id)))
    g.add((uri, DCTERMS.title, Literal(properties["naam_Naam"])))
    g.add((uri, DCTERMS.alternative, Literal(properties["naam_Naa_1"])))
    g.add((uri, DCTERMS.URI, Literal(properties["uri"])))
    wkt = "MULTIPOLYGON(" + str(geometry["coordinates"]) + ")"
    g.add((uri, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

g.serialize(destination="departementen.ttl", format="turtle")

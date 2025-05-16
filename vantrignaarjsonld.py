from rdflib import Graph
import json

# Load the TriG file into an RDFlib graph
g = Graph()
g.parse("E:\pythoncursus\pp_project_cultuurhistorischethesaurus.trig", format="trig")

# Serialize the graph as JSON-LD
jsonld_data = g.serialize(format="json-ld", indent=4)

# Save the JSON-LD data to a file or use it as needed
with open("E:\pythoncursus\pp_project_cultuurhistorischethesaurus.jsonld", "w") as jsonld_file:
    json.dump(jsonld_data, jsonld_file, indent=4)

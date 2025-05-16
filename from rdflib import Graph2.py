from rdflib import Graph

g = Graph()
g.parse("zzm_48.rdf")

# Print alle triples in de graph
for subj, pred, obj in g:
    print(subj, pred, obj)

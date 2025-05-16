from rdflib import Graph, Namespace, RDF, RDFS, Literal
from rdflib.namespace import DCTERMS

# Define namespaces
SCHEMA = Namespace('http://schema.org/')
MYONTO = Namespace('http://example.com/ontology#')

# Create an RDF graph
g = Graph()

# Define metadata for the graph
g.bind('schema', SCHEMA)
g.bind('myonto', MYONTO)
g.bind('dcterms', DCTERMS)

# Define resources
book = MYONTO['book/1']
author = MYONTO['author/1']
publisher = MYONTO['publisher/1']

# Add triples to the graph
g.add((book, RDF.type, SCHEMA['Book']))
g.add((book, SCHEMA.name, Literal('My Book')))
g.add((book, SCHEMA.datePublished, Literal('2023-03-02')))
g.add((book, SCHEMA.author, author))
g.add((book, SCHEMA.publisher, publisher))

g.add((author, RDF.type, SCHEMA['Person']))
g.add((author, SCHEMA.name, Literal('John Smith')))
g.add((author, DCTERMS.identifier, Literal('0000-0000-0000-0001')))

g.add((publisher, RDF.type, SCHEMA['Organization']))
g.add((publisher, SCHEMA.name, Literal('My Publisher')))
g.add((publisher, SCHEMA.location, Literal('My City')))

# Serialize the RDF graph in Turtle format and write to file
with open('test_jvand.ttl', 'wb') as f:
    f.write(g.serialize(format='turtle'))

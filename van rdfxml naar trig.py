import rdflib

def convert_rdf_to_trig(input_file, output_file, graph_name):
    graph_uri = f"https://linkeddata.cultureelerfgoed.nl/graph/{graph_name}"

    # Load the RDF data
    graph = rdflib.Graph()
    graph.parse(input_file, format="xml")

    # Create a new Trig graph
    trig_graph = rdflib.Graph(identifier=rdflib.URIRef(graph_uri))
    trig_graph.bind("rdf", rdflib.RDF)
    trig_graph.bind("dc", rdflib.URIRef("http://purl.org/dc/elements/1.1/"))
    trig_graph.bind("dcterms", rdflib.URIRef("http://purl.org/dc/terms/"))
    trig_graph.bind("edm", rdflib.URIRef("http://www.europeana.eu/schemas/edm/"))
    trig_graph.bind("foaf", rdflib.URIRef("http://xmlns.com/foaf/0.1/"))
    trig_graph.bind("nave", rdflib.URIRef("http://schemas.delving.eu/nave/terms/"))
    trig_graph.bind("ore", rdflib.URIRef("http://www.openarchives.org/ore/terms/"))
    trig_graph.bind("graph", rdflib.URIRef("https://linkeddata.cultureelerfgoed.nl/graph/"))
    trig_graph.bind("skos", rdflib.URIRef("http://www.w3.org/2004/02/skos/core#"))
    trig_graph.bind("wgs84_pos", rdflib.URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#"))

    total_triples = len(graph)
    progress = 0

    # Add the RDF data to the Trig graph
    for triple in graph:
        trig_graph.add(triple)

        # Update the progress counter
        progress += 1
        print(f"Progress: {progress}/{total_triples}", end="\r")

    print("\nConversion complete!")

    # Serialize the Trig graph to the output file
    trig_graph.serialize(destination=output_file, format="trig")

if __name__ == "__main__":
    input_file = input("Enter the input RDF filename: ")
    output_file = input("Enter the output Trig filename: ")
    graph_name = input("Enter the graph name: ")

    convert_rdf_to_trig(input_file, output_file, graph_name)

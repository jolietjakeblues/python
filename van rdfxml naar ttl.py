from rdflib import Graph, ConjunctiveGraph, URIRef, Namespace

NAVE = Namespace("http://schemas.delving.eu/nave/terms/")
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
ORE = Namespace("http://www.openarchives.org/ore/terms/")

def convert_rdfxml_to_trig(input_file, output_file, graph_name):
    # Create an RDF graph and parse the input RDF/XML file
    graph = Graph()
    graph.parse(input_file, format='xml')

    # Bind your desired prefixes to the namespaces
    graph.bind('nave', NAVE)
    graph.bind('edm', EDM)
    graph.bind('ore', ORE)

    # Create a conjunctive graph (which can hold multiple named graphs)
    conj_graph = ConjunctiveGraph()

    # Add the parsed graph to the conjunctive graph with the provided graph name (URI)
    total_triples = len(graph)
    for count, (s, p, o) in enumerate(graph, start=1):
        conj_graph.add((s, p, o, URIRef(graph_name)))
        print(f"Processed {count}/{total_triples} triples", end='\r')

    # Serialize the conjunctive graph to Trig and save it to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(conj_graph.serialize(format='trig'))

    print(f"\nConversion completed! Saved to {output_file}")

if __name__ == '__main__':
    # Prompt the user for input and output file paths
    input_rdfxml_file = input("Please enter the path to your RDF/XML file: ")
    output_file = input("Please enter the desired output file path: ")

    # Prompt the user for the named graph URI
    graph_name = input("Please enter the URI for the named graph: ")

    # Convert the input file to Trig format with the provided graph name
    convert_rdfxml_to_trig(input_rdfxml_file, output_file, graph_name)

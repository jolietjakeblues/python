from rdflib import Graph

def convert_rdfxml_to_ttl(input_file, output_file):
    # Create an RDF graph and parse the input RDF/XML file
    graph = Graph()
    graph.parse(input_file, format='xml')

    # Serialize the graph to Turtle and save it to the output TTL file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(graph.serialize(format='turtle'))

if __name__ == '__main__':
    input_rdfxml_file = 'am_clean6.rdf'   # Replace with the path to your RDF/XML file
    output_ttl_file = 'am_output6.ttl'    # Replace with the desired output TTL file path

    convert_rdfxml_to_ttl(input_rdfxml_file, output_ttl_file)

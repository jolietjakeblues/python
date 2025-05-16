from rdflib import Graph

def convert_nt_to_turtle(input_file, output_file):
    # Create an RDF graph
    g = Graph()

    # Parse the input file with N-Triples data
    g.parse(input_file, format="nt")

    # Serialize the graph to Turtle and write to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(g.serialize(format="turtle"))

# Voer de functie uit met de input en output bestandsnamen
input_file = "E:\werk\oudeomschrijvingen.nt"
output_file = "E:\werk\oudeomschrijvingen.ttl"
convert_nt_to_turtle(input_file, output_file)

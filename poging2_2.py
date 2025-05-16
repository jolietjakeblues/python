def process_rdf_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as input_file:
        rdf_data = input_file.readlines()

    data_tag = '<edm:aggregatedCHO rdf:resource="http://data.collectienederland.nl/resource/document/'
    data_end_tag = '"/>'

    processed_data = []

    new_line = None
    in_rdf_block = False
    last_metadata_value = None

    for line in rdf_data:
        if data_tag in line:
            data_start_pos = line.find(data_tag)
            data_end_pos = line.find(data_end_tag, data_start_pos)

            if data_start_pos != -1 and data_end_pos != -1:
                data_value = line[data_start_pos + len(data_tag):data_end_pos]
                new_line = line.replace(data_tag + data_value + data_end_tag,
                                         '<edm:Metadata rdf:resource="http://data.collectienederland.nl/resource/subject/' + data_value + '"/>')
                last_metadata_value = new_line

                # Create a copy of the <edm:aggregatedCHO> and include it in <ore:Aggregation> block
                agg_cho_copy = '<edm:aggregatedCHO rdf:resource="http://data.collectienederland.nl/resource/document/' + data_value + '"/>'
                processed_data.append(agg_cho_copy)

        else:
            processed_data.append(line)

        if '<rdf:RDF' in line:
            in_rdf_block = True

        if in_rdf_block and ('<edm:ProvidedCHO' in line or '<ceox:ff' in line):
            if last_metadata_value is not None:
                processed_data.append(last_metadata_value)

        if '</rdf:RDF>' in line:
            in_rdf_block = False

    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.writelines(processed_data)


if __name__ == "__main__":
    input_filename = input("Geef de naam van het invoerbestand (RDF/XML-bestand): ")
    output_filename = input("Geef de naam van het uitvoerbestand: ")
    process_rdf_file(input_filename, output_filename)
    print("Het verwerken is voltooid. Het gewijzigde bestand is opgeslagen als", output_filename)

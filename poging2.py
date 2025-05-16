def process_rdf_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as input_file:
        rdf_data = input_file.readlines()

    data_tag = '<edm:aggregatedCHO rdf:resource="http://data.collectienederland.nl/resource/document/'
    data_end_tag = '"/>'

    processed_data = []

    for line in rdf_data:
        if data_tag in line:
            data_start_pos = line.find(data_tag)
            data_end_pos = line.find(data_end_tag, data_start_pos)

            if data_start_pos != -1 and data_end_pos != -1:
                data_value = line[data_start_pos + len(data_tag):data_end_pos]
                new_line = line.replace(data_tag + data_value + data_end_tag,
                                         '<ceox:Metadata rdf:resource="http://data.collectienederland.nl/resource/subject/' + data_value + '"/>')
                processed_data.append(line)
                processed_data.append(new_line)
        else:
            processed_data.append(line)

    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.writelines(processed_data)


if __name__ == "__main__":
    input_filename = input("Geef de naam van het invoerbestand (RDF/XML-bestand): ")
    output_filename = input("Geef de naam van het uitvoerbestand: ")
    process_rdf_file(input_filename, output_filename)
    print("Het verwerken is voltooid. Het gewijzigde bestand is opgeslagen als", output_filename)

import re

def process_file(input_filename, output_filename):
    rdf_start_pattern = '<rdf:RDF xmlns:dc="http://purl.org/dc/elements/1.1/"'
    rdf_end_pattern = '</rdf:RDF>'
    metadata_rdf_end_pattern = '</ceox:Metadata></rdf:RDF>'
    metadata_pattern = '</ceox:Metadata>'
    comment_pattern = '<!--<http://data.collectienederland.nl/resource/aggregation/'
    web_resource_pattern = '<edm:WebResource rdf:about="'
    ceox_ff_pattern = '<ceox:ff>'
    ceox_ff_end_pattern = '</ceox:ff>'
    modified_start_line = '<rdf:RDF xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:edm="http://www.europeana.eu/schemas/edm/" xmlns:nave="http://schemas.delving.eu/nave/terms/" xmlns:ore="http://www.openarchives.org/ore/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:skos="http://www.w3.org/2004/02/skos/core#" xmlns:wgs84_pos="http://www.w3.org/2003/01/geo/wgs84_pos#">'

    total_lines = sum(1 for _ in open(input_filename, 'r', encoding='utf-8'))
    processed_lines = 0

    output_lines = []
    last_line = None

    with open(input_filename, 'r', encoding='utf-8') as f:
        for line in f:
            processed_lines += 1
            progress = (processed_lines / total_lines) * 100
            print(f"\rProgress: {progress:.2f}%", end="")

            line = line.rstrip()  # Remove trailing whitespaces

            # Check if the line is the last line of the document
            is_last_line = processed_lines == total_lines

            # Skip comment lines
            if line.startswith(comment_pattern):
                continue

            # Remove <ceox:ff> and </ceox:ff> from the line
            line = line.replace(ceox_ff_pattern, '').replace(ceox_ff_end_pattern, '')
            line = line.replace(metadata_rdf_end_pattern, metadata_pattern)

            if line.startswith(rdf_start_pattern) and processed_lines == 1:
                output_lines.append(modified_start_line)
                continue
            elif line.startswith(rdf_start_pattern):
                continue
            elif is_last_line and line.strip() == rdf_end_pattern:
                continue  # Skip the last </rdf:RDF> entirely
            elif web_resource_pattern in line:
                url = re.search(r'rdf:about="(.*?)"', line).group(1)
                modified_line = f'<foaf:depiction>{url}</foaf:depiction>'
                output_lines.extend([line, modified_line])
            else:
                output_lines.append(line)

    # ... (vervolg van de code blijft hetzelfde)

    # Append only one rdf_end_pattern at the end if it's missing
    if not is_last_line or output_lines[-1].strip() != rdf_end_pattern:
        output_lines.append(rdf_end_pattern)

    # Remove consecutive empty lines
    filtered_output = [line + '\n' for index, line in enumerate(output_lines) if line != '' or (index + 1 < len(output_lines) and output_lines[index + 1] != '')]

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.writelines(filtered_output)

    print("\nProcessing completed!")

if __name__ == "__main__":
    input_filename = input("Enter the input filename: ")
    output_filename = input("Enter the output filename: ")
    process_file(input_filename, output_filename)

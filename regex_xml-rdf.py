import re

def transform_data(input_file, output_file):
    # Lees de input data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()

    # Stap 1: <ceox:heeftMetadata rdf:resource toevoegen aan de <ore:Aggregation rdf:about
    aggregated_cho_values = re.findall('<edm:aggregatedCHO rdf:resource="([^"]+)"/>', data)
    for cho_value in aggregated_cho_values:
        new_value = cho_value.replace('document', 'subject')
        heeft_metadata_element = f'<ceox:heeftMetadata rdf:resource="{new_value}"/>'
        data = data.replace('<edm:aggregatedCHO rdf:resource="' + cho_value + '"/>', heeft_metadata_element + '\n' + '<edm:aggregatedCHO rdf:resource="' + cho_value + '"/>')

    # Stap 2: <foaf:depiction> toevoegen aan de <edm: ProvidedCHO
    is_shown_by_values = re.findall('<edm:isShownBy rdf:resource="([^"]+)"/>', data)
    for shown_by_value in is_shown_by_values:
        depiction_element = f'<foaf:depiction rdf:resource="{shown_by_value}"/>'
        data = re.sub(r'(<edm:ProvidedCHO[^>]*>)', r'\1\n' + depiction_element, data)

    # Stap 3: <ceox:Metadata rdf:about genereren
    metadata_block = '<ceox:Metadata rdf:about="DUMMY_VALUE">\n'
    skos_pref_labels = re.findall('<skos:prefLabel>([^<]+)</skos:prefLabel>', data)
    for label in skos_pref_labels:
        metadata_block += f'<skos:prefLabel>{label}</skos:prefLabel>\n'

    nave_values = re.findall('<nave:([^>]+)>([^<]+)</nave:\w+>', data)
    for tag, value in nave_values:
        metadata_block += f'<nave:{tag}>{value}</nave:{tag}>\n'

    metadata_block += '</ceox:Metadata>'
    # Voeg de metadata_block toe aan het einde van de data
    data += '\n' + metadata_block

    # Verwijder de inhoud tussen </edm:WebResource> en <ceox:Metadata rdf:about=
    data = re.sub('</edm:WebResource>.*?<ceox:Metadata rdf:about=', '</edm:WebResource>\n<ceox:Metadata rdf:about=', data, flags=re.DOTALL)

    # Schrijf de getransformeerde data naar het uitvoerbestand
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data)

if __name__ == '__main__':
    input_file = input("Geef het pad van het invoerbestand op: ").strip()
    output_file = input("Geef de naam van het uitvoerbestand op: ").strip()
    transform_data(input_file, output_file)

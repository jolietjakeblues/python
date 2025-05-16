
import re

def transform_txt(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # 1. Voeg <ceox:heeftMetadata rdf:resource="..." /> alleen toe aan <ore:Aggregation rdf:about...
    ore_aggregations = re.findall(r'(<ore:Aggregation rdf:about.*?<edm:aggregatedCHO rdf:resource="(.*?document.*?)").*?</ore:Aggregation>', content, flags=re.DOTALL)
    for full_match, cho_value in ore_aggregations:
        new_value = cho_value.replace('document', 'subject')
        content = content.replace(full_match, full_match + f'\n<ceox:heeftMetadata rdf:resource="{new_value}" />')

    # 2. Voeg <foaf:depiction> toe aan <edm:ProvidedCHO> gebaseerd op de waarde van <edm:isShownBy rdf:resource...> binnen <ore:Aggregation rdf:about...
    aggregations = re.findall(r'(<ore:Aggregation rdf:about.*?</ore:Aggregation>)', content, flags=re.DOTALL)
    for agg in aggregations:
        depiction_link = re.search(r'<edm:isShownBy rdf:resource="(.*?)"', agg).group(1)
        cho_about = re.search(r'<edm:aggregatedCHO rdf:resource="(.*?)"', agg).group(1)
        cho_pattern = rf'(<edm:ProvidedCHO rdf:about="{re.escape(cho_about)}".*?>)'
        content = re.sub(cho_pattern, rf'\1\n<foaf:depiction>{depiction_link}</foaf:depiction>', content, 1, flags=re.DOTALL)

    # 3. Genereer <ceox:Metadata rdf:about> met de gegevens tussen <ceox:ff> en </ceox:ff>.
    old_model_data_matches = re.findall(r'<ceox:ff>(.*?)</ceox:ff>', content, flags=re.DOTALL)
    ore_aggregation_matches = re.findall(r'<ore:Aggregation rdf:about.*?<ceox:heeftMetadata rdf:resource="(.*?)".*?</ore:Aggregation>', content, flags=re.DOTALL)

    for index, match in enumerate(old_model_data_matches):
        if index < len(ore_aggregation_matches):  # Om te zorgen dat we niet buiten de lijst indexeren
            metadata_resource = ore_aggregation_matches[index]
            new_metadata = f'<ceox:Metadata rdf:about="{metadata_resource}">' + match + '</ceox:Metadata>'
            content = content.replace(f'<ceox:ff>{match}</ceox:ff>', new_metadata, 1)

    # 4. Verwijder inhoud tussen </edm:WebResource> en <ceox:Metadata rdf:about=
    content = re.sub(r'</edm:WebResource>.*?<ceox:Metadata rdf:about=', '<ceox:Metadata rdf:about=', content, flags=re.DOTALL)

    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(content)

input_file = input("Geef de naam van het invoerbestand: ")
output_file = input("Geef de naam van het uitvoerbestand: ")

transform_txt(input_file, output_file)
print(f"Transformatie voltooid. Gegevens opgeslagen in {output_file}.")

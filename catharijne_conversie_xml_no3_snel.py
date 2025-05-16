import re
from tqdm import tqdm

# Vraag de gebruiker om de naam van het inputbestand
input_file_name = input("Voer de naam van het inputbestand in: ")

# Vraag de gebruiker om de naam van het outputbestand
output_file_name = input("Voer de naam van het outputbestand in: ")

# Lees het RDF/XML-bestand
with open(input_file_name, 'r', encoding='utf-8') as file:
    rdf_content = file.read()

# Split the rdf_content using the object blocks as delimiters
split_content = re.split(r'(<sys:Object>.*?</sys:Object>)', rdf_content, flags=re.DOTALL)

modified_content = []

# Lus door de gesplitste inhoud
for segment in tqdm(split_content, desc="Verwerken", unit="blok"):
    # Check if the segment is one of our object blocks
    if segment.startswith('<sys:Object>'):
        # Find the last occurrence of </edm:Place> within the segment
        last_skos_concept_index = segment.rfind('</edm:Place>')

        if last_skos_concept_index != -1:
            # Replace the last </edm:Place> tag with </edm:Place>\n</edm:ProvidedCHO>
            segment = segment[:last_skos_concept_index] + '</edm:Place>' + '\n' + '</edm:ProvidedCHO>' + segment[last_skos_concept_index+len('</edm:Place>'):]

    # Append the (possibly modified) segment to our list
    modified_content.append(segment)

# Join the modified segments to form the complete modified content
rdf_content_modified = ''.join(modified_content)

print("\nConversie voltooid!")

# Schrijf het aangepaste XML-bestand
with open(output_file_name, 'w', encoding='utf-8') as file:
    file.write(rdf_content_modified)

print(f"De aangepaste inhoud is opgeslagen in: {output_file_name}")

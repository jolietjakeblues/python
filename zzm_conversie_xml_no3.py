import re

# Vraag de gebruiker om de naam van het inputbestand
input_file_name = input("Voer de naam van het inputbestand in: ")

# Vraag de gebruiker om de naam van het outputbestand
output_file_name = input("Voer de naam van het outputbestand in: ")

# Lees het RDF/XML-bestand
with open(input_file_name, 'r', encoding='utf-8') as file:
    rdf_content = file.read()

# Zoek naar alle voorkomens van <sys:Object>...</sys:Object> blokken
object_blocks = re.findall(r'<sys:Object>.*?</sys:Object>', rdf_content, re.DOTALL)

total_blocks = len(object_blocks)
print(f"Totaal aantal <sys:Object> blokken gevonden: {total_blocks}")

# Lus door de gevonden blokken
for index, object_block in enumerate(object_blocks, 1):
    # Zoek de laatste </skos:Concept> tag binnen elk object_block
    last_skos_concept_index = object_block.rfind('</skos:Concept>')

    if last_skos_concept_index != -1:
        # Vervang de laatste </skos:Concept> tag door </skos:Concept></dcterms:subject>
        modified_block = object_block[:last_skos_concept_index] + '</skos:Concept>' + '\n' + '</edm:ProvidedCHO>' + object_block[last_skos_concept_index+len('</skos:Concept>'):]

        # Vervang het oorspronkelijke object_block door het gewijzigde object_block in rdf_content
        rdf_content = rdf_content.replace(object_block, modified_block)

    # Print voortgangsindicator
    print(f"Verwerkt: {index}/{total_blocks} blokken", end='\r')

print("\nConversie voltooid!")

# Schrijf het aangepaste XML-bestand
with open(output_file_name, 'w', encoding='utf-8') as file:
    file.write(rdf_content)

print(f"De aangepaste inhoud is opgeslagen in: {output_file_name}")

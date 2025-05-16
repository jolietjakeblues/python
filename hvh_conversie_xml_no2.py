import re
from tqdm import tqdm

# Vraag de gebruiker om de naam van het inputbestand
input_filename = input("Voer de naam van het inputbestand in (bijv. 'zuiderzeemuseum.rdf'): ")

# Vraag de gebruiker om de naam van het outputbestand
output_filename = input("Voer de naam van het outputbestand in (bijv. 'zzm_aangepast_stap2_xml.rdf'): ")

# Lees het RDF/XML-bestand
with open(input_filename, 'r', encoding='utf-8') as file:
    rdf_content = file.read()

# Zoek naar alle voorkomens van <skos:Concept>...</skos:Concept> blokken
concept_blocks = re.findall(r'<sys:Object>.*?</sys:Object>', rdf_content, re.DOTALL)

# Lus door de gevonden blokken met tqdm voor voortgangsindicatie
for concept_block in tqdm(concept_blocks, desc="Verwerking blokken", unit="blok"):
    # Zoek de inhoud tussen <dc:identifier>...</dc:identifier> binnen elk concept_block
    identifier_match = re.search(r'<dc:identifier>(.*?)</dc:identifier>', concept_block, re.DOTALL)

    if identifier_match:
        identifier_value = identifier_match.group(1)  # Haal de waarde tussen de tags
        new_tag = f'<edm:ProvidedCHO rdf:about="http://data.collectienederland.nl/resource/document/huis-van-hilde/{identifier_value}">'  # Maak de nieuwe tag

        # Voeg de nieuwe tag toe aan het concept_block
        modified_block = concept_block.replace('<edm:Place>', new_tag + "\n" + '<edm:Place>', 1)

        # Vervang het oorspronkelijke concept_block door het gewijzigde concept_block in rdf_content
        rdf_content = rdf_content.replace(concept_block, modified_block)

# Schrijf het aangepaste XML-bestand
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(rdf_content)

print("Conversie voltooid!")

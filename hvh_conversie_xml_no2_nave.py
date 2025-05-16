import re
from tqdm import tqdm

# Vraag de gebruiker om de naam van het inputbestand
input_filename = input("Voer de naam van het inputbestand in (bijv. 'zuiderzeemuseum.rdf'): ")

# Vraag de gebruiker om de naam van het outputbestand
output_filename = input("Voer de naam van het outputbestand in (bijv. 'zzm_aangepast_stap2_xml.rdf'): ")

# Regex patronen vooraf compileren voor betere prestaties
block_start_pattern = re.compile(r'<sys:Object>')
block_end_pattern = re.compile(r'</sys:Object>')
identifier_pattern = re.compile(r'<dc:identifier>(.*?)</dc:identifier>', re.DOTALL)

# Open het invoer- en uitvoerbestand tegelijkertijd
with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
    inside_block = False
    block_content = []

    for line in tqdm(infile, desc="Verwerking blokken"):
        if block_start_pattern.search(line):
            inside_block = True
        
        if inside_block:
            block_content.append(line)
        
        if block_end_pattern.search(line):
            inside_block = False
            block_string = ''.join(block_content)
            
            # Zoek de inhoud tussen <dc:identifier>...</dc:identifier> binnen elk concept_block
            identifier_match = identifier_pattern.search(block_string)
            if identifier_match:
                identifier_value = identifier_match.group(1)
                new_tag = f'<edm:ProvidedCHO rdf:about="http://data.collectienederland.nl/resource/document/huis-van-hilde/{identifier_value}">'
                block_string = block_string.replace('<nave:DcnResource>', new_tag + "\n" + '<nave:DcnResource>', 1)
            
            outfile.write(block_string)
            block_content = []
        elif not inside_block:
            outfile.write(line)

print("Conversie voltooid!")

import re
from tqdm import tqdm

# Vraag de gebruiker om de naam van het inputbestand
input_file_name = input("Voer de naam van het inputbestand in: ")

# Vraag de gebruiker om de naam van het outputbestand
output_file_name = input("Voer de naam van het outputbestand in: ")

# Regex patroon vooraf compileren voor betere prestaties
object_start_pattern = re.compile(r'<sys:Object>')
object_end_pattern = re.compile(r'</sys:Object>')

# Open het invoer- en uitvoerbestand tegelijkertijd
with open(input_file_name, 'r', encoding='utf-8') as infile, open(output_file_name, 'w', encoding='utf-8') as outfile:
    inside_object = False
    object_content = []

    for line in tqdm(infile, desc="Verwerken"):
        if object_start_pattern.search(line):
            inside_object = True
        
        if inside_object:
            object_content.append(line)
        
        if object_end_pattern.search(line):
            inside_object = False
            object_string = ''.join(object_content)
            
            # Zoek de laatste </skos:Concept> tag binnen elk object_block
            last_skos_concept_index = object_string.rfind('</nave:DcnResource>')

            if last_skos_concept_index != -1:
                # Vervang de laatste </skos:Concept> tag door </skos:Concept></dcterms:subject>
                object_string = object_string[:last_skos_concept_index] + '</nave:DcnResource>' + '\n' + '</edm:ProvidedCHO>' + object_string[last_skos_concept_index+len('</skos:Concept>'):]

            outfile.write(object_string)
            object_content = []
        elif not inside_object:
            outfile.write(line)

print(f"De aangepaste inhoud is opgeslagen in: {output_file_name}")

import re
from tqdm import tqdm

# Vraag om de naam van het invoerbestand
input_filename = input("Voer de naam van het invoerbestand in: ")

# Vraag om de naam van het uitvoerbestand
output_filename = input("Voer de naam van het uitvoerbestand in: ")

# Lees het RDF/XML-bestand
with open(input_filename, 'r', encoding='utf-8') as file:
    rdf_content = file.read()

# Definieer de begintag die je wilt toevoegen
new_begintag = "<sys:Object>"

# Zoek naar de begintag waar je na wilt toevoegen
target_begintag = "</ore:Aggregation>"

print("Voeg begintags toe...")
# Vervang de target_begintag met de target_begintag gevolgd door de nieuwe begintag
modified_content_begin = re.sub(target_begintag, lambda x: x.group(0) + "\n" + new_begintag, rdf_content)

# Definieer de endtag die je wilt toevoegen
new_endtag = "</sys:Object>"

# Zoek naar de endtag waar je na wilt toevoegen
target_endtag = "</nave:DelvingResource>"

print("Voeg eindtags toe...")
# Vervang de target_endtag met de target_endtag gevolgd door de nieuwe endtag
modified_content_end = modified_content_begin.replace(target_endtag, target_endtag + "\n" + new_endtag)

# Schrijf het aangepaste XML-bestand
with open(output_filename, 'w', encoding='utf-8') as file:
    for line in tqdm(modified_content_end.splitlines()):
        file.write(line + "\n")

print("Bestand is met succes aangepast!")

#oude versie van Patrick

# Eerste conversie toevoegen tags <sys:Object> en </sys:Object>
#import re

# Lees het RDF/XML-bestand
#with open('zuiderzeemuseum.rdf', 'r', encoding='utf-8') as file:
#    rdf_content = file.read()

# Definieer de begintag die je wilt toevoegen
#new_begintag = "<sys:Object>"

# Zoek naar de begintag waar je na wilt toevoegen
#target_begintag = "</ore:Aggregation>"

# Vervang de target_begintag met de target_begintag gevolgd door de nieuwe begintag
#modified_content_begin = re.sub(target_begintag, lambda x: x.group(0) + "\n" + new_begintag, rdf_content)

# Definieer de endtag die je wilt toevoegen
#new_endtag = "</sys:Object>"

# Zoek naar de endtag waar je na wilt toevoegen
#target_endtag = "</nave:DelvingResource>"

# Vervang de target_endtag met de target_endtag gevolgd door de nieuwe endtag
#modified_content_end = modified_content_begin.replace(target_endtag, target_endtag + "\n" + new_endtag)

# Schrijf het aangepaste XML-bestand
#with open('zzm_aangepast_stap1_xml.rdf', 'w', encoding='utf-8') as file:
#    file.write(modified_content_end)


import re

# Vraag de gebruiker om de naam van het inputbestand
input_filename = input("Voer de naam van het inputbestand in (bijv. zzm_aangepast_stap3_xml.rdf): ")

# Vraag de gebruiker om de naam van het outputbestand
output_filename = input("Voer de naam van het outputbestand in (bijv. zzm_aangepast_stap4_xml.rdf): ")

# Lees het oorspronkelijke XML-bestand
with open(input_filename, 'r', encoding='utf-8') as file:
    rdf_content = file.read()

# Definieer het patroon voor <sys:Object> tags
sys_object_pattern = r'<nave:DcnResource>|</nave:DcnResource>'

print("Verwijderen van <nave:DcnResource></nave:DcnResource> tags...")

# Verwijder de <sys:Object> en </sys:Object> tags
modified_content = re.sub(sys_object_pattern, '', rdf_content)

# Verwijder overgebleven lege regels
modified_content = re.sub(r'\n\s*\n', '\n', modified_content)

print("Schrijven naar outputbestand...")

# Schrijf het aangepaste XML-bestand
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(modified_content)

print("Conversie voltooid!")

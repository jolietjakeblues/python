import re
import sys

# Vraag om input bestandsnaam
input_filename = input("Voer de naam van het inputbestand in (bijv. 'zuiderzeemuseum.rdf'): ")

# Vraag om output bestandsnaam
output_filename = input("Voer de naam van het outputbestand in (bijv. 'zzm_aangepast_stap5_xml.rdf'): ")

# Lees het oorspronkelijke XML-bestand
try:
    with open(input_filename, 'r', encoding='utf-8') as file:
        rdf_content = file.read()
except FileNotFoundError:
    print(f"Fout: Het bestand '{input_filename}' is niet gevonden.")
    sys.exit() ]

# Definieer het patroon voor <skos:Concept> tags
sys_object_pattern = r'<skos:Concept>|</skos:Concept>'

# Verwijder de <skos:Concept> en </skos:Concept> tags
modified_content = re.sub(sys_object_pattern, '', rdf_content)

# Verwijder overgebleven lege regels
modified_content = re.sub(r'\n\s*\n', '\n', modified_content)

# Schrijf het aangepaste XML-bestand
with open(output_filename, 'w', encoding='utf-8') as file:
    for i, line in enumerate(modified_content.splitlines()):
        # Voortgangsindicator
        if i % 1000 == 0:  # Update elke 1000 regels
            print(f"Verwerking... {i} regels geschreven")
        file.write(line + '\n')
    print(f"Conversie voltooid! Bestand opgeslagen als '{output_filename}'")

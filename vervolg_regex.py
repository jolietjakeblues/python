# Vraag de gebruiker om de bestandsnaam in te voeren
filename = input("Geef de naam van het bestand dat u wilt bewerken (bijv. output.txt): ")

# Lees het bestand in
with open(filename, 'r', encoding='utf-8') as file:
    input_data = file.read()

# Voeg <ceox:heeftMetadata> toe aan <ore:Aggregation>
start_idx = input_data.find('<ore:Aggregation rdf:about="http://data.collectienederland.nl/resource/aggregation/zuiderzeemuseum/007140">')
end_idx = input_data.find('</ore:Aggregation>', start_idx)
aggregation_part = input_data[start_idx:end_idx]
aggregation_part += '\n\t<ceox:heeftMetadata rdf:resource="http://data.collectienederland.nl/resource/subject/zuiderzeemuseum/007140/"/>\n'
input_data = input_data[:start_idx] + aggregation_part + input_data[end_idx:]

# Verwijder onnodige skos en nave delen
sections_to_remove = ['<skos:Concept>', '</skos:Concept>', '<nave:BrabantCloudResource>', '</nave:BrabantCloudResource>',
                      '<nave:RijksCollection>', '</nave:RijksCollection>', '<nave:DelvingResource>', '</nave:DelvingResource>']

for section in sections_to_remove:
    input_data = input_data.replace(section, "")

# Schrijf het resultaat naar een nieuw bestand
output_filename = "modified_" + filename
with open(output_filename, "w", encoding='utf-8') as f:
    f.write(input_data)

print(f"Bewerking voltooid! Het aangepaste bestand is opgeslagen als '{output_filename}'.")

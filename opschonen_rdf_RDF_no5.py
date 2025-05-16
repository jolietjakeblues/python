def clean_xml_rdf():
    # Vraag om input en output bestandsnamen
    input_name = input("Voer de naam van het inputbestand in: ")
    output_name = input("Voer de naam van het outputbestand in: ")

    with open(input_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Verwijder alle regels met </rdf:RDF> behalve de laatste
    last_index = None
    for index, line in reversed(list(enumerate(lines))):
        if '</rdf:RDF>' in line:
            last_index = index
            break

    lines = [line for index, line in enumerate(lines) if '</rdf:RDF>' not in line or index == last_index]

    # Verwijder alle regels die starten met <rdf:RDF xmlns: behalve de eerste
    first_index = None
    for index, line in enumerate(lines):
        if line.startswith('<rdf:RDF xmlns:'):
            if first_index is None:
                first_index = index
            else:
                lines[index] = ""

    # Schrijf naar het outputbestand
    with open(output_name, 'w', encoding='utf-8') as file:
        for index, line in enumerate(lines):
            # Voortgangsindicator
            print(f"Voortgang: {index + 1}/{len(lines)}", end='\r')
            file.write(line)

    print("\nBestand is schoongemaakt en opgeslagen!")

clean_xml_rdf()

def clean_rdf_file():
    input_name = input("Voer de naam van het invoerbestand in: ")
    output_name = input("Voer de naam van het uitvoerbestand in: ")

    with open(input_name, 'r') as file:
        lines = file.readlines()

    # Verwijder alle </rdf:RDF> behalve de laatste
    lines = [line for line in lines if line.strip() != '</rdf:RDF>']
    lines.append('</rdf:RDF>\n')

    # Verwijder alle regels die beginnen met <rdf:RDF xmlns: behalve de eerste
    rdf_start_lines = [line for line in lines if line.strip().startswith('<rdf:RDF xmlns:')]
    if rdf_start_lines:
        first_rdf_start = rdf_start_lines[0]
        lines = [line if line != first_rdf_start else "" for line in lines]
        lines[0] = first_rdf_start

    with open(output_name, 'w') as file:
        for index, line in enumerate(lines, start=1):
            file.write(line)
            # Voortgangsindicator
            print(f"Verwerking: {index}/{len(lines)} regels", end='\r')

    print("\nBestand is succesvol schoongemaakt!")

clean_rdf_file()

import re

# Functie om XML-bestanden te splitsen op basis van <zaken> en </zaken> tags
def split_xml(input_file, output_prefix):
    with open(input_file, 'r', encoding='utf-8') as f:
        # Begin met het lezen van de regels
        inside_zaken = False
        current_zaken = []
        count = 0
        for line in f:
            # Zoek de start van een zakenblok
            if '<zaken>' in line:
                inside_zaken = True
                current_zaken = []

            # Voeg de inhoud toe aan de huidige zaken
            if inside_zaken:
                current_zaken.append(line)

            # Zoek het einde van een zakenblok
            if '</zaken>' in line:
                inside_zaken = False
                output_file = f"{output_prefix}_{count}.xml"
                with open(output_file, 'w', encoding='utf-8') as output:
                    output.write(''.join(current_zaken))
                print(f"Gesplitste gegevens opgeslagen in: {output_file}")
                count += 1


# Geef het pad naar de grote XML-bestand en een prefix voor de uitvoerbestanden op
input_file = "E:\I_ldv_cho.xml"
output_prefix = 'E:\zaken_ldv.xml'

# Roep de functie aan om de XML-bestanden te splitsen
split_xml(input_file, output_prefix)

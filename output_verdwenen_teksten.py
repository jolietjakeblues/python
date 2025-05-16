import os

# Vraag om de bestandsnaam
bestandsnaam = input("Voer de naam van het XML-bestand in: ")

# Zoektekst
zoektekst = "Deze tekst is verhuisd naar"

# Outputbestand
output_bestand = "kennisregistratie.txt"

# Open het XML-bestand en het outputbestand
with open(bestandsnaam, 'r', encoding='utf-8') as xml_bestand, open(output_bestand, 'w', encoding='utf-8') as output:
    # Voortgangsindicator
    print("Bezig met zoeken...")
    
    # Loop door elk regel in het XML-bestand
    for regel in xml_bestand:
        # Zoek de zoektekst in de regel
        if zoektekst in regel:
            # Schrijf de gevonden regel naar het outputbestand
            output.write(regel.strip() + '\n')
    
    # Geef aan dat het zoeken is voltooid
    print("Zoeken voltooid. Resultaten zijn opgeslagen in", output_bestand)

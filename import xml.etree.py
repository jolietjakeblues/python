import xml.etree.ElementTree as ET
from tqdm import tqdm

# XML-bestandspad
xml_file_path = "E:\I_ldv_cho.xml"

# Functie om XML-bestand te lezen en gegevens te extraheren
def parse_xml(xml_file, output_file):
    # Open het uitvoerbestand om data naar te schrijven
    with open(output_file, 'w') as f:
        # Schrijf kolomkoppen naar uitvoerbestand
        f.write("zaakid|zaaknummer|zaaktype|choid|\n")

        # XML-bestand inlezen
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Alle <zaak> elementen doorlopen
        for zaak in tqdm(root.findall('zaak'), desc="Parsing XML"):
            # Gegevens van elk <zaak> element ophalen
            zaakid = zaak.find('zaakId').text
            zaaknummer = zaak.find('zaaknummer').text
            zaaktype = zaak.find('zaaktype').text

            # In dit voorbeeld gaan we ervan uit dat er slechts één <zaakobject> element is per <zaak>
            # Als er meerdere <zaakobject> elementen zijn, moet je hierdoor een lus maken
            choid = zaak.find('zaakobject/choId').text

            # Schrijf de geëxtraheerde gegevens naar het uitvoerbestand
            f.write(f"{zaakid}|{zaaknummer}|{zaaktype}|{choid}\n")

# XML-bestand parsen en gegevens naar een uitvoerbestand schrijven
parse_xml(xml_file_path, "uitvoer.csv")

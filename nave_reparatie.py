from lxml import etree
from tqdm import tqdm

def process_xml(input_filename, output_filename):
    # Parseer het XML-bestand
    tree = etree.parse(input_filename)
    root = tree.getroot()

    # Definieer namespaces
    ns = {
        'nave': 'http://schemas.delving.eu/nave/terms/',
        'skos': 'http://www.w3.org/2004/02/skos/core#',
        'edm': 'http://www.europeana.eu/schemas/edm/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    # Verwerk elk <nave:material> element
    for elem in tqdm(root.xpath(".//nave:material", namespaces=ns)):
        # Zoek naar het overeenkomstige <edm:ProvidedCHO> element op basis van identifier
        matching_providedCHO = root.xpath(f".//edm:ProvidedCHO[dc:identifier='{elem.text}']", namespaces=ns)
        
        # Hernoem en verplaats het element indien een match is gevonden
        if matching_providedCHO:
            elem.tag = "{%s}prefLabel" % ns['skos']
            matching_providedCHO[0].append(elem)

    # Sla het aangepaste XML-bestand op
    tree.write(output_filename, pretty_print=True, xml_declaration=True, encoding="utf-8")

# Vraag om input en output bestandsnamen
input_filename = input("Geef de naam van het input bestand: ")
output_filename = input("Geef de naam van het output bestand: ")

process_xml(input_filename, output_filename)

import xml.etree.ElementTree as ET
import sys

def add_namespaces(tree):
    root = tree.getroot()
    namespaces = {
        "owl": "http://www.w3.org/2002/07/owl#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nave": "http://schemas.delving.eu/nave/terms/",
        "dcterms": "http://purl.org/dc/terms/",
        "wgs84_pos": "http://www.w3.org/2003/01/geo/wgs84_pos#",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "ore": "http://www.openarchives.org/ore/terms/",
        "ceox": "https://linkeddata.cultureelerfgoed.nl/def/ceox/",
        "edm": "http://www.europeana.eu/schemas/edm/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    for prefix, uri in namespaces.items():
        root.set(f"xmlns:{prefix}", uri)

def transform_data(tree):
    ns = {
        "owl": "http://www.w3.org/2002/07/owl#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nave": "http://schemas.delving.eu/nave/terms/",
        "dcterms": "http://purl.org/dc/terms/",
        "wgs84_pos": "http://www.w3.org/2003/01/geo/wgs84_pos#",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "ore": "http://www.openarchives.org/ore/terms/",
        "ceox": "https://linkeddata.cultureelerfgoed.nl/def/ceox/",
        "edm": "http://www.europeana.eu/schemas/edm/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    
    # Metadata koppeling toevoegen
    for aggregation in tree.findall(".//ore:Aggregation", ns):
        resource_value = aggregation.find("edm:aggregatedCHO", ns).get('rdf:resource').replace("document", "subject")
        metadata_elem = ET.SubElement(aggregation, 'ceox:heeftMetadata')
        metadata_elem.set('rdf:resource', resource_value)
    
    # Afbeeldingsverwijzing toevoegen
    for providedCHO in tree.findall(".//edm:ProvidedCHO", ns):
        parent = providedCHO.getparent()
        depiction_value = parent.find(".//edm:isShownBy", ns).get('rdf:resource')
        depiction_elem = ET.SubElement(providedCHO, 'foaf:depiction')
        depiction_elem.set('rdf:resource', depiction_value)
    
    # Metadata sectie genereren
    for ceox_ff in tree.findall(".//ceox:ff", ns):
        metadata_elem = ET.Element('ceox:Metadata')
        for child in ceox_ff:
            metadata_elem.append(child)
        tree.getroot().append(metadata_elem)
        tree.getroot().remove(ceox_ff)

def main():
    input_file = input("Geef de bestandsnaam voor invoer: ")
    output_file = input("Geef de bestandsnaam voor uitvoer: ")

    try:
        tree = ET.parse(input_file)
        print("Bestand wordt verwerkt...")

        add_namespaces(tree)
        transform_data(tree)
        
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Verwerking voltooid. Gegevens opgeslagen in {output_file}.")

    except ET.ParseError:
        print("Fout bij het parseren van het XML-bestand.")
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")

if __name__ == "__main__":
    main()

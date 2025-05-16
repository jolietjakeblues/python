from xml.etree import ElementTree as ET

def add_namespaces(root):
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

def process_aggregation(elem):
    aggregated_cho = elem.find("edm:aggregatedCHO", NAMESPACES).get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource")
    metadata_value = aggregated_cho.replace('/document/', '/subject/')
    ceox_metadata = ET.Element("ceox:heeftMetadata")
    ceox_metadata.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", metadata_value)
    elem.append(ceox_metadata)

def process_providedCHO(elem, root):
    about_value = elem.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")
    aggregation = root.find(f"./ore:Aggregation[edm:aggregatedCHO/@rdf:resource='{about_value}']", NAMESPACES)
    if aggregation is not None:
        isShownBy = aggregation.find("edm:isShownBy", NAMESPACES)
        if isShownBy is not None:
            depiction = ET.Element("foaf:depiction")
            depiction.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", isShownBy.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"))
            elem.append(depiction)

def process_ceox_metadata(root):
    # Dummy code for creating the ceox:Metadata element as the "oud model" structure wasn't provided in the question
    ceox_metadata = ET.Element("ceox:Metadata")
    for skos_label in root.findall(".//skos:prefLabel", NAMESPACES):
        ceox_metadata.append(skos_label)
    for nave_element in root.findall(".//nave:*", NAMESPACES):
        ceox_metadata.append(nave_element)
    root.append(ceox_metadata)

if __name__ == "__main__":
    input_file = input("Please provide the input file name: ")
    output_file = input("Please provide the output file name: ")

    tree = ET.parse(input_file)
    root = tree.getroot()

    NAMESPACES = {node[0]: node[1] for _, node in ET.iterparse(input_file, events=['start-ns'])}

    add_namespaces(root)

    for elem in root.findall("ore:Aggregation", NAMESPACES):
        process_aggregation(elem)

    for elem in root.findall("edm:ProvidedCHO", NAMESPACES):
        process_providedCHO(elem, root)

    process_ceox_metadata(root)

    # Saving the tree
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    print(f"Processed and saved to {output_file}!")

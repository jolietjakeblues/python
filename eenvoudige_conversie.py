import xml.etree.ElementTree as ET

NAMESPACES = {
    'ceox': 'https://linkeddata.cultureelerfgoed.nl/def/ceox/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'edm': 'http://www.europeana.eu/schemas/edm/',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'nave': 'http://schemas.delving.eu/nave/terms/',
    'ore': 'http://www.openarchives.org/ore/terms/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'skos': 'http://www.w3.org/2004/02/skos/core#'
}

def process_providedCHO(root):
    for cho in root.findall('.//edm:ProvidedCHO', NAMESPACES):
        about_value = cho.attrib.get(f"{{{NAMESPACES['rdf']}}}about")
        
        # Zoek de overeenkomstige Aggregation
        aggregation = root.find(f"./ore:Aggregation[edm:aggregatedCHO/@rdf:resource='{about_value}']", NAMESPACES)
        
        # Voeg de heeftMetadata-tag toe aan Aggregation als deze niet bestaat
        if aggregation is not None and not aggregation.find('ceox:heeftMetadata', NAMESPACES):
            metadata_elem = ET.Element(f"{{{NAMESPACES['ceox']}}}heeftMetadata")
            metadata_elem.set(f"{{{NAMESPACES['rdf']}}}resource", f"http://data.collectienederland.nl/resource/subject/{about_value.split('/')[-1]}")
            aggregation.append(metadata_elem)

def main():
    tree = ET.parse('zzm_48.rdf')
    root = tree.getroot()

    process_providedCHO(root)
    tree.write('zzm_48_03.rdf', encoding='utf-8')

if __name__ == "__main__":
    main()

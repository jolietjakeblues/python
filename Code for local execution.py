import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm

def process_xml(input_filename, output_filename):
    # Parse the XML data
    tree = ET.parse(input_filename)
    root = tree.getroot()
    
    # Ensure the root has the foaf namespace definition
    if not 'xmlns:foaf' in root.attrib:
        root.set('xmlns:foaf', 'http://xmlns.com/foaf/0.1/')

    # Define the namespaces for easier querying
    namespaces = {
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'dc': "http://purl.org/dc/elements/1.1/",
        'dcterms': "http://purl.org/dc/terms/",
        'edm': "http://www.europeana.eu/schemas/edm/",
        'nave': "http://schemas.delving.eu/nave/terms/",
        'ore': "http://www.openarchives.org/ore/terms/",
        'skos': "http://www.w3.org/2004/02/skos/core#",
        'wgs84_pos': "http://www.w3.org/2003/01/geo/wgs84_pos#",
        'foaf': "http://xmlns.com/foaf/0.1/"
    }
    
    # Process each <ore:Aggregation> tag
    aggregations = list(root.findall('ore:Aggregation', namespaces))
    for aggregation in tqdm(aggregations, desc="Processing", ncols=100):
        # Extract the value of the <edm:isShownBy rdf:resource="..."/> tag
        is_shown_by = aggregation.find('edm:isShownBy', namespaces)
        if is_shown_by is not None:
            resource_value = is_shown_by.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"]
            
            # Create a new tag <foaf:depiction> [value] </foaf:depiction>
            depiction = ET.Element('foaf:depiction')
            depiction.text = resource_value
            
            # Get the related <edm:ProvidedCHO rdf:about=...> block
            aggregated_cho = aggregation.find('edm:aggregatedCHO', namespaces)
            if aggregated_cho is not None:
                about_value = aggregated_cho.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"]
                for provided_cho in root.findall('edm:ProvidedCHO', namespaces):
                    if provided_cho.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"] == about_value:
                        provided_cho.append(depiction)
                        break

    # Serialize the modified XML
    modified_xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')
    # Using minidom for pretty printing
    pretty_xml = minidom.parseString(modified_xml_str).toprettyxml(indent="    ")
    
    # Write to output file
    with open(output_filename, 'w', encoding="utf-8") as f:
        f.write(pretty_xml)

# Uncomment these lines to run locally
input_filename = input("Please provide the input filename: ")
output_filename = input("Please provide the output filename: ")
process_xml(input_filename, output_filename)

# Note: Make sure to install the tqdm package locally using pip before executing the code.
# pip install tqdm

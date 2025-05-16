import re
import rdflib

def fix_rdf_file(rdf_path):
    with open(rdf_path, 'r') as file:
        content = file.read()

    # Using regex to find all RDF blocks
    rdf_blocks = re.findall(r'<rdf:RDF.*?</rdf:RDF>', content, re.DOTALL)

    # Combining the RDF blocks into one if there are multiple blocks
    if len(rdf_blocks) > 1:
        combined_block = rdf_blocks[0]
        for block in rdf_blocks[1:]:
            # Removing the opening and closing RDF tags
            cleaned_block = re.sub(r'<rdf:RDF.*?>', '', block)
            cleaned_block = cleaned_block.replace('</rdf:RDF>', '').strip()
            combined_block += '\n' + cleaned_block

        content = combined_block + '\n</rdf:RDF>'

    with open(rdf_path, 'w') as file:
        file.write(content)

def rdf_to_trig(rdf_file, trig_file):
    # Create an RDF graph and parse the RDF/XML
    g = rdflib.Graph()
    g.parse(rdf_file, format="xml")

    # Serialize and save the data in TriG format
    trig_data = g.serialize(format="trig").decode("utf-8")
    with open(trig_file, 'w') as f:
        f.write(trig_data)

def main():
    rdf_path = "am.rdf"
    trig_path = "am_clean.trig"

    # Fix the RDF file to ensure it has only one root element
    fix_rdf_file(rdf_path)

    # Convert the fixed RDF file to a TriG file
    rdf_to_trig(rdf_path, trig_path)

if __name__ == "__main__":
    main()

def fix_rdf_file(rdf_path):
    with open(rdf_path, 'r') as file:
        content = file.read()

    # Remove XML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

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

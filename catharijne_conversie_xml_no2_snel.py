import re
from tqdm import tqdm

# Ask for input and output filenames
input_filename = input("Please enter the input filename (including path): ")
output_filename = input("Please enter the output filename (including path): ")

# Read the RDF/XML file
with open(input_filename, 'r', encoding='utf-8') as file:
    rdf_content = file.read()

# Split the rdf_content using the concept blocks as delimiters
split_content = re.split(r'(<sys:Object>.*?</sys:Object>)', rdf_content, flags=re.DOTALL)

modified_content = []

# Process each segment of the split content
for segment in tqdm(split_content, desc="Processing blocks"):
    # Check if the segment is a concept block
    if segment.startswith('<sys:Object>'):
        # Find the content between <edm:ProvidedCHO ...> and </edm:ProvidedCHO> within each concept_block
        providedcho_match = re.search(r'<edm:ProvidedCHO(.*?)>', segment, re.DOTALL)
        
        if providedcho_match:
            cho_id = providedcho_match.group(1)  # Get the content between the tags
            new_tag = f'<edm:ProvidedCHO rdf:about={cho_id}>'  # Create the new tag

            # Add the new tag to the concept_block
            segment = segment.replace('<edm:Place>', new_tag + "\n" + '<edm:Place>', 1)
            
    modified_content.append(segment)

# Join the modified content to form the complete string
rdf_content_modified = ''.join(modified_content)

# Write the adjusted XML file
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(rdf_content_modified)

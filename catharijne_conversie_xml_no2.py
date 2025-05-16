import re
from tqdm import tqdm

# Ask for input and output filenames
input_filename = input("Please enter the input filename (including path): ")
output_filename = input("Please enter the output filename (including path): ")

# Read the RDF/XML file
with open(input_filename, 'r', encoding='utf-8') as file:
    rdf_content = file.read()

# Find all occurrences of <sys:Object>...</sys:Object> blocks
concept_blocks = re.findall(r'<sys:Object>.*?</sys:Object>', rdf_content, re.DOTALL)

# Loop through the found blocks with progress indication
for concept_block in tqdm(concept_blocks, desc="Processing blocks"):
    # Find the content between <edm:ProvidedCHO ...> and </edm:ProvidedCHO> within each concept_block
    providedcho_match = re.search(r'<edm:ProvidedCHO(.*?)>', concept_block, re.DOTALL)

    if providedcho_match:
        cho_id = providedcho_match.group(1)  # Get the content between the tags
        new_tag = f'<edm:ProvidedCHO rdf:about={cho_id}>'  # Create the new tag

        # Add the new tag to the concept_block
        modified_block = concept_block.replace('<edm:Place>', new_tag + "\n" + '<edm:Place>', 1)

        # Replace the original concept_block with the modified concept_block in rdf_content
        rdf_content = rdf_content.replace(concept_block, modified_block)

# Write the adjusted XML file
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(rdf_content)

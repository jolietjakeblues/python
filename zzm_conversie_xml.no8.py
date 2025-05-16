from tqdm import tqdm

import re

def transform_content(content):
    # Check for the specific tag and perform the transformation
    if '<edm:ProvidedCHO rdf:about="http://data.collectienederland.nl/resource/document/' in content:
        content = re.sub(r' /([a-z])">', r'-\1">', content)        # For /c">
        content = re.sub(r' ([a-z])/([a-z])">', r'-\1-\2">', content) # For c/h">
        content = re.sub(r' /([0-9]{2})">', r'-\1">', content)           # For /01">
        content = re.sub(r' /([a-z])/([a-z])">', r'-\1-\2">', content) # For /c/h">
        content = re.sub(r' /([a-z])-([a-z])-([a-z])">', r'-\1-\2">', content) # For /a-b-c">
    return content

def main():
    # Ask for input and output filenames
    input_filename = input("Enter the input filename: ")
    output_filename = input("Enter the output filename: ")

    # Read the input file
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Transform the content and write to the output file
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in tqdm(lines, desc="Processing"):
            outfile.write(transform_content(line))

    print(f"Transformation completed. Check the output in {output_filename}")

if __name__ == "__main__":
    main()

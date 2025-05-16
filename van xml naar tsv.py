import re

def remove_tags(text):
    # Remove values between < > and the < > themselves
    return re.sub(r'<.*?>', '', text)

def xml_to_tab(xml_data, output_filename):
    # Define headers
    headers = ["identifier", "datestamp", "setSpec", "identifierType", "identifier",
               "creator", "title", "publisher", "subject", "contributor", 
               "dateSubmitted", "dateIssued", "dateCreated", "language", 
               "resourceType", "alternateIdentifier", "relatedIdentifier",
               "size", "rights", "description", "geoLocationPlace", "identifierURI"]

    # Open tab-delimited file for writing
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        # Write header row
        outfile.write('\t'.join(headers) + '\n')

        # Extract data rows
        records = re.findall(r'<record>(.*?)</record>', xml_data, re.DOTALL)
        for record in records:
            row_data = []
            for header in headers[:-1]:  # Exclude identifierURI for now
                # Find all values for the current header
                values = re.findall(rf'<{header}[^>]*>(.*?)</{header}>', record)
                if values:
                    # If multiple values found, join them with "|"
                    row_data.append('|'.join(remove_tags(value) for value in values))
                else:
                    row_data.append('')  # Empty value if not found

            # Extract relatedIdentifierURI
            related_uri_match = re.search(r'<relatedIdentifier\srelatedIdentifierType="URL"\srelationType="isSupplementBy">(.*?)</relatedIdentifier>', record)
            if related_uri_match:
                row_data.append(related_uri_match.group(1))
            else:
                row_data.append('')

            # Write row to file
            outfile.write('\t'.join(row_data) + '\n')

    print(f"Tab-delimited file '{output_filename}' has been created successfully.")

def main():
    input_filename = input("Enter the input filename: ")
    # Append '.tsv' extension to output filename
    output_filename = input("Enter the output filename (without extension): ") + ".tsv"

    # Read the XML-like data from the input file
    with open(input_filename, 'r', encoding='utf-8') as infile:  # Specify encoding here
        xml_data = infile.read()

    # Convert XML-like data to tab-delimited format
    xml_to_tab(xml_data, output_filename)

if __name__ == "__main__":
    main()

import csv

# Set up the prefixes
prefixes = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'edm': 'http://www.europeana.eu/schemas/edm/'
}

# Set up the output file
output_file = open('am-CN.ttl', 'w')

# Write the prefixes to the output file
for prefix, uri in prefixes.items():
    output_file.write(f'@prefix {prefix}: <{uri}> .\n')

# Open the input CSV file
with open('AM-CN.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='|')

    # Loop over the rows in the CSV file
    for row in csv_reader:

        # Write the turtle subject line
        output_file.write(f'<https://linkeddata.cultureelerfgoed.nl/cn/am/{row["priref"]}> a edm:ProvidedCHO;\n')

        # Loop over the properties in the row
        for prop, value in row.items():

            # Skip the priref property, since we've already used it as the subject
            if prop == 'priref':
                continue
            # Remove the space and number from the property name
            prop = row['property'].replace(' ', '').replace('1', '')
            output_file.write(f'{prefixes[prop]}{prop} "{value}" ;\n')

        # Finish the turtle subject
        output_file.write('.\n\n')

# Close the output file
output_file.close()

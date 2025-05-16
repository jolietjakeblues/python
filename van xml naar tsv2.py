import csv
import re

def extract_data(record):
    data = {}
    fields = {
        'identifier': r'<identifier>(.*?)</identifier>',
        'datestamp': r'<datestamp>(.*?)</datestamp>',
        'setSpec': r'<setSpec>(.*?)</setSpec>',
        'identifierType': r'<identifier identifierType="(.*?)"',
        'identifierURL': r'<identifier identifierType="URL">(.*?)</identifier>',
        'creator': r'<creatorName>(.*?)</creatorName>',
        'title': r'<title>(.*?)</title>',
        'publisher': r'<publisher>(.*?)</publisher>',
        'subjects': r'<subject[^>]*>(.*?)</subject>',
        'contributor': r'<contributorName>(.*?)</contributorName>',
        'dateSubmitted': r'<date dateType="Submitted">(.*?)</date>',
        'dateIssued': r'<date dateType="Issued">(.*?)</date>',
        'dateCreated': r'<date dateType="Created">(.*?)</date>',
        'language': r'<language>(.*?)</language>',
        'resourceType': r'<resourceType[^>]*>(.*?)</resourceType>',
        'alternateIdentifiers': r'<alternateIdentifiers?>(.*?)</alternateIdentifiers?>',
        'relatedIdentifiers': r'<relatedIdentifiers?>(.*?)</relatedIdentifiers?>',
        'size': r'<size>(.*?)</size>',
        'rights': r'<rights>(.*?)</rights>',
        'descriptions': r'<description[^>]*>(.*?)</description>',
        'geoLocationPlace': r'<geoLocationPlace>(.*?)</geoLocationPlace>',
    }

    for field, pattern in fields.items():
        matches = re.findall(pattern, record, re.DOTALL)
        if matches:
            data[field] = '|'.join(re.sub('<[^<]+?>', '', match.strip()) for match in matches)
        else:
            data[field] = ''

    return data

def xml_to_csv(xml_data, output_filename):
    headers = ["identifier", "datestamp", "setSpec", "identifierType", "identifierURL",
               "creator", "title", "publisher", "subjects", "contributor", 
               "dateSubmitted", "dateIssued", "dateCreated", "language", 
               "resourceType", "alternateIdentifiers", "relatedIdentifiers",
               "size", "rights", "descriptions", "geoLocationPlace"]

    with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers, delimiter='\t')
        writer.writeheader()

        records = re.findall(r'<record>(.*?)</record>', xml_data, re.DOTALL)
        for record in records:
            row_data = extract_data(record)
            writer.writerow(row_data)

    print(f"CSV file '{output_filename}' has been created successfully.")

def main():
    input_filename = input("Enter the input filename (with extension): ")
    with open(input_filename, 'r', encoding='utf-8') as infile:
        xml_data = infile.read()
    
    output_filename = input("Enter the output filename (without extension): ") + ".csv"
    xml_to_csv(xml_data, output_filename)

if __name__ == "__main__":
    main()

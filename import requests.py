import requests
import xml.etree.ElementTree as ET

# Set the OAI-PMH endpoint URL
url = 'https://prod.dcn.hubs.delving.org/api/oai-pmh/'
#https://prod.dcn.hubs.delving.org/api/oai-pmh/?verb=ListRecords&metadataPrefix=edm&set=atlas-of-mutual-heritage
# Set the initial request parameters
params = {
    'verb': 'ListRecords',
    'metadataPrefix': 'edm',
    'set': 'atlas-of-mutual-heritage'
}

# Keep making requests until there are no more resumption tokens
while True:
        # Make the request and get the response
    # Make the request and get the response
    response = requests.get(url, params=params)
    print(response.url)

    # Parse the response as XML
    xml = ET.fromstring(response.content)

    # Append the records to the output file
    with open('data_am2.rdf', 'a') as f:
        for record in xml.findall('.//{http://www.openarchives.org/OAI/2.0/}record'):
            f.write(ET.tostring(record).decode())

    # Check for a resumption token
    resumption_token = xml.find('.//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
    if resumption_token is not None:
        # Set the new request parameters with the resumption token
        params = {
            'verb': 'ListRecords',
            'metadataPrefix': 'edm',
            'set': 'atlas-of-mutual-heritage',
            'resumptionToken': resumption_token.text
        }
    else:
        # No more resumption tokens, so break out of the loop
        break

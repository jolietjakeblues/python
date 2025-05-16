# Set the OAI-PMH endpoint URL
url = 'https://prod.dcn.hubs.delving.org/api/oai-pmh/'

# Set the initial request parameters
params = {
    'verb': 'ListRecords',
    'metadataPrefix': 'edm',
    'set': 'atlas-of-mutual-heritage'
}

# Keep track of the number of records
num_records = 0

# Keep making requests until there are no more resumption tokens
while True:
    # Make the request and get the response
    response = requests.get(url, params=params)
    
    # Print the request URL for debugging purposes
    print(response.url)

    # Parse the response as XML
    xml = ET.fromstring(response.content)

    # Append the records to the output file
    with open('data_am.xml', 'a') as f:
        for record in xml.findall('.//{http://www.openarchives.org/OAI/2.0/}record'):
            f.write(ET.tostring(record).decode())
            num_records += 1

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

    # Check if the completeListSize attribute is present
    complete_list_size = xml.find('.//{http://www.openarchives.org/OAI/2.0/}ListRecords').get('completeListSize')
    if complete_list_size is not None and num_records >= int(complete_list_size):
        # We have retrieved all the records, so break out of the loop
        break

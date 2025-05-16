# import de requests library. This block imports the necessary libraries for making HTTP requests, encoding and decoding URLs, and using HTTP basic authentication.
# for API documentation see <https://help.poolparty.biz/8.1/en/developer-guide/basic---advanced-server-apis/thesaurus---ontology-manager-api/collection-services/web-service-method--add-concept-to-collection.html>

import requests, urllib.parse, base64
from urllib.parse import urlencode, quote_plus, unquote
from requests.auth import HTTPBasicAuth
# open document. This opens a file called "landschap.txt" and reads its contents into a list called "inhoud".
with open("pp_subtree_bebouwdeomgeving.txt","r") as l:
    inhoud = l.readlines()
#This loops through each item in the "inhoud" list, which contains concepts that need to be added to the thesaurus. For each concept, it creates a URL string with the PoolParty API endpoint for adding a concept to a collection. It also creates two dictionaries, "con" and "col", that hold the concept and collection information.
for item in inhoud:
    try:
# api-endpoint. Eigenlijk niet endpoint, maar met request
        url = "https://digitaalerfgoed.poolparty.biz/PoolParty/api/thesaurus/1DF17ED4-4A38-0001-C6FF-883013B04AD0/addConceptToCollection"
# concepts
        con = {'?concept': item.rstrip()}
        col = {'&collection': 'https://data.cultureelerfgoed.nl/term/id/cht/90de02e3-4ae8-4cc8-992f-422fe80a7b32'} #CHT
# encoding en decoding. This encodes the "col" and "con" dictionaries into URL-encoded strings and concatenates them with the API endpoint URL. The resulting URL string is then decoded to remove any percent-encoded characters. 
        url_col = urllib.parse.urlencode(col)
        url_con = urllib.parse.urlencode(con)
        url_con_col = url + url_con + url_col
        full_url = urllib.parse.unquote(url_con_col)
# uiteindelijke request
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        request = requests.post(full_url, headers=header, auth=HTTPBasicAuth('apiuser', 't9FafCBb5FDc23Px'))
# test print en statuscode
        print(full_url)
        print(request.status_code)
# de exeption van de try
    except Exception as e:
        print("Oeps")
 

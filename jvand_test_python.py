# importing the requests library
import requests, urllib.parse, base64
from urllib.parse import urlencode, quote_plus
# https://docs.python.org/2.7/howto/urllib2.html
# api-endpoint
con = {'concept': 'https://data.cultureelerfgoed.nl/term/id/cht/51121c7f-7cd8-4970-926c-0ee4f2dc2ffe'}
col = {'collection': 'https://data.cultureelerfgoed.nl/term/id/cht/e010aa4b-0b97-4e25-ae51-2644b20f43f1'}
url_values = urllib.parse.urlencode(con)
url_values2 = urllib.parse.urlencode(col)
url = "https://digitaalerfgoed.poolparty.biz/PoolParty/api/thesaurus/1DF17ED4-4A38-0001-C6FF-883013B04AD0/addConceptToCollection"
full_url = url + '?concept=' + url_values + '&collection=' + url_values2
# request
headers = {'Content-type': 'application/x-www-form-urlencoded'}
#headers = {'Authorization', b'Basic ' + base64.b64encode("apiuser" +b':' + "t9FafCBb5FDc23Px")} 
request = requests.post(full_url, auth=('apiuser', 't9FafCBb5FDc23P'))
#request.add_header('Authorization', b'Basic ' + base64.b64encode("apiuser" +b':' + "t9FafCBb5FDc23Px"))
#headers = {'Content-type': 'application/x-www-form-urlencoded'}
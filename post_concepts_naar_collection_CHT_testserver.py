# import de requests library
import requests, urllib.parse, base64
import tkinter as tk
from urllib.parse import urlencode, quote_plus, unquote
from requests.auth import HTTPBasicAuth
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.filename = filedialog,askopenfilename(initialdir="e:\", title ="Kies een file", fyletypes=(("txt files", "*.txt))
# open document
with open("post_telecom_collections.txt","r") as l:
    inhoud = l.readlines()
for item in inhoud:
    try:
# api-endpoint. Eigenlijk niet endpoint, maar met request
        url = "https://digitaalerfgoed-test.poolparty.biz/PoolParty/api/thesaurus/97866e08-48ab-42fb-9c14-dde5bc57a18f/addConceptToCollection"
# concepts
        con = {'?concept': item.rstrip()}
        col = {'&collection': 'https://data.cultureelerfgoed.nl/term/id/cht/e010aa4b-0b97-4e25-ae51-2644b20f43f1'}
# encoding en decoding
        url_col = urllib.parse.urlencode(col)
        url_con = urllib.parse.urlencode(con)
        url_con_col = url + url_con + url_col
        full_url = urllib.parse.unquote(url_con_col)
# uiteindelijke request
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        request = requests.post(full_url, headers=header, auth=HTTPBasicAuth('apiuser_jvand', 'apiuserjvand'))
# test print en statuscode
        print(full_url)
        print(request.status_code)
# de exeption van de try
    except Exception as e:
        print("ready")

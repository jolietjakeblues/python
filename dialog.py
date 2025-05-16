# import de requests library
import requests, urllib.parse, base64
import tkinter as tk
from urllib.parse import urlencode, quote_plus, unquote
from requests.auth import HTTPBasicAuth
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.filename = filedialog,askopenfilename(initialdir="e:\", title ="Kies een file", fyletypes=(("txt files", "*.txt))
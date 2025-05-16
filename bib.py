import requests
url = http://rce.adlibhosting.com/harvest/wwwopac.ashx?database=books&search=all&limit=5000&startfrom=5001&xmltype=grouped
r = requests.get(url, allow_redirects=True)
write(r.content)

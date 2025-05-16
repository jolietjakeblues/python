#!/usr/bin/env python3
 
lijst=[ 1, 5, 2, 33, 5, 16, 7 ]
totaal = sum(lijst)
aantal = len(lijst)
#print (lijst)
#print(totaal)
#print(aantal)
gemiddeld = totaal / aantal
print("Het gemiddelde van", lijst, "is:", round(gemiddeld,2))
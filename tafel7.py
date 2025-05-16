tafel = 7
for getal in range(1, 11):
   print(getal, "x", tafel, "=", getal * tafel)

#gespiekt
for getal, uitkomst in enumerate(range(tafel, tafel * 10 + 1, tafel)):
    print(getal + 1, 'x', tafel, '=', uitkomst)
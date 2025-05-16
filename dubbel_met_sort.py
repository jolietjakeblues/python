namen = [ 'els', 'els', 'els', 'Joop', 'joop', 'els', 'henk', 'henk', 'jan', 'jan', 'john', 'Joop', 'piet', 'piet' ]
print(namen)
klein_namen = [k.lower() for k in namen]
print(klein_namen)
list.sort(klein_namen)
print(klein_namen)
prevnm = None

for i, naam in enumerate(klein_namen):
    if prevnm == naam:
        print(i)
    prevnm = naam
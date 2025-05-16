namen = [ 'els', 'els', 'els', 'Joop', 'els', 'henk', 'henk', 'jan', 'jan', 'john', 'Joop', 'piet', 'piet' ]
print(namen)
list.sort(namen)
print(namen)
vorigenaam = None

for i, naam in enumerate(namen):
    if vorigenaam == naam:
        print(i)
    vorigenaam = naam
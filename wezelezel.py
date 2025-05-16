vraag = input("Stel een vraag: ") 
vraag = vraag.rstrip(" ?")      # verwijder spaties en vraagtekens aan het eind 
woorden = vraag.split()
if len(woorden)>0:
    woord = woorden.pop()       # neem het laatste woord 
    woord = woord[1:]           # verwijder eerste letter 
    medeklinkers = 'bcdfghjklmnpqrstvwxz'
    medeklinkers += medeklinkers.upper()
    woord = woord.lstrip(medeklinkers)  # verwijder begin-medeklinkers  
    woord = woord.capitalize()  # laat resultaat met hoofletter beginnen 
    print(woord)
else:
    print("Er is geen vraag opgegeven.")
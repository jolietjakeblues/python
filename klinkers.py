def telklinkers(tekst):
    import re
    patroon = re.compile("[AEIOUaeiou]")
    aantal = 0
    for patroon in tekst:
        if patroon.match(str(tekst)):
            aantal += 1
    return aantal

zin = "In deze zín staan %d klinkers"
print(zin % telklinkers(zin)) 
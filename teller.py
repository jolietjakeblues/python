def counter(filenaam):
    try:
        f = open(filenaam)
    except Exception:
        print('Bestand %s kan niet worden geopend' % filenaam, file=sys.stderr)
        raise

    rcount = 0 # regel teller 
    wcount = 0 # woorden teller 
    ccount = 0 # character teller 

    for regel in f:
        rcount += 1
        wcount += len(regel.split())
        ccount += len(regel)

    print("%15s: %5d %6d %7d" % (filenaam, rcount, wcount, ccount) )
    f.close()

import glob

filenamen = glob.glob("*.txt")
for file in filenamen:
    try:
        counter(file)
    except Exception:
        continue
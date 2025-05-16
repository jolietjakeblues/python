filename = 'verhaal.txt'

try:
    fh = open(filename,'r')
except Exception:
    import system
    print('File %s not found!' % filename)
    system.exit()

nr_of_lines = 0
nr_of_words = 0
nr_of_chars = 0

print()

for line in fh:
    print(line.rstrip())        # haal new line teken uit regel weg 
    nr_of_lines += 1            # hoog nr_of_lines op 
    words = line.split()        # breek regel op in woorden 
    nr_of_words += len(words)   # aantal woorden van regel = len(words) 
    nr_of_chars += len(line)    # aantal characters van regel = len(line) 

print('\nFile %s has %d lines, %d words, %d characters' % \
        (filename, nr_of_lines, nr_of_words, nr_of_chars))   
 
fh.close()
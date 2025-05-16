f = open("weer.txt")
for regel in f:
    if regel[0] == '#':
        continue
    print(regel, end='')
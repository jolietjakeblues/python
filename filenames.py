filenames = ['limerick.txt', 'news.1.pdf', 'verhaal']
for filename in filenames:
    zonder = filename.split(".")
    if len(zonder)>1:
        zonder.pop()
    print(".".join(zonder))

import csv
import random
import string
from lorem_text import lorem

# Functie om een willekeurige tekenreeks te genereren
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Functie om een willekeurig jaartal te genereren tussen 1800 en 2022
def generate_year():
    return random.randint(1800, 2022)

# Lijst met fictieve trefwoorden
trefwoorden = ["Fantasy", "Sciencefiction", "Romantiek", "Dystopie", "Klassieker", "Filosofie", "Avontuur", "Misdaadroman", "Coming-of-age", "Magie", "Politiek", "Sociale satire", "Rechtvaardigheid", "Psychologie", "Identiteit"]

# Functie om willekeurige trefwoorden te genereren
def generate_trefwoorden():
    return random.sample(trefwoorden, random.randint(2, 3))

# Functie om een willekeurige abstract van 100 woorden te genereren
def generate_abstract():
    return lorem.paragraph()

# Open een CSV-bestand om de gegevens in te schrijven
with open('boeken_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Boektitel', 'ISBN', 'Auteur', 'Jaar van uitgave', 'Plaats van uitgave', 'Uitgever', 'Aantal pagina\'s', 'Trefwoorden', 'Abstract']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # Genereer 1000 boeken
    for i in range(1000):
        writer.writerow({
            'Boektitel': f"Boek {i+1}",
            'ISBN': f"978012345678{i%10}",
            'Auteur': generate_random_string(random.randint(5, 15)),
            'Jaar van uitgave': generate_year(),
            'Plaats van uitgave': generate_random_string(random.randint(5, 15)),
            'Uitgever': generate_random_string(random.randint(5, 15)),
            'Aantal pagina\'s': random.randint(100, 600),
            'Trefwoorden': ', '.join(generate_trefwoorden()),
            'Abstract': generate_abstract()
        })

print("Dataset met 1000 boeken is gegenereerd.")

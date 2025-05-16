import xml.etree.ElementTree as ET
import os

def count_text_occurrences(xml_file_path, search_text):
    # Initialiseer de teller
    occurrences = 0

    # Open het XML-bestand
    with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
        # Doorloop het XML-document één regel tegelijk en tel het aantal voorkomens van de opgegeven tekst
        for line in xml_file:
            if search_text in line:
                occurrences += line.count(search_text)

    return occurrences

    # Bepaal de totale grootte van het XML-bestand
    total_size = os.path.getsize(xml_file)

    # Houd de huidige positie in het bestand bij
    current_position = 0

    # Doorloop het XML-document één element tegelijk en tel het aantal voorkomens van de opgegeven tekst
    for event, element in ET.iterparse(xml_file, events=("start", "end")):
        if event == "end" and element.text and search_text in element.text:
            occurrences += element.text.count(search_text)

        # Update de huidige positie in het bestand
        current_position = xml_file.tell()

        # Bereken en print de voortgang
        if total_size != 0:
            progress = (current_position / total_size) * 100
            print(f"Voortgang: {progress:.2f}%", end="\r")

    return occurrences

def main():
    # Vraag de gebruiker om het XML-bestand en de tekst waarin gezocht moet worden
    xml_file = input("Geef het pad naar het XML-document op: ")
    search_text = input("Geef de tekst op waarin gezocht moet worden (tussen aanhalingstekens): ")

    # Controleer of het pad naar het XML-bestand geldig is
    if not os.path.isfile(xml_file):
        print("Ongeldig pad naar het XML-document.")
        return

    # Verwijder dubbele aanhalingstekens als die zijn ingevoerd
    search_text = search_text.strip('"')

    # Tel het aantal voorkomens van de tekst in het XML-document
    count = count_text_occurrences(xml_file, search_text)
    print(f"Het aantal voorkomens van '{search_text}' in het XML-document is: {count}")

if __name__ == "__main__":
    main()

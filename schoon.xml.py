import xml.etree.ElementTree as ET
import os

def main():
    # 1. Bestandsnamen opvragen
    input_file = input("Geef de naam van uw XML-invoerbestand: ")
    output_file = input("Geef de naam voor uw nieuwe XML-bestand: ")

    if not os.path.isfile(input_file):
        print("Het opgegeven invoerbestand bestaat niet.")
        return

    # 2. Tags die u wilt verwijderen
    tags_to_remove = {
        "ccnl.edit.date",
        "edit.date",
        "edit.name",
        "edit.notes",
        "edit.source",
        "edit.time"
    }

    # 3. Voorbereiden iterparse
    print("Start met verwerken...")
    context = ET.iterparse(input_file, events=("start", "end"))
    
    # Eerste (root) element inlezen
    event, root = next(context)

    # Houd bij welke elementen openstaan
    stack = [root]

    count = 0  # Voor voortgang
    step = 1000  # Toon bericht om de 1000 elementen

    # 4. Verwerken van de rest van het bestand
    for event, elem in context:
        if event == "start":
            stack.append(elem)
        elif event == "end":
            count += 1
            if count % step == 0:
                print(f"Verwerkt: {count} elementen...")

            if elem.tag in tags_to_remove:
                # Verwijder dit element uit de ouder
                parent = stack[-2]  # Oudere element in de stack
                parent.remove(elem)
            # Stap terug in de stack
            stack.pop()

    print("Klaar met verwerken. Schrijf resultaat naar bestand...")

    # 5. Resultaat wegschrijven
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    print(f"Gereed. Bestand opgeslagen als: {output_file}")

if __name__ == "__main__":
    main()

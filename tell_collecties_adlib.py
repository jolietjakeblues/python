import xml.etree.ElementTree as ET
from openpyxl import Workbook
from tqdm import tqdm

def main():
    # Vraagt naar de paden
    xml_file = input("Geef het pad naar uw XML-bestand (incl. .xml): ")
    excel_output = input("Geef het pad voor het Excel-resultaat (bijv. .xlsx): ")

    # Teltags opslaan
    tag_counts = {}

    # Inlezen en parsen
    print("Bezig met lezen van XML-bestand...")
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Doorloop alle elementen met voortgangsindicator
    print("Tags tellen...")
    for elem in tqdm(root.iter()):
        if elem.text and elem.text.strip():
            tag_counts[elem.tag] = tag_counts.get(elem.tag, 0) + 1

    # Schrijf resultaten naar Excel
    print("Resultaten wegschrijven naar Excel...")
    wb = Workbook()
    ws = wb.active
    ws.title = "Tag Tellingen"
    ws.append(["Tag", "Aantal"])

    for tag, count in sorted(tag_counts.items()):
        ws.append([tag, count])

    wb.save(excel_output)
    print(f"Klaar. Resultaten staan in: {excel_output}")

if __name__ == "__main__":
    main()

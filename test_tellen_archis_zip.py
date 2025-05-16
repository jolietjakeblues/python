import xml.etree.ElementTree as ET
from collections import defaultdict
import zipfile
import io
import os
from tqdm import tqdm

def fix_xml_stream(file_obj):
    """Repareert en streamt XML zonder overbodige tekens en sluit correct af."""
    corrected_xml = io.BytesIO()
    first_line = file_obj.readline().decode('utf-8').strip()

    # Voeg XML-header toe als deze ontbreekt
    if not first_line.startswith('<?xml'):
        print("⚠️  XML-header ontbreekt, wordt toegevoegd...")
        corrected_xml.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        corrected_xml.write(b'<root>\n')  # Voeg root toe als fallback

    corrected_xml.write(first_line.encode('utf-8') + b'\n')

    has_root = False
    content_lines = []

    for line in file_obj:
        decoded_line = line.decode('utf-8').strip()

        if decoded_line:
            # Controleer of een root-element bestaat
            if decoded_line.startswith('<') and not decoded_line.startswith('<?xml'):
                has_root = True
            content_lines.append(decoded_line)

    # Voeg root toe als deze ontbreekt
    if not has_root:
        print("⚠️  Root-element ontbreekt, wordt toegevoegd...")
        corrected_xml.write(b"<root>\n")

    # Schrijf inhoud naar buffer
    for line in content_lines:
        corrected_xml.write(line.encode('utf-8') + b'\n')

    # Controleer of het bestand correct is afgesloten
    last_line = content_lines[-1] if content_lines else ""
    if not last_line.endswith(">"):
        print("⚠️  XML lijkt niet correct afgesloten, `</root>` wordt toegevoegd...")
        corrected_xml.write(b"</root>\n")

    corrected_xml.seek(0)
    return corrected_xml

def count_tags_in_xml(file_obj):
    """Telt XML-tags zonder het hele bestand in geheugen te laden."""
    tag_counts = defaultdict(int)

    # Fix XML indien nodig
    fixed_file = fix_xml_stream(file_obj)

    # Gebruik iterparse() direct op de gerepareerde stream
    try:
        context = ET.iterparse(fixed_file, events=('start', 'end'))
        for event, elem in context:
            if event == 'start':
                tag_counts[elem.tag] += 1
            elem.clear()
    except ET.ParseError as e:
        print(f"❌ XML-verwerking mislukt: {e}")

    return tag_counts

def write_tag_counts_to_file(tag_counts, output_file):
    """Schrijft de tag-tellingen naar een bestand."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for tag, count in tag_counts.items():
            f.write(f'{tag}: {count}\n')

def main():
    zip_file = input("Voer de naam van het ZIP-bestand in: ")
    output_file = input("Voer de naam van het uitvoerbestand in: ")

    with zipfile.ZipFile(zip_file, 'r') as z:
        xml_files = [name for name in z.namelist() if name.endswith('.xml')]
        
        if not xml_files:
            print("Geen XML-bestand gevonden in de ZIP.")
            return
        
        # Laat gebruiker kiezen als er meerdere XML-bestanden zijn
        if len(xml_files) > 1:
            print("Gevonden XML-bestanden in de ZIP:")
            for i, file in enumerate(xml_files, 1):
                print(f"{i}. {file}")
            choice = int(input("Kies een bestand (nummer): ")) - 1
            xml_file_name = xml_files[choice]
        else:
            xml_file_name = xml_files[0]

        print(f"Verwerken: {xml_file_name}")

        tag_counts = defaultdict(int)

        with z.open(xml_file_name) as f:
            try:
                tag_counts = count_tags_in_xml(f)
                if tag_counts:
                    write_tag_counts_to_file(tag_counts, output_file)
                    print(f"✅ Tag tellingen zijn geschreven naar {output_file}")
                else:
                    print("⚠️  Geen tags gevonden. Controleer of het XML-bestand correct is.")
            except ET.ParseError as e:
                print(f"❌  XML-verwerking mislukt: {e}")

if __name__ == "__main__":
    main()

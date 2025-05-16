import xml.etree.ElementTree as ET
import os
import sys

def split_xml_in_four_parts(input_file, output_base, tag_to_split):
    print("Voorbereiding... Tellen van elementen.")

    # Stap 1: aantal records tellen
    total = 0
    for event, elem in ET.iterparse(input_file, events=("end",)):
        if elem.tag == tag_to_split:
            total += 1
        elem.clear()

    if total == 0:
        print(f"Geen <{tag_to_split}> elementen gevonden.")
        return

    print(f"Totaal aantal <{tag_to_split}> elementen: {total}")
    split_size = total // 4

    # Stap 2: splitsen op basis van telling
    print("Start met splitsen...")
    context = ET.iterparse(input_file, events=("start", "end"))
    _, root = next(context)

    current_part = 1
    count = 0
    written = 0

    def open_writer(part_number):
        path = f"{output_base}-{part_number}.xml"
        f = open(path, "wb")
        f.write(b'<?xml version="1.0"?>\n<root>\n')
        return f, path

    out_file, current_path = open_writer(current_part)

    for event, elem in context:
        if event == "end" and elem.tag == tag_to_split:
            out_file.write(ET.tostring(elem, encoding="utf-8"))
            count += 1
            written += 1

            if written % 1000 == 0:
                print(f"{written}/{total} verwerkt...")

            # Nieuwe file starten
            if written >= split_size * current_part and current_part < 4:
                out_file.write(b'</root>')
                out_file.close()
                print(f"Deel {current_part} opgeslagen: {current_path}")
                current_part += 1
                out_file, current_path = open_writer(current_part)

            elem.clear()
            root.clear()

    # Sluit laatste bestand af
    out_file.write(b'</root>')
    out_file.close()
    print(f"Deel {current_part} opgeslagen: {current_path}")
    print("Splitsen voltooid.")

if __name__ == "__main__":
    input_file = input("Input XML-bestand: ").strip()
    if not os.path.exists(input_file):
        print("Bestand niet gevonden.")
        sys.exit(1)

    output_base = input("Output-bestandsbasis (zonder .xml): ").strip()
    tag = input("Splits op XML-element (bijv. record): ").strip()

    split_xml_in_four_parts(input_file, output_base, tag)

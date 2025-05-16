import xml.etree.ElementTree as ET
from collections import defaultdict
import gzip
import os
from tqdm import tqdm

def count_tags_in_xml(xml_file):
    tag_counts = defaultdict(int)
    for event, elem in ET.iterparse(xml_file, events=('start', 'end')):
        if event == 'start':
            tag_counts[elem.tag] += 1
        elem.clear()
    return tag_counts

def write_tag_counts_to_file(tag_counts, output_file):
    with open(output_file, 'w') as f:
        for tag, count in tag_counts.items():
            f.write(f'{tag}: {count}\n')

def main():
    xml_file = input("Voer de naam van het gz-gecomprimeerde XML-bestand in: ")
    output_file = input("Voer de naam van het uitvoerbestand in: ")

    # Bereken de totale grootte van het bestand voor de voortgangsindicator
    total_size = os.path.getsize(xml_file)

    tag_counts = defaultdict(int)

    with gzip.open(xml_file, 'rt', encoding='utf-8') as f:
        context = ET.iterparse(f, events=('start', 'end'))
        context = iter(context)

        for event, elem in tqdm(context, total=total_size, unit='B', unit_scale=True, desc="Processing XML"):
            if event == 'start':
                tag_counts[elem.tag] += 1
            elem.clear()

    write_tag_counts_to_file(tag_counts, output_file)
    print(f"Tag tellingen zijn geschreven naar {output_file}")

if __name__ == "__main__":
    main()

import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm

def fetch_oai_data():
    base_url = "https://adlib.catharijneconvent.nl/oaix/oai.ashx"
    params = {
        "verb": "ListRecords",
        "metadataPrefix": "oai_dc"
    }

    output_file = "cath_monica_records.xml"
    all_records = []
    resumption_token = None
    total_records = 74053  # Totaal aantal records voor voortgangsindicator

    print("Records ophalen...")

    with tqdm(total=total_records, desc="Vooruitgang", unit="records") as pbar:
        while True:
            try:
                # Voeg de resumptionToken toe als deze aanwezig is
                if resumption_token:
                    params = {
                        "verb": "ListRecords",
                        "resumptionToken": resumption_token
                    }

                response = requests.get(base_url, params=params, timeout=30)

                if response.status_code != 200:
                    print(f"Fout bij ophalen gegevens: {response.status_code}")
                    break

                # Parse de XML-respons
                root = ET.fromstring(response.content)
                records = root.findall(".//{http://www.openarchives.org/OAI/2.0/}record")
                all_records.extend(records)

                # Update voortgangsindicator
                pbar.update(len(records))

                # Controleer op een resumptionToken
                resumption_element = root.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
                if resumption_element is not None and resumption_element.text:
                    resumption_token = resumption_element.text
                else:
                    break

            except requests.exceptions.Timeout:
                print("Verzoek timeout. Probeer later opnieuw.")
                break
            except requests.exceptions.RequestException as e:
                print(f"Netwerkfout: {e}")
                break
            except ET.ParseError as e:
                print(f"Fout bij het verwerken van XML: {e}")
                break

    # Maak een XML-bestand voor de verzamelde records
    if all_records:
        root = ET.Element("OAI_PMH_Records")
        for record in all_records:
            root.append(record)

        tree = ET.ElementTree(root)
        try:
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            print(f"Gegevens opgeslagen in {output_file}")
        except IOError as e:
            print(f"Fout bij het opslaan van gegevens: {e}")
    else:
        print("Geen records opgehaald.")

if __name__ == "__main__":
    fetch_oai_data()

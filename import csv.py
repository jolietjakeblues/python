import csv
import requests
from xml.etree import ElementTree as ET
from tqdm import tqdm

def download_and_combine_rdf(input_csv_path, output_rdf_path):
    # Create a new RDF/XML root element
    rdf_root = ET.Element("rdf:RDF", xmlns="http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    # Read the URLs from the CSV
    urls = []
    with open(input_csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip header if there's one
        urls = [row[0] for row in reader]
    
    for url in tqdm(urls, desc="Downloading and combining RDF/XML data", unit="url"):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the RDF/XML from the response
            tree = ET.fromstring(response.content)
            
            # Append the elements from the fetched RDF/XML to our root element
            for elem in tree:
                rdf_root.append(elem)
                
        except requests.RequestException as e:
            print(f"\nFailed to fetch RDF/XML from {url}. Error: {e}")

    # Save the combined RDF/XML to a file
    with open(output_rdf_path, 'wb') as output_file:
        output_file.write(ET.tostring(rdf_root))

if __name__ == "__main__":
    download_and_combine_rdf("zzm.csv", "combined.rdf")

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def fetch_records(url, file):
    try:
        response = requests.get(url, timeout=30)  # Increase the timeout to 30 seconds (or adjust as needed)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            records = soup.find_all('record')
            next_resumption_token = soup.find('resumptionToken').text if soup.find('resumptionToken') else None
            write_to_xml(records, file)  # Write records to XML file
            return next_resumption_token
        else:
            print("Failed to fetch records from:", url)
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching records:", e)
        return None

def download_all_records(base_url, filename, resumption_token=None):
    while True:
        if resumption_token:
            url = f"{base_url}&resumptionToken={resumption_token}"
        else:
            url = base_url
        
        resumption_token = fetch_records(url, filename)
        if not resumption_token:
            break

def write_to_xml(records, filename):
    with open(filename, 'a', encoding='utf-8') as f:  # Open file in append mode with UTF-8 encoding
        for record in records:
            f.write(str(record))
            f.write('\n')

base_url = "https://rce.adlibhosting.com/oaiapi/oai.ashx?verb=ListRecords&set=archrep&metadataPrefix=oai_datacite"
xml_filename = "archrep_1.xml"
print("Downloading and writing records...")
download_all_records(base_url, xml_filename)
print("Data written to", xml_filename)

import requests
import csv

def get_data(nummer):
    url = "https://webservices.picturae.com/mediabank/media?apiKey=50cc410d-09d5-4874-ad11-edf41a0e8064&lang=nl&fq[]=search_s_priref:%20" + str(nummer)
    response = requests.get(url)
    data = response.json()

    if 'media' not in data or not data['media']:
        print(f"Er is een fout opgetreden bij het ophalen van de gegevens voor nummer {nummer}: {data}")
        return None

    media = data['media'][0]

    if 'asset' not in media or not media['asset']:
        print(f"No assets found for nummer {nummer}")
        return None

    uuid = media['asset'][0]['uuid']
    id = media['id']
    thumb_large = media['asset'][0]['thumb']['large']

    return [nummer, id, uuid, thumb_large]

def write_to_csv(data):
    if data is not None:
        with open('picturae_def3.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(data)

def main():
    with open('picturae_run3.csv', 'r') as file:
        nummers = file.readlines()

    for nummer in nummers:
        data = get_data(nummer.strip())
        write_to_csv(data)

if __name__ == "__main__":
    main()

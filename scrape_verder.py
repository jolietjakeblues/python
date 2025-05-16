import requests

def extract_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Probeer JSON-gegevens te vinden binnen script-tags
        json_start = response.text.find('<script type="application/ld+json">')
        if json_start != -1:
            json_start += len('<script type="application/ld+json">')
            json_end = response.text.find('</script>', json_start)
            json_data = response.text[json_start:json_end]
            return json_data
        else:
            print("JSON-gegevens niet gevonden op de pagina:", url)
            return None
    else:
        print("Fout bij het ophalen van de pagina:", url)
        return None

def process_urls(input_file, output_file):
    with open(input_file, 'r') as f:
        urls = f.readlines()

    with open(output_file, 'w') as f_out:
        f_out.write("URL\tJSON Data\n")
        for url in urls:
            url = url.strip()  # verwijder eventuele nieuwe regel tekens
            
            # De URL moet correct worden geformatteerd voordat er een verzoek naar wordt gedaan
            url = url.replace(' ', '')  # Verwijder spaties
            
            json_data = extract_json_data(url)
            if json_data:
                f_out.write(f"{url}\t{json_data}\n")
            else:
                f_out.write(f"{url}\tGeen JSON-gegevens gevonden\n")
            f_out.flush()  # Forceer schrijven naar het bestand om de voortgang bij te werken

if __name__ == "__main__":
    input_file = input("Geef het pad naar het bestand met URLs op: ")
    output_file = input("Geef het pad naar het uitvoerbestand op: ")

    process_urls(input_file, output_file)

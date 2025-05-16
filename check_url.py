import pandas as pd
import aiohttp
import asyncio
from tqdm import tqdm

# Functie om een enkele URL te controleren
async def check_url(session, url):
    try:
        async with session.head(url, allow_redirects=True, timeout=5) as response:
            if response.status == 200:
                return "Ja", ""
            else:
                return "Nee", f"Status code: {response.status}"
    except Exception as e:
        return "Nee", str(e)

# Asynchrone functie om alle URL's te controleren
async def check_all_urls(rows):
    results = []
    async with aiohttp.ClientSession() as session:
        for row in tqdm(rows, desc="URLs controleren"):
            url = row['concept']
            resolvable, error_message = await check_url(session, url)
            # Voeg ook prefLabel en matchType toe aan de resultaten, met foutafhandeling
            results.append([url, row.get('prefLabel', ''), row.get('matchType', ''), resolvable, error_message])
    return results

# Lees URL's uit CSV-bestand
def read_urls_from_csv(csv_file):
    df = pd.read_csv(csv_file, sep=";")
    df.columns = df.columns.str.strip().str.lower()  # Normaliseer kolomnamen: verwijder spaties en zet alles naar lowercase
    print(df.columns)  # Controleer de kolomnamen
    return df

# Schrijf resultaten naar een nieuwe CSV
def write_results_to_csv(results, output_file):
    results_df = pd.DataFrame(results, columns=["concept", "prefLabel", "matchType", "resolveerbaar", "foutmelding"])
    results_df.to_csv(output_file, index=False)

# Hoofdscript
def main(input_csv, output_csv):
    # Lees URL's in
    urls_df = read_urls_from_csv(input_csv)
    
    # Zet de DataFrame-rijen om naar een lijst van dictionaries
    rows = urls_df.to_dict(orient='records')

    # Voer de asynchrone URL-check uit
    results = asyncio.run(check_all_urls(rows))

    # Schrijf resultaten naar een CSV-bestand
    write_results_to_csv(results, output_csv)
    print(f"Resultaten opgeslagen in {output_csv}")

# Geef het pad naar je invoer- en uitvoer-CSV-bestanden op
input_csv = 'input_urls_cht2.csv'  # Verander dit naar je eigen CSV-bestand met URL's
output_csv = 'output_results_cht_2.csv'  # Hierin worden de resultaten opgeslagen

# Start het script
if __name__ == "__main__":
    main(input_csv, output_csv)

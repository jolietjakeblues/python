import pandas as pd
import aiohttp
import asyncio
from tqdm import tqdm

async def check_url(session, url):
    try:
        async with session.head(url, allow_redirects=True, timeout=5) as response:
            if response.status == 200:
                return "Ja", ""
            else:
                return "Nee", f"Status code: {response.status}"
    except Exception as e:
        return "Nee", str(e)

async def check_all_urls(key_url_pairs):
    results = []
    async with aiohttp.ClientSession() as session:
        for key, url in tqdm(key_url_pairs, desc="URLs controleren"):
            resolvable, error_message = await check_url(session, url)
            results.append([key, url, resolvable, error_message])
    return results

def read_csv_pairs(csv_file, key_col, url_col):
    # 1. Lees het ruwe header-gedeelte om te zien hoe het gesplitst wordt:
    with open(csv_file, "r", encoding="utf-8-sig") as f:
        first_line = f.readline().rstrip('\n')
        print("\n--- Debug: eerste regel uit CSV ---")
        print(first_line)
        print("--- Einde debug ---\n")

    # 2. Lees de CSV met een vaste scheidingsteken-instelling.
    #    Zet sep=";" als uw bestand puntkomma's gebruikt.
    df = pd.read_csv(csv_file, sep=",", encoding="utf-8-sig")

    # 3. Kolomnamen normaliseren.
    #    Verwijder spaties en zet naar lowercase, zodat 'hg_IN geoN' -> 'hg_ingeon'.
    df.columns = [col.strip().lower().replace(" ", "") for col in df.columns]

    print("Beschikbare kolomnamen (genormaliseerd):")
    for c in df.columns:
        print("-", c)

    # 4. Normaliseer de opgegeven kolomnamen.
    norm_key = key_col.strip().lower().replace(" ", "")
    norm_url = url_col.strip().lower().replace(" ", "")

    if norm_key not in df.columns:
        raise ValueError(f"Kolom '{key_col}' (genormaliseerd '{norm_key}') niet gevonden in de CSV.")
    if norm_url not in df.columns:
        raise ValueError(f"Kolom '{url_col}' (genormaliseerd '{norm_url}') niet gevonden in de CSV.")

    # 5. Bouw paren (key, url).
    #    We laten alleen rijen staan waar de url-kolom niet leeg is.
    pairs = df[[norm_key, norm_url]].dropna(subset=[norm_url]).values.tolist()
    return pairs

def write_results_to_csv(results, output_file):
    df = pd.DataFrame(results, columns=["objectnummer", "url", "resolveerbaar", "foutmelding"])
    df.to_csv(output_file, index=False)
    print(f"Resultaten opgeslagen in {output_file}")

def main():
    csv_file = input("Voer de naam van het CSV-bestand in: ")
    key_column = input("Voer de naam van de kolom met het objectnummer (of key) in: ")
    url_column = input("Voer de naam van de kolom met de URL in: ")
    output_csv = input("Voer de naam van het uitvoer-CSV-bestand in: ")

    pairs = read_csv_pairs(csv_file, key_column, url_column)
    results = asyncio.run(check_all_urls(pairs))
    write_results_to_csv(results, output_csv)

if __name__ == "__main__":
    main()

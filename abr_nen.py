import spacy
import pandas as pd
import os
import re
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import logging
import time
import subprocess
import requests

# --- Setup ---
try:
    import importlib.util
    model_name = "nl_core_news_md" if importlib.util.find_spec("nl_core_news_md") else "nl_core_news_sm"
except Exception:
    model_name = "nl_core_news_sm"

try:
    nlp = spacy.load(model_name)
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
    nlp = spacy.load(model_name)

log_filename = f"verwerkingslog_{int(time.time())}.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

SAMENSTELLINGEN = [("begin", "jaartelling"), ("eerste", "wereldoorlog"), ("tweede", "kamer")]

def herstel_samenstellingen(nomenlijst):
    woorden = nomenlijst.split("|")
    i, resultaat = 0, []
    while i < len(woorden):
        if i < len(woorden) - 1 and (woorden[i], woorden[i + 1]) in SAMENSTELLINGEN:
            resultaat.append(f"{woorden[i]} {woorden[i + 1]}")
            i += 2
        else:
            resultaat.append(woorden[i])
            i += 1
    return "|".join(resultaat)

def unieke_bestandsnaam(pad):
    if not os.path.exists(pad): return pad
    base, ext = os.path.splitext(pad)
    for i in range(1, 1000):
        nieuw = f"{base}-{i}{ext}"
        if not os.path.exists(nieuw): return nieuw
    return pad

def vind_romeinse_eeuwen(tekst):
    matches = re.findall(r"\b([IVXLCDM]+)-eeuw\b", tekst)
    return [f"{m}-eeuw".lower() for m in matches]

def check_term_in_thesaurus(term):
    term = term.strip().lower()
    url = f"https://api.linkeddata.cultureelerfgoed.nl/queries/thesauri/zoek-naar-abr-termen/run?zoekterm={term}"
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            for r in results:
                uri = r.get("concept")
                if uri:
                    return uri
    except Exception as e:
        logging.error(f"API-fout voor term '{term}': {e}")
    logging.info(f"Geen match in thesaurus voor: {term}")
    return ""

def select_input_file():
    root = tk.Tk(); root.withdraw()
    return filedialog.askopenfilename(title="Selecteer bestand", filetypes=[("CSV/Excel", "*.csv *.tsv *.xlsx")])

def main():
    input_file = select_input_file()
    if not input_file: print("Geen bestand geselecteerd."); return
    ext = os.path.splitext(input_file)[1].lower()
    sep, df = None, None

    if ext in [".csv", ".tsv"]:
        sep = input("Scheidingsteken (',' of ';' of '|' of '\t') [druk op Enter]: ").strip() or ','
        df = pd.read_csv(input_file, encoding="utf-8", sep=sep, on_bad_lines='skip')
    elif ext == ".xlsx":
        df = pd.read_excel(input_file, engine="openpyxl")
    else:
        print("Bestandstype niet ondersteund."); return

    print("\nKolommen:")
    for i, col in enumerate(df.columns): print(f"[{i}] {col}")
    print(df.head(2).to_string(index=False))

    try:
        col_index = int(input("\nKies kolomnummer [druk op Enter]: ").strip())
        column_name = df.columns[col_index]
    except: print("Ongeldig."); return

    output_column = input("Naam voor outputkolom? [druk op Enter]: ").strip()
    if not output_column: print("Geen naam."); return

    include_entities = input("Entiteiten meenemen? (ja/nee) [druk op Enter]: ").strip().lower() == "ja"
    lowercase = input("Omzetten naar kleine letters? (ja/nee) [druk op Enter]: ").strip().lower() == "ja"
    sort_output = input("Alfabetisch sorteren? (ja/nee) [druk op Enter]: ").strip().lower() == "ja"
    extra_terms_input = input("Extra termen handmatig toevoegen (gescheiden door komma)? [druk op Enter]: ").strip()
    extra_terms = [t.strip().lower() for t in extra_terms_input.split(",") if t.strip()]

    start_time = time.time()
    print("\nVerwerken gestart...")

    texts = df[column_name].astype(str).str.lower() if lowercase else df[column_name].astype(str)
    texts = texts.str.replace(r'[\"“”.,]', '', regex=True).str.replace(r'\s+', ' ', regex=True).tolist()

    results, uri_results = [], []
    unieke_termen = set()

    for doc, raw_text in zip(tqdm(nlp.pipe(texts, batch_size=50), total=len(texts)), texts):
        try:
            terms = [t.text.lower() for t in doc if t.pos_ == "NOUN"]
            if include_entities:
                terms += [e.text.lower() for e in doc.ents if e.label_ in {"LOC", "GPE", "ORG", "MISC"}]
            terms += vind_romeinse_eeuwen(raw_text)
            terms += [et for et in extra_terms if et in raw_text]
            terms = [t for t in terms if len(t.strip()) > 1]
            terms = list(dict.fromkeys(terms))
            if sort_output: terms = sorted(terms)
            termen_str = herstel_samenstellingen("|".join(terms))
            results.append(termen_str)
            unieke_termen.update(terms)
        except Exception as e:
            logging.error(f"Fout bij tekst: {raw_text[:30]}... - {e}")
            results.append("")
            continue

    print("Zoeken naar thesaurus-URI's...")
    term2uri = {term: check_term_in_thesaurus(term) for term in tqdm(unieke_termen)}
    for lijn in results:
        termen = lijn.split("|")
        uris = [term2uri.get(t, "") for t in termen if term2uri.get(t)]
        uri_results.append("|".join(uris))

    df[output_column] = results
    df["thesaurus_uris"] = uri_results

    input_dir = os.path.dirname(input_file)
    input_name = os.path.splitext(os.path.basename(input_file))[0]
    output_ext = ".xlsx" if ext == ".xlsx" else ".csv"
    output_file = unieke_bestandsnaam(os.path.join(input_dir, f"{input_name}_output{output_ext}"))

    try:
        if output_ext == ".xlsx":
            df.to_excel(output_file, index=False)
        else:
            df.to_csv(output_file, encoding="utf-8", index=False, sep=sep or ',')
        print(f"\nBestand opgeslagen als: {output_file}")
    except Exception as e:
        print(f"Fout bij opslaan: {e}")
        logging.error(f"Opslaan mislukt: {e}")

    print(f"\n--- Verwerking voltooid ---\nRijen: {len(df)}\nDuur: {round(time.time() - start_time, 1)} s\nLog: {log_filename}")

if __name__ == "__main__":
    main()

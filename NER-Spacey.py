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

SAMENSTELLINGEN = [
    ("begin", "jaartelling"),
    ("eerste", "wereldoorlog"),
    ("tweede", "kamer"),
    ("koninklijk", "huis"),
    ("oude", "rijksdaggebouw"),
]

DOMEINTERMEN = {"wierde", "terp", "waterput", "kerkheuvel", "urnenveld", "huisterp", "dorpswierde", "borg"}

def herstel_samenstellingen(nomenlijst):
    woorden = nomenlijst.split("|")
    i = 0
    resultaat = []
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

def vind_romeinse_eeuwen_en_jaartallen(tekst):
    tekst = tekst.lower()
    losse_eeuwen = re.findall(r"\b\d{1,2}e eeuw\b", tekst)
    samengestelde_eeuwen = re.findall(r"\b\d{1,2}e\s*[-–]\s*\d{1,2}e eeuw\b", tekst)
    jaartallen = re.findall(r"\b\d{3,4}(?:\s*[-–]\s*\d{3,4})?\b", tekst)
    return losse_eeuwen + samengestelde_eeuwen + jaartallen

def select_input_file():
    root = tk.Tk(); root.withdraw()
    return filedialog.askopenfilename(title="Selecteer bestand", filetypes=[("CSV/Excel", "*.csv *.tsv *.xlsx")])

def main():
    input_file = select_input_file()
    if not input_file: print("Geen bestand geselecteerd."); return
    ext = os.path.splitext(input_file)[1].lower()
    sep, df = None, None

    if ext in [".csv", ".tsv"]:
        sep = input("Wat is het scheidingsteken tussen de kolommen? (bijv. ',' of ';' of '|' of '\t')\nLaat leeg voor ',': ").strip() or ','
        df = pd.read_csv(input_file, encoding="utf-8", sep=sep, on_bad_lines='skip')
    elif ext == ".xlsx":
        df = pd.read_excel(input_file, engine="openpyxl")
    else:
        print("Bestandstype niet ondersteund."); return

    print("\nKolommen in uw bestand:")
    for i, col in enumerate(df.columns): print(f"[{i}] {col}")
    print(df.head(2).to_string(index=False))

    try:
        col_index = int(input("\nKies het nummer van de kolom die u wilt analyseren:\n(typ alleen het cijfer en druk op Enter): ").strip())
        column_name = df.columns[col_index]
    except: print("Ongeldige kolomkeuze. Script wordt gestopt."); return

    output_column = input("Hoe moet de nieuwe kolom met resultaten heten?\n(bijvoorbeeld 'ner_archeologie') [druk op Enter]: ").strip()
    if not output_column:
        print("Geen naam opgegeven. Script wordt gestopt.")
        return

    include_entities = input("Wilt u ook entiteiten zoals plaatsnamen en objecten meenemen?\nTyp 'ja' of 'nee' [druk op Enter]: ").strip().lower() == "ja"
    lowercase = input("Wilt u alle termen omzetten naar kleine letters?\nTyp 'ja' of 'nee' [druk op Enter]: ").strip().lower() == "ja"
    sort_output = input("Wilt u de termen alfabetisch sorteren in de output?\nTyp 'ja' of 'nee' [druk op Enter]: ").strip().lower() == "ja"

    start_time = time.time()
    print("\nVerwerken gestart...")

    texts = df[column_name].astype(str)
    if lowercase:
        texts = texts.str.lower()
    texts = texts.str.replace(r'["“”.,;:!?]', '', regex=True).str.strip().str.replace(r'\s+', ' ', regex=True).tolist()

    results = []
    for doc, raw_text in zip(tqdm(nlp.pipe(texts, batch_size=50), total=len(texts)), texts):
        try:
            terms = [t.text.lower().strip() for t in doc if t.pos_ in {"NOUN", "PROPN"}]
            if include_entities:
                terms += [e.text.lower().strip() for e in doc.ents if e.label_ in {"LOC", "GPE", "ORG", "MISC"}]
            terms += vind_romeinse_eeuwen_en_jaartallen(raw_text)
            for term in DOMEINTERMEN:
                if term in raw_text.lower():
                    terms.append(term)
            terms = [t for t in terms if len(t.strip()) > 1]
            terms = list(dict.fromkeys(terms))
            terms = [t for t in terms if len(t) > 2 and not re.fullmatch(r"\d{1,2}|\w{1,2}", t)]
            if sort_output: terms = sorted(terms)
            termen_str = herstel_samenstellingen("|".join(terms))
            results.append(termen_str)
        except Exception as e:
            logging.error(f"Fout bij tekst: {raw_text[:30]}... - {e}")
            results.append("")
            continue

    df[output_column] = results

    # Opslaan: gebruiker kiest bestandsnaam of accepteert default
    save_choice = input("Wilt u zelf de bestandsnaam en type opgeven? Typ 'ja' of druk op Enter voor automatisch opslaan: ").strip().lower()
    if save_choice == 'ja':
        filename = input("Voer een bestandsnaam in zonder extensie (bijv. 'resultaten'): ").strip()
        filetype = input("Kies formaat: 'csv' of 'xlsx': ").strip().lower()
        if filetype not in ['csv', 'xlsx']:
            print("Ongeldig formaat. Script wordt gestopt.")
            return
        output_ext = f".{filetype}"
        output_file = unieke_bestandsnaam(os.path.join(os.path.dirname(input_file), f"{filename}{output_ext}"))
    else:
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

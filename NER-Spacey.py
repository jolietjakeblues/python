import spacy
import pandas as pd
import csv
import os
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import logging
import time
import subprocess

# Automatically choose best available SpaCy model
try:
    import importlib.util
    if importlib.util.find_spec("nl_core_news_md"):
        model_name = "nl_core_news_md"
    else:
        model_name = "nl_core_news_sm"
except Exception:
    model_name = "nl_core_news_sm"

# Load Dutch language model with fallback and auto-install if missing
try:
    nlp = spacy.load(model_name)
except OSError:
    print(f"Model '{model_name}' niet gevonden. Installatie wordt gestart...")
    try:
        subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
        nlp = spacy.load(model_name)
        print(f"Model '{model_name}' is succesvol geïnstalleerd en geladen.")
    except Exception as install_error:
        print(f"Automatische installatie mislukt: {install_error}")
        exit()

# Setup logging
log_filename = f"verwerkingslog_{int(time.time())}.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Extract nouns and optionally entities; remove duplicates
def extract_nouns(text, include_entities=False, lowercase=False, sort_result=False):
    try:
        doc = nlp(text)
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        if include_entities:
            entities = [ent.text for ent in doc.ents if ent.label_ in {"LOC", "GPE", "ORG", "MISC"}]
            nouns.extend(entities)
        if lowercase:
            nouns = [n.lower() for n in nouns]
        unique_nouns = list(dict.fromkeys(nouns))  # preserve order
        if sort_result:
            unique_nouns = sorted(unique_nouns)
        return "|".join(unique_nouns)
    except Exception as e:
        logging.error(f"Fout bij verwerken tekst: '{text[:30]}...' - {e}")
        return ""

# Select input file via GUI
def select_input_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecteer bestand", filetypes=[("Ondersteunde bestanden", "*.csv *.tsv *.xlsx")])
    return file_path

def main():
    print("Selecteer het inputbestand (.csv, .tsv of .xlsx)...")
    input_file = select_input_file()

    if not input_file:
        print("Geen bestand geselecteerd. Script wordt gestopt.")
        return

    ext = os.path.splitext(input_file)[1].lower()
    if ext == ".csv" or ext == ".tsv":
        sep_input = input("Wat is het scheidingsteken tussen de kolommen? (bijv. ',' of ';' of '|' of '\\t'): ").strip()
        sep = sep_input if sep_input else ','
        try:
            df = pd.read_csv(input_file, encoding="utf-8", sep=sep, on_bad_lines='skip')
        except Exception as e:
            print(f"Fout bij lezen van het bestand: {e}")
            return
    elif ext == ".xlsx":
        try:
            df = pd.read_excel(input_file, engine="openpyxl")
            sep = None  # not needed for Excel
        except Exception as e:
            print(f"Fout bij lezen van het Excel-bestand: {e}")
            return
    else:
        print("Bestandstype niet ondersteund.")
        return

    print("\nKolommen gevonden:")
    for i, col in enumerate(df.columns):
        print(f"[{i}] {col}")

    print("\nVoorbeeld (eerste 2 rijen):")
    print(df.head(2).to_string(index=False))

    try:
        col_index = int(input("\nKies het nummer van de kolom die u wilt analyseren: ").strip())
        column_name = df.columns[col_index]
    except:
        print("Ongeldige kolomkeuze. Script wordt gestopt.")
        return

    output_column = input("Hoe moet de outputkolom heten (bijv. 'Namenwoorden')? ").strip()
    if not output_column:
        print("Geen naam opgegeven. Script wordt gestopt.")
        return

    include_entities = input("Wilt u ook entiteiten zoals plaatsnamen en objecten meenemen? (ja/nee): ").strip().lower() == "ja"
    lowercase = input("Wilt u de termen omzetten naar kleine letters? (ja/nee): ").strip().lower() == "ja"
    sort_output = input("Wilt u de termen alfabetisch sorteren? (ja/nee): ").strip().lower() == "ja"

    start_time = time.time()
    errors = 0

    print("\nVerwerken gestart...")
    results = []
    texts = df[column_name].astype(str).tolist()
    for doc, text in zip(tqdm(nlp.pipe(texts, batch_size=50), total=len(texts)), texts):
        try:
            nouns = [token.text for token in doc if token.pos_ == "NOUN"]
            if include_entities:
                entities = [ent.text for ent in doc.ents if ent.label_ in {"LOC", "GPE", "ORG", "MISC"}]
                nouns.extend(entities)
            if lowercase:
                nouns = [n.lower() for n in nouns]
            unique_nouns = list(dict.fromkeys(nouns))
            if sort_output:
                unique_nouns = sorted(unique_nouns)
            results.append("|".join(unique_nouns))
        except Exception as e:
            logging.error(f"Fout bij verwerken tekst: '{text[:30]}...' - {e}")
            results.append("")
            errors += 1

    df[output_column] = results

    output_file = input("\nGeef de bestandsnaam voor de output (bijv. output.csv of output.xlsx): ").strip()
    if not output_file:
        print("Geen bestandsnaam opgegeven. Script wordt gestopt.")
        return

    try:
        if output_file.endswith(".xlsx"):
            df.to_excel(output_file, index=False)
        else:
            df.to_csv(output_file, encoding="utf-8", index=False, sep=sep if sep else ',')
        print(f"\nBestand opgeslagen als: {output_file}")
    except Exception as e:
        print(f"Fout bij opslaan van het bestand: {e}")
        logging.error(f"Fout bij opslaan bestand: {e}")

    duration = time.time() - start_time
    rapport = f"""
--- Verwerking voltooid ---
Bestand: {input_file}
Model: {model_name}
Kolom verwerkt: {column_name}
Nieuwe kolom: {output_column}
Rijen verwerkt: {len(df)}
Fouten tijdens verwerking: {errors}
Totale duur: {round(duration, 2)} seconden
Logbestand: {log_filename}
    """
    print(rapport)
    with open("rapport.txt", "w", encoding="utf-8") as f:
        f.write(rapport)

if __name__ == "__main__":
    main()

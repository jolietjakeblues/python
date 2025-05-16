import spacy
import pandas as pd
import csv
import os

# Laad het Nederlandse taalmodel
try:
    nlp = spacy.load("nl_core_news_sm")
except OSError:
    print("Het taalmodel 'nl_core_news_sm' is niet geïnstalleerd. Installeer het met: python -m spacy download nl_core_news_sm")
    exit()

def extract_nouns(text):
    doc = nlp(text)
    return "|".join([token.text for token in doc if token.pos_ == "NOUN"])

def main():
    # Vraag om gebruikersinput
    input_file = input("Geef de naam van het inputbestand (met extensie): ").strip()
    if not input_file:
        print("Fout: De naam van het inputbestand mag niet leeg zijn.")
        return

    output_file = input("Geef de naam van het outputbestand (met extensie): ").strip()
    if not output_file:
        print("Fout: De naam van het outputbestand mag niet leeg zijn.")
        return

    column_name = input("Geef de naam van de kolom waaruit zelfstandige naamwoorden moeten worden geëxtraheerd: ").strip()
    if not column_name:
        print("Fout: De kolomnaam mag niet leeg zijn.")
        return

    # Controleer of het inputbestand bestaat
    if not os.path.exists(input_file):
        print(f"Fout: Het bestand '{input_file}' bestaat niet.")
        return

    # Lees het CSV-bestand
    try:
        df = pd.read_csv(input_file, encoding="utf-8", sep='|', on_bad_lines='skip')
    except Exception as e:
        print(f"Fout bij het lezen van het bestand: {e}")
        return

    # Check of de kolom bestaat
    if column_name not in df.columns:
        print(f"Fout: Kolom '{column_name}' niet gevonden in het bestand.")
        return

    total_rows = len(df)
    print(f"Verwerken van {total_rows} rijen...")

    # Voeg een nieuwe kolom toe voor zelfstandige naamwoorden
    try:
        df['Zelfstandige Naamwoorden'] = df[column_name].apply(lambda x: extract_nouns(str(x)))
    except Exception as e:
        print(f"Fout tijdens het verwerken van de kolom: {e}")
        return

    # Controleer of het outputbestand al bestaat
    if os.path.exists(output_file):
        overwrite = input(f"Het bestand '{output_file}' bestaat al. Wilt u het overschrijven? (ja/nee): ").strip().lower()
        if overwrite != 'ja':
            print("Het proces is geannuleerd. Bestand is niet overschreven.")
            return

    # Opslaan naar het nieuwe bestand
    try:
        df.to_csv(output_file, encoding="utf-8", index=False, sep='|')
        print(f"Verwerking voltooid. Resultaten opgeslagen in {output_file}.")
    except Exception as e:
        print(f"Fout bij het opslaan van het bestand: {e}")

if __name__ == "__main__":
    main()

import spacy
import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the Dutch language model
nlp = spacy.load("nl_core_news_sm")

def extract_names(text, names):
    doc = nlp(text)
    extracted_names = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            extracted_name = ent.text
            # Use fuzzy matching to find the closest matching name in the list
            best_match = process.extractOne(extracted_name, names, scorer=fuzz.ratio)
            if best_match[1] >= 80:  # Adjust the threshold as needed
                extracted_names.append(best_match[0])

    return "|".join(extracted_names)

def main():
    # Prompt for user input
    input_file = input("Enter the name of the input file (e.g., maastricht.csv): ")
    names_file = input("Enter the name of the file containing names to be recognized (e.g., namen.csv): ")
    output_file = "Maastricht_SpaCy_Names.csv"

    # Load the CSV files
    df = pd.read_csv(input_file, encoding="utf-8")
    names_df = pd.read_csv(names_file)

    names = names_df["namen"].tolist()

    total_rows = len(df)
    print(f"Processing {total_rows} rows...")

    with tqdm(total=total_rows) as pbar:
        def update_progress(*_):
            pbar.update(1)

        df['Extracted Names'] = df["omschrijving"].apply(lambda x: extract_names(x, names))
        df["Extracted Names"] = df["Extracted Names"].apply(lambda x: x if x else None)
        df["Text"] = df["omschrijving"].apply(lambda x: x if x else None)
        df["Index"] = df.index + 1  # Add an index column

        # Save the results to the new file
        df.to_csv(output_file, encoding="utf-8", index=False)

    print(f"Processing complete. Results saved in {output_file}.")

if __name__ == "__main__":
    main()

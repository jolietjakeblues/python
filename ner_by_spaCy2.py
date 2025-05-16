import spacy
import pandas as pd
from tqdm import tqdm

# Load the English language model
nlp = spacy.load("nl_core_news_sm")

def extract_named_entities(text):
    doc = nlp(text)
    people = []
    locations = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.append(ent.text)
        elif ent.label_ == "GPE":
            locations.append(ent.text)

    return "|".join(people), "|".join(locations)

def main():
    # Prompt for user input
    input_file = input("Enter the name of the input file (with extension): ")
    output_file = input("Enter the name of the output file (with extension): ")
    column_name = input("Enter the name of the column containing text data: ")

    # Load the CSV file
    df = pd.read_csv(input_file, encoding="utf-8")

    # Check if the specified column exists
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in the file.")
        return

    total_rows = len(df)
    print(f"Processing {total_rows} rows...")

    # Create a progress bar
    with tqdm(total=total_rows) as pbar:
        def update_progress(*_):
            pbar.update(1)

        # Add new columns for people and locations
        df['People'], df['Locations'] = zip(*df[column_name].apply(extract_named_entities))
        # Add an update to the progress bar for each row processed
        df[column_name].apply(update_progress)

    # Save the results to the new file
    df.to_csv(output_file, encoding="utf-8", index=False)

    print(f"Processing complete. Results saved in {output_file}.")

if __name__ == "__main__":
    main()

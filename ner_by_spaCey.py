import spacy
import pandas as pd

# Load the Dutch language model
nlp = spacy.load("nl_core_news_sm")

def extract_entities(text, entity_type):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ == entity_type]
    return "|".join(entities)

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

    # Add new columns for people and locations
    df['People'] = df[column_name].apply(lambda x: extract_entities(str(x), "PERSON"))
    df['Locations'] = df[column_name].apply(lambda x: extract_entities(str(x), "GPE"))

    # Save the results to the new file
    df.to_csv(output_file, encoding="utf-8", index=False)

    print(f"Processing complete. Results saved in {output_file}.")

if __name__ == "__main__":
    main()

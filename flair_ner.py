import pandas as pd
from tqdm import tqdm
from flair.data import Sentence
from flair.models import SequenceTagger

# Load the Dutch sequence tagger model from Flair
tagger = SequenceTagger.load('nl-ner')

def extract_names_and_roles(text, names, roles):
    try:
        sentence = Sentence(text)
        tagger.predict(sentence)
        extracted_names = []
        extracted_roles = []

        for entity in sentence.get_spans('ner'):
            if entity.tag == 'PER' and entity.text in names:  # Flair's tag for names
                extracted_names.append(entity.text)
            elif entity.tag == 'MISC' and entity.text in roles:  # Flair's tag for roles
                extracted_roles.append(entity.text)

        return "|".join(extracted_names), "|".join(extracted_roles)
    except Exception as e:
        return None, None

def main():
    # Prompt for user input
    input_file = input("Enter the name of the input file (e.g., maastricht.csv): ")
    names_file = input("Enter the name of the file containing names to be recognized (e.g., naamen.csv): ")
    roles_file = input("Enter the name of the file containing roles to be recognized (e.g., rol.csv): ")
    output_file = "Maastricht_Flair.csv"

    # Load the CSV files
    df = pd.read_csv(input_file, encoding="utf-8")
    names_df = pd.read_csv(names_file)
    roles_df = pd.read_csv(roles_file)

    names = names_df["namen"].tolist()
    roles = roles_df["rol"].tolist()

    total_rows = len(df)
    print(f"Processing {total_rows} rows...")

    with tqdm(total=total_rows) as pbar:
        def update_progress(*_):
            pbar.update(1)

        df['Extracted Names'], df['Roles'] = zip(*df["omschrijving"].apply(lambda x: extract_names_and_roles(x, names, roles)))
        df["Extracted Names"] = df["Extracted Names"].apply(lambda x: x if x else None)
        df["Roles"] = df["Roles"].apply(lambda x: x if x else None)
        df["Text"] = df["omschrijving"].apply(lambda x: x if x or x == '' else None)  # Handle empty strings
        df["Index"] = df.index + 1  # Add an index column

        # Save the results to the new file
        df.to_csv(output_file, encoding="utf-8", index=False)

    print(f"Processing complete. Results saved in {output_file}.")

if __name__ == "__main__":
    main()

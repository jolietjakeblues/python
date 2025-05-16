import spacy
import pandas as pd
from tqdm import tqdm

# Load the Dutch language model
nlp = spacy.load("nl_core_news_sm")

def extract_names_and_roles(text, names, roles):
    doc = nlp(text)
    extracted_names = []
    extracted_roles = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            extracted_names.append(ent.text)
        elif ent.label_ == "ROLE":
            extracted_roles.append(ent.text)

    # Filter the extracted names and roles using the provided lists
    filtered_names = [name for name in extracted_names if name in names]
    filtered_roles = [role for role in extracted_roles if role in roles]

    return "|".join(filtered_names), "|".join(filtered_roles)

def main():
    # Prompt for user input
    input_file = input("Enter the name of the input file (e.g., maastricht.csv): ")
    names_file = input("Enter the name of the file containing names to be recognized (e.g., naamen.csv): ")
    roles_file = input("Enter the name of the file containing roles to be recognized (e.g., rol.csv): ")
    output_file = "Maastricht_SpaCy.csv"

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

        df['Extracted Names'], df['rol'] = zip(*df["omschrijving"].apply(lambda x: extract_names_and_roles(x, names, roles)))
        df["Extracted Names"] = df["Extracted Names"].apply(lambda x: x if x else None)
        df["Roles"] = df["rol"].apply(lambda x: x if x else None)
        df["Text"] = df["omschrijving"].apply(lambda x: x if x else None)
        df["Index"] = df.index + 1  # Add an index column

        # Save the results to the new file
        df.to_csv(output_file, encoding="utf-8", index=False)

    print(f"Processing complete. Results saved in {output_file}.")

if __name__ == "__main__":
    main()

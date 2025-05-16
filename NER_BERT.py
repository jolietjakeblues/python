from transformers import AutoTokenizer, AutoModelForTokenClassification
import pandas as pd
from tqdm import tqdm
import torch

# Load the pre-trained Dutch BERT model fine-tuned for NER
model_name = "wietsedv/bert-base-dutch-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

def extract_names_and_roles(text):
    # Tokenize the text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Predict NER labels
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract the predicted labels
    predicted_labels = torch.argmax(outputs.logits, dim=2)
    predicted_labels = predicted_labels.tolist()[0]

    # Map the labels to their corresponding tokens
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0].tolist())

    names = []
    roles = []

    current_entity = ""
    for token, label_id in zip(tokens, predicted_labels):
        label = model.config.id2label[label_id]
        if label.startswith("B-"):
            if current_entity:
                if "ROLE" in current_entity:
                    roles.append(current_entity[2:])
                else:
                    names.append(current_entity[2:])
            current_entity = f"{label[2:]} {token}"
        elif label.startswith("I-"):
            if current_entity:
                current_entity += f" {token}"
        else:
            if current_entity:
                if "ROLE" in current_entity:
                    roles.append(current_entity[2:])
                else:
                    names.append(current_entity[2:])
                current_entity = ""

    return "|".join(names), "|".join(roles)

def main():
    # Prompt for user input
    input_file = input("Enter the name of the input file (e.g., maastricht.csv): ")
    output_file = "Maastricht_BERT.csv"

    # Load the CSV file
    df = pd.read_csv(input_file, encoding="utf-8")

    total_rows = len(df)
    print(f"Processing {total_rows} rows...")

    with tqdm(total=total_rows) as pbar:
        def update_progress(*_):
            pbar.update(1)

        # Adjust column names for roles and names
        df['Extracted Names'], df['Roles'] = zip(*df["omschrijving"].apply(extract_names_and_roles))
        df["Extracted Names"] = df["Extracted Names"].apply(lambda x: x if x else None)
        df["Roles"] = df["Roles"].apply(lambda x: x if x else None)
        df["Text"] = df["omschrijving"].apply(lambda x: x if x else None)
        df["Index"] = df.index + 1  # Add an index column

        # Save the results to the new file
        df.to_csv(output_file, encoding="utf-8", index=False)

    print(f"Processing complete. Results saved in {output_file}.")

if __name__ == "__main__":
    main()

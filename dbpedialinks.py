import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm

# Function to execute SPARQL query
def execute_sparql_query(value):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT *
        WHERE {{
            ?thing rdfs:label "{value}"@nl.
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results['results']['bindings']:
        return results['results']['bindings']
    else:
        return None

# Function to process CSV file and execute SPARQL query
def process_csv(input_filename, output_filename, selected_column):
    df = pd.read_csv(input_filename)
    
    if selected_column not in df.columns:
        print(f"Column '{selected_column}' not found in the CSV file. Available columns: {', '.join(df.columns)}")
        return

    output_df = pd.DataFrame()

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing"):
        value = row[selected_column]
        query_results = execute_sparql_query(value)

        if query_results:
            # Extracting the relevant data from the query results
            query_result_data = {key: value['value'] for key, value in query_results[0].items()}
        else:
            query_result_data = {'thing': 'Not Found'}

        # Adding the results to the new dataframe
        new_row = pd.Series({**row, **query_result_data})
        output_df = output_df.append(new_row, ignore_index=True)

    # Save the results to a new CSV file
    output_df.to_csv(output_filename, index=False)
    print(f"\nResults saved to {output_filename}")

if __name__ == "__main__":
    # Ask for input CSV file
    input_filename = input("Enter the input CSV file path: ")

    # Ask for the output CSV file
    output_filename = input("Enter the output CSV file path: ")

    # Ask for the column name
    selected_column = input("Enter the column name to use for the SPARQL query: ")

    # Process CSV and execute SPARQL query
    process_csv(input_filename, output_filename, selected_column)

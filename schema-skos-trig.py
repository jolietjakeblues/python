import requests
import rdflib
from rdflib import Graph, URIRef, Namespace

def fetch_data(base_url, max_pages=None):
    page = 1
    all_data = set()  # Gebruik een set om duplicaten te voorkomen
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(f"{base_url}&page={page}&pageSize=10000")
        if response.status_code != 200:
            print(f"Failed to fetch data from page {page}. Status code: {response.status_code}")
            break

        data = response.text.strip()
        if data in all_data:
            print(f"Data from page {page} is already fetched. Stopping to avoid duplicates.")
            break

        all_data.add(data)
        
        if not data or (max_pages and page >= max_pages):
            break
        
        page += 1

    return list(all_data)

def save_to_trig(data_list, output_file, graph_uri):
    g = Graph(identifier=URIRef(graph_uri))
    
    # Bind de namespaces expliciet
    schema = Namespace('http://schema.org/')
    ceo = Namespace('https://linkeddata.cultureelerfgoed.nl/def/ceo#')

    g.bind('schema', schema)
    g.bind('ceo', ceo)

    for data in data_list:
        g.parse(data=data, format='nt')

    print(f"Saving data to {output_file}...")
    g.serialize(destination=output_file, format='trig')
    print(f"Data saved successfully.")

def main():
    base_url = "https://api.linkeddata.cultureelerfgoed.nl/queries/rce/Query-15-3/2/run?"
    output_file = "result.trig"
    graph_uri = "https://linkeddata.cultureelerfgoed.nl/graph/schema"
    
    print("Starting data fetching process...")
    data_list = fetch_data(base_url)
    
    if data_list:
        save_to_trig(data_list, output_file, graph_uri)
    else:
        print("No data fetched. Exiting.")

if __name__ == "__main__":
    main()

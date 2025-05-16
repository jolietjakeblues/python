import requests
import rdflib
from rdflib import Graph, URIRef
import os

def fetch_data(base_url, max_pages=None):
    page = 1
    all_data = []
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(f"{base_url}&page={page}&pageSize=10000")  # pageSize toegevoegd
        if response.status_code != 200:
            print(f"Failed to fetch data from page {page}. Status code: {response.status_code}")
            break

        data = response.text
        all_data.append(data)

        # Check if we should stop fetching more pages
        if not data.strip() or (max_pages and page >= max_pages):
            break
        
        page += 1

    return all_data

def save_to_trig(data_list, output_file, graph_uri):
    g = Graph()
    g.bind('schema', URIRef('http://schema.org/'))
    g.bind('ceo', URIRef('https://linkeddata.cultureelerfgoed.nl/def/ceo#'))

    for data in data_list:
        g.parse(data=data, format='nt')

    print(f"Saving data to {output_file}...")
    g.serialize(destination=output_file, format='trig', context=URIRef(graph_uri))
    print(f"Data saved successfully.")

def main():
    base_url = "https://api.linkeddata.cultureelerfgoed.nl/queries/rce/Query-15-3/3/run?"
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

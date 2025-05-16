import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

# Ask for input and output file names
input_file = input("Enter input file name: ")
output_file = input("Enter output file name: ")

# Function to fetch metadata from a URL
def fetch_metadata(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Initialize a dictionary to store metadata
        metadata = {}
        
        # Find all metadata rows
        metadata_rows = soup.find_all("tr")
        
        # Initialize tqdm for progression bar
        progress_bar = tqdm(total=len(metadata_rows), desc="Processing Metadata", unit="row")
        
        # Loop through each metadata row and extract key-value pairs
        for row in metadata_rows:
            th = row.find("th")
            td = row.find("td")
            if th and td:
                metadata_key = th.get_text(strip=True)
                metadata_value = td.get_text(strip=True)
                # Split the value if ';' is present
                if ';' in metadata_value:
                    metadata[metadata_key] = [value.strip() for value in metadata_value.split(';')]
                else:
                    metadata[metadata_key] = metadata_value.strip()
            progress_bar.update(1)  # Update progress bar
        
        progress_bar.close()  # Close progress bar
        
        return metadata
    else:
        print(f"Failed to retrieve data from the URL: {url}")
        return None

# Read URLs from the input file
with open(input_file, "r") as f:
    urls = f.readlines()

# Initialize a dictionary to store metadata for all URLs
all_metadata = {}

# Iterate through each URL and fetch metadata
for url in urls:
    url = url.strip()
    metadata = fetch_metadata(url)
    if metadata:
        all_metadata[url] = metadata

# Write all metadata to the specified output file
with open(output_file, "w") as json_file:
    json.dump(all_metadata, json_file, indent=4)
        
print(f"Metadata saved to {output_file} file.")

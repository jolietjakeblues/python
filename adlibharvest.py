import requests
import os
from tqdm import tqdm
import time

BASE_URL = "https://rce.adlibhosting.com/harvest/wwwopac.ashx?database=books&search=ex=*&limit=3000"
TOTAL_RECORDS = 162306
LIMIT = 3000
TOTAL_REQUESTS = (TOTAL_RECORDS // LIMIT) + (1 if TOTAL_RECORDS % LIMIT > 0 else 0)

def fetch_records(offset, retry_count=3):
    url = f"{BASE_URL}&startfrom={offset}"
    try:
        print(f"Fetching records from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.content
    except requests.exceptions.RequestException as e:
        if retry_count > 0:
            print(f"Request failed: {e}. Retrying... ({retry_count} retries left)")
            time.sleep(5)  # Wait a bit before retrying
            return fetch_records(offset, retry_count - 1)
        else:
            print(f"Failed to fetch records at offset {offset}: {e}")
            return None

def save_records(data, index):
    filename = f"adlibpointer1962_{index}.xml"
    print(f"Saving records to: {filename}")
    with open(filename, "wb") as file:
        file.write(data)

def main():
    # Determine the last successfully fetched file index
    index = 1
    while os.path.exists(f"adlibpointer1962_{index}.xml"):
        index += 1

    with tqdm(total=TOTAL_REQUESTS, initial=index-1) as pbar:
        for i in range(index, TOTAL_REQUESTS + 1):
            offset = (i - 1) * LIMIT + 1
            data = fetch_records(offset)
            if data:
                save_records(data, i)
            else:
                print(f"Stopping due to failure at offset {offset}")
                break
            pbar.update(1)

if __name__ == "__main__":
    print("Starting script...")
    main()
    print("Script finished.")

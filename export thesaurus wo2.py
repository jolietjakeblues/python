import requests
import os
import subprocess
import logging

# Logging instellen
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hardcoded configuratie (voor testen)
EXPORT_URL = 'https://data.cultureelerfgoed.nl/PoolParty/api/projects/1DE00318-CB07-0001-FBB4-C620F33C1540/export'
AUTH_HEADER_EXPORT = {
    'Authorization': 'Basic YXBpdXNlcl9yZWZlcmVudGllbmV0d2VyazotbmsrMWdJNkQiRWJNYih3MHhBZUFrcykwYmEmM0E3OEpZMzlMZSMj',
    'Content-Type': 'application/json'
}
EXPORT_PARAMS = {
    "prettyPrint": True,
    "format": "TriG",
    "modules": ["concepts"]
}
TRIPLYDB_PATH = r"C:\Users\linkeddata\Downloads\triplydb.exe"  # Pad naar triplydb.exe
DATASET_NAME = "wo2thesaurus-cli"  # Naam van de dataset waar data wordt toegevoegd
GRAPH_NAME = "https://data.niod.nl/WO2_Thesaurus/thesaurus"  # Graph naam of thesaurus
TRIPLYDB_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1bmtub3duIiwiaXNzIjoiaHR0cHM6Ly9hcGkubGlua2VkZGF0YS5jdWx0dXJlZWxlcmZnb2VkLm5sIiwianRpIjoiMTZhMmMwMzAtYzk3Ni00ZWFjLTgxNDgtNDY3YmI3ZTYxYTMwIiwidWlkIjoiNjI4MjI5MWUxOTIyYTEyZTlhNzE2MDliIiwiaWF0IjoxNzM3MTE5OTc2fQ.kbzgP9RKQSDax01bmVZQNlB9iwWkxFLHHbBymYUjWXs"  # Uw TriplyDB API-token

def export_rdf_data(export_url, headers, params):
    """Exporteer RDF-data van de API."""
    logging.info("Start met exporteren van RDF-data...")
    try:
        response = requests.post(export_url, headers=headers, json=params)
        if response.status_code == 200:
            logging.info("Export succesvol!")
            return response.content
        else:
            logging.error(f"Fout bij export: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logging.error(f"Onverwachte fout tijdens export: {e}")
        return None

def save_to_file(data, file_name):
    """Sla RDF-data op in een bestand."""
    try:
        with open(file_name, 'wb') as file:
            file.write(data)
        logging.info(f"Data succesvol opgeslagen in bestand: {file_name}")
        return True
    except Exception as e:
        logging.error(f"Fout bij opslaan bestand: {e}")
        return False

def import_with_triplydb(file_path, triplydb_path, dataset_name, graph_name, token):
    """Gebruik triplydb.exe om het bestand toe te voegen aan de bestaande dataset."""
    logging.info(f"Start met importeren van '{file_path}' naar dataset '{dataset_name}' en graph '{graph_name}' met TriplyDB CLI...")
    try:
        command = [
            triplydb_path,
            "import-from-file",
            "--dataset", dataset_name,
            "--token", token,  # Token toevoegen voor authenticatie
            "--default-graph-name", graph_name,  # Graph naam specificeren
            "--mode", "merge",  # Modus instellen op 'merge'
            file_path
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Import succesvol! Data toegevoegd aan de bestaande dataset en graph.")
            logging.info(result.stdout)
            return True
        else:
            logging.error(f"Fout bij import: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Onverwachte fout tijdens import: {e}")
        return False

def main():
    # Stap 1: Exporteer data
    rdf_data = export_rdf_data(EXPORT_URL, AUTH_HEADER_EXPORT, EXPORT_PARAMS)
    if not rdf_data:
        logging.error("Export mislukt. Proces beëindigd.")
        return

    # Stap 2: Sla de data op in een bestand
    file_name = "exported_data.trig"
    if not save_to_file(rdf_data, file_name):
        logging.error("Opslaan van data is mislukt. Proces beëindigd.")
        return

    # Stap 3: Importeer met TriplyDB CLI
    if not import_with_triplydb(file_name, TRIPLYDB_PATH, DATASET_NAME, GRAPH_NAME, TRIPLYDB_TOKEN):
        logging.error("Import mislukt. Controleer de TriplyDB CLI en dataset.")
        return

    # Stap 4: Opruimen van tijdelijke bestanden
    try:
        os.remove(file_name)
        logging.info("Tijdelijk bestand succesvol verwijderd.")
    except Exception as e:
        logging.warning(f"Kon het tijdelijke bestand niet verwijderen: {e}")

    logging.info("Proces voltooid.")

if __name__ == "__main__":
    main()

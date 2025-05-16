import requests  # Voor HTTP-aanroepen
import os  # Voor bestandsbeheer
import subprocess  # Voor het uitvoeren van CLI-commando's
import logging  # Voor logging van processen
import yaml  # Voor het laden van YAML-configuratie
from datetime import datetime  # Voor datumstempels

# Functie om de configuratie uit een YAML-bestand te laden
def load_config(config_file="config_wo2.yaml"):
    """
    Laadt de configuratie uit een YAML-bestand.
    :param config_file: Pad naar de YAML-configuratie.
    :return: Geparste configuratie als een Python-dictionary.
    """
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

# Logging instellen
def setup_logging(log_file):
    """
    Configureert logging zodat logberichten zowel in een bestand als op de console worden weergegeven.
    :param log_file: Pad naar het logbestand.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Log naar bestand
            logging.StreamHandler()  # Log naar console
        ]
    )

# Exporteer RDF-data vanuit PoolParty
def export_rdf_data(project_code, export_url_template, headers):
    """
    Voert een HTTP POST-aanroep uit om RDF-data van PoolParty te exporteren.
    :param project_code: De unieke code van het PoolParty-project.
    :param export_url_template: Sjabloon voor de export-URL van PoolParty.
    :param headers: Headers voor authenticatie.
    :return: De geëxporteerde RDF-data als bytes.
    """
    logging.info(f"Start export voor project {project_code}...")
    try:
        response = requests.post(
            export_url_template.format(project_code),
            headers=headers,
            json={"prettyPrint": True, "format": "TriG", "modules": ["concepts"]}
        )
        if response.status_code == 200:
            logging.info(f"Export succesvol voor project {project_code}!")
            return response.content
        else:
            logging.error(f"Fout bij export voor project {project_code}: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logging.error(f"Onverwachte fout bij export voor project {project_code}: {e}")
        return None

# Sla RDF-data op in een lokaal bestand
def save_to_file(data, file_name):
    """
    Schrijft RDF-data naar een bestand.
    :param data: De RDF-data in bytes.
    :param file_name: Naam van het bestand waarin de data wordt opgeslagen.
    :return: True bij succes, anders False.
    """
    try:
        with open(file_name, "wb") as file:
            file.write(data)
        logging.info(f"Data opgeslagen in bestand: {file_name}")
        return True
    except Exception as e:
        logging.error(f"Fout bij opslaan van bestand {file_name}: {e}")
        return False

# Voeg meerdere bestanden samen tot één bestand
def merge_files(input_files, output_file):
    """
    Combineert meerdere RDF-bestanden tot één bestand.
    :param input_files: Lijst van bestandsnamen die moeten worden samengevoegd.
    :param output_file: Naam van het outputbestand.
    :return: True bij succes, anders False.
    """
    logging.info("Start met samenvoegen van bestanden...")
    try:
        with open(output_file, "wb") as merged_file:
            for file_path in input_files:
                with open(file_path, "rb") as input_file:
                    merged_file.write(input_file.read())
        logging.info(f"Bestanden samengevoegd in {output_file}")
        return True
    except Exception as e:
        logging.error(f"Fout bij samenvoegen van bestanden: {e}")
        return False

# Importeer een bestand naar TriplyDB via de CLI
def import_with_triplydb(file_path, cli_path, dataset_name, account_name, graph_name, token):
    """
    Importeert RDF-data naar TriplyDB met behulp van de CLI.
    :param file_path: Pad naar het bestand dat moet worden geïmporteerd.
    :param cli_path: Pad naar de TriplyDB CLI.
    :param dataset_name: Naam van de dataset in TriplyDB.
    :param account_name: Naam van de account waarin de dataset zich bevindt.
    :param graph_name: Naam van de graph waarin de data wordt opgeslagen.
    :param token: Authenticatietoken voor TriplyDB.
    """
    logging.info(f"Start met importeren van '{file_path}' naar graph '{graph_name}' in dataset '{dataset_name}'...")
    try:
        command = [
            cli_path,
            "import-from-file",
            "--dataset", dataset_name,
            "--account", account_name,  # Voeg de accountnaam toe
            "--token", token,
            "--default-graph-name", graph_name,
            "--mode", "merge",
            file_path
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Import succesvol voor graph {graph_name}!")
            return True
        else:
            logging.error(f"Fout bij importeren van '{file_path}' naar graph '{graph_name}': {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Onverwachte fout tijdens import: {e}")
        return False

# Upload een logbestand als asset naar TriplyDB
def upload_asset(file_path, cli_path, dataset_name, account_name, token):
    """
    Uploadt een bestand als asset naar TriplyDB.
    :param file_path: Pad naar het bestand dat moet worden geüpload.
    :param cli_path: Pad naar de TriplyDB CLI.
    :param dataset_name: Naam van de dataset waarin het bestand wordt geüpload.
    :param account_name: Naam van de account waarin de dataset zich bevindt.
    :param token: Authenticatietoken voor TriplyDB.
    """
    logging.info(f"Start met uploaden van asset '{file_path}' naar dataset '{dataset_name}' in account '{account_name}'...")
    try:
        command = [
            cli_path,
            "upload-asset",
            "--dataset", dataset_name,
            "--account", account_name,  # Voeg de accountnaam toe
            "--token", token,
            "--overwrite",
            file_path
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Asset succesvol geüpload: {file_path}")
            return True
        else:
            logging.error(f"Fout bij uploaden van asset '{file_path}': {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Onverwachte fout bij uploaden van asset: {e}")
        return False

# Hoofdproces
def main():
    """
    Hoofdproces om RDF-data te exporteren, samen te voegen, te importeren naar TriplyDB, 
    en logbestanden als asset te uploaden.
    """
    # Laad configuratie
    config = load_config()
    triplydb_config = config["triplydb"]
    poolparty_config = config["poolparty"]
    projects = config["projects"]
    output_config = config["output"]

    # Stel logging in
    log_file = output_config["log_file"].replace("<date>", datetime.now().strftime("%Y%m%d"))
    setup_logging(log_file)

    temp_files = []

    # Stap 1: Exporteer data per project
    for project in projects:
        project_code = project["project_code"]
        file_name = f"{project_code}.trig"
        data = export_rdf_data(project_code, poolparty_config["export_url_template"], poolparty_config["auth_headers"])
        if data and save_to_file(data, file_name):
            temp_files.append((file_name, project["graph_name"]))

    # Stap 2: Merge bestanden
    merged_file = output_config["merged_file"]
    merge_files([file[0] for file in temp_files], merged_file)

    # Stap 3: Importeer naar TriplyDB
    for _, graph_name in temp_files:
        import_with_triplydb(
            merged_file, 
            triplydb_config["cli_path"], 
            triplydb_config["dataset_name"], 
            triplydb_config["account"], 
            graph_name, 
            triplydb_config["token"]
        )

    # Stap 4: Upload logbestand als asset
    upload_asset(
        log_file, 
        triplydb_config["cli_path"], 
        triplydb_config["dataset_name"], 
        triplydb_config["account"], 
        triplydb_config["token"]
    )

    # Stap 5: Opruimen
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    for file_name, _ in temp_files:
        os.remove(file_name)
    os.remove(log_file)

    logging.info("Proces voltooid.")

# Start het script
if __name__ == "__main__":
    main()

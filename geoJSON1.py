import pandas as pd
import geopandas as gpd
import json
import requests

def main():
    # Definieer de API-request URL
    api_url = "https://api.linkeddata.cultureelerfgoed.nl/queries/rce/Query-16-1-1-2-1-1/run.json"

    # Voer de API-request uit en lees de JSON-gegevens
    response = requests.get(api_url)
    data = response.json()

    # Convert de JSON data naar een DataFrame
    df = pd.DataFrame(data["results"]["bindings"])

    # Maak een GeoDataFrame van de DataFrame met behulp van de WKT-representatie van de geometrie
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["shape.value"]))

    # Stel de CRS van de GeoDataFrame in op EPSG:28992 (RD New)
    gdf.crs = "EPSG:28992"

    # Definieer de bestandsnaam voor het GeoJSON-bestand
    output_filename = "output_geo_winkels2"

    # Schrijf de GeoDataFrame naar een GeoJSON-bestand
    gdf.to_file(f"{output_filename}.geojson", driver="GeoJSON")

    # Laad de laag in QGIS
    iface.addVectorLayer(f"{output_filename}.geojson", output_filename, "ogr")

# Roep de main-functie aan
main()

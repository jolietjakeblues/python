import pandas as pd
import geopandas as gpd

# Prompt the user for the URL of the CSV file to read
csv_url = input("Enter the URL of the CSV file to read. (including the .csv extension): ")

# Prompt the user for the name of the column containing the geometry information
geom_col = input("Enter the name of the column containing the geometry information: ")

# Prompt the user for the name of the output file
output_file = input("Enter the name of the output file (without extension): ")

# Read the CSV file from the specified URL
df = pd.read_csv(csv_url)

# Create a GeoDataFrame from the DataFrame, using the WKT representation of the geometry
gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df[geom_col]))

# Set the CRS of the GeoDataFrame to EPSG:28992 (RD New)
gdf.crs = "EPSG:28992"

# Write the GeoDataFrame to a GeoJSON file
gdf.to_file(f"{output_file}.geojson", driver="GeoJSON")

# Print message when script is done
print("Shapefile successfully created!")
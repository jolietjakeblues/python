import pandas as pd
import geopandas as gpd

# Read the CSV file from the API endpoint
df = pd.read_csv("https://api.linkeddata.cultureelerfgoed.nl/queries/rce/Query-16-1-1-2-1-1/run.csv")

# Create a GeoDataFrame from the DataFrame, using the WKT representation of the geometry
gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["shape"]))

# Set the CRS of the GeoDataFrame to EPSG:28992 (RD New)
gdf.crs = "EPSG:28992"

# Write the GeoDataFrame to a shapefile
gdf.to_file("output_geo_winkels2.geojson", driver="GeoJSON")

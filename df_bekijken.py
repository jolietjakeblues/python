import pandas as pd

# Gebruik raw string (r"...") om backslashes goed te lezen
pad = r"E:\Export_2025-03-11-Kunstcollectie_alles_in_eigen_beheer\Export_2025-03-11-Kunstcollectie_alles_in_eigen_beheer.xml"

# Probeer standaard XML-parsing
try:
    df = pd.read_xml(pad)
except ValueError:
    # Als standaard mislukt, probeer met xpath op 'record'-achtige elementen
    df = pd.read_xml(pad, xpath=".//record")  # Pas 'record' aan op basis van uw XML-structuur

# Laat eerste rijen zien
print(df.head(10))
print(df.info())

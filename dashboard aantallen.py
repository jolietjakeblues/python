import pandas as pd
import matplotlib.pyplot as plt

# Vraag de gebruiker om de bestandsnamen
file1 = input("Voer de naam van het eerste Excel-bestand in (inclusief .xlsx): ")
file2 = input("Voer de naam van het tweede Excel-bestand in (inclusief .xlsx): ")

# Lees de Excel-bestanden
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Zorg ervoor dat de kolommen consistent zijn
df1.columns = ['Tag', 'Count']
df2.columns = ['Tag', 'Count']

# Merge de twee dataframes op de 'Tag' kolom
merged_df = pd.merge(df1, df2, on='Tag', how='outer', suffixes=('_file1', '_file2')).fillna(0)

# Bereken het verschil in aantallen
merged_df['Difference'] = merged_df['Count_file2'] - merged_df['Count_file1']

# Maak een dashboard
plt.figure(figsize=(12, 8))

# Bar chart voor de verschillen
plt.bar(merged_df['Tag'], merged_df['Difference'], color='skyblue')
plt.xlabel('Tags')
plt.ylabel('Verschil in Aantal')
plt.title('Verschil in Aantal Tags tussen Twee Bestanden')
plt.xticks(rotation=90)
plt.grid(True)

# Toon de plot
plt.tight_layout()
plt.show()

# Sla het resultaat op in een nieuw Excel-bestand
output_file = input("Voer de naam van het uitvoerbestand in (inclusief .xlsx): ")
merged_df.to_excel(output_file, index=False)
print(f"De resultaten zijn opgeslagen in {output_file}")

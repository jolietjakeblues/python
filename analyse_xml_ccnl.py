import xml.etree.ElementTree as ET
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter

def analyze_xml_fields():
    # Vraag om de bestandsnamen
    input_file = input("Voer de naam van het XML-bestand in (inclusief pad): ").strip()
    output_file = input("Voer de naam van het uitvoerbestand (CSV) in: ").strip()
    error_date_file = input("Voer de naam van het bestand voor foutieve datums in (CSV): ").strip()
    pdf_output_file = input("Voer de naam van het grafiekbestand (PDF): ").strip()

    if not os.path.exists(input_file):
        print("Het opgegeven bestand bestaat niet.")
        return

    # Voortgangsindicator
    print("Bezig met het verwerken van het bestand...")

    # XML-bestand inlezen
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Analyse voorbereiden
    all_fields = set()
    records = []

    # Verzamel alle velden en hun waarden per record
    for record in root:
        record_data = {}
        for element in record.iter():
            field_name = element.tag
            value = element.text.strip() if element.text else None
            record_data[field_name] = value
            all_fields.add(field_name)
        records.append(record_data)

    # DataFrame maken voor analyse
    df = pd.DataFrame(records)

    # Algemene analyse van velden
    analysis = []
    for field in all_fields:
        total = len(df)
        filled = df[field].notna().sum()
        percentage = (filled / total) * 100 if total > 0 else 0
        analysis.append({"Field": field, "Total Records": total, "Filled Records": filled, "Percentage": percentage})

    # Frequentieanalyse van waarden per veld
    frequentie_resultaten = {}
    for field in all_fields:
        if field in df.columns:
            frequentie_resultaten[field] = df[field].value_counts().head(5).to_dict()

    # Analyse van veldlengte
    lengte_analyse = {}
    for field in all_fields:
        if field in df.columns and df[field].notna().any():
            lengte_analyse[field] = df[field].dropna().apply(len).mean()

    # Trendanalyse op basis van datumvelden (indien aanwezig)
    datum_trend = {}
    error_dates = []
    for index, row in df.iterrows():
        for field in all_fields:
            if field in df.columns:
                if "date" in field.lower() or "time" in field.lower():  # Controleer alleen velden die mogelijk datums bevatten
                    try:
                        df[field] = pd.to_datetime(df[field], format='%Y-%m-%d', errors='coerce')
                        if pd.isna(df.at[index, field]) and row[field]:
                            error_dates.append({"Record": row.get("priref", index), "Field": field, "Value": row[field]})
                        elif df[field].notna().any():
                            datum_trend[field] = df[field].dropna().dt.year.value_counts().sort_index().to_dict()
                    except Exception:
                        continue

    # Opslaan foutieve datums
    if error_dates:
        error_df = pd.DataFrame(error_dates)
        error_df.to_csv(error_date_file, index=False)
        print(f"Foutieve datums opgeslagen in {error_date_file}")

    # Analyse van lege records
    lege_records = (df.isna().mean(axis=1) * 100).value_counts(bins=[0, 25, 50, 75, 100]).to_dict()

    # Resultaten naar een DataFrame
    analysis_df = pd.DataFrame(analysis)

    # Opslaan als CSV
    analysis_df.to_csv(output_file, index=False)
    print(f"Resultaten opgeslagen in {output_file}")

    # Visualisatie: Grafieken in één PDF-bestand
    with PdfPages(pdf_output_file) as pdf:
        # Percentage gevulde velden
        plt.figure(figsize=(12, 8))
        analysis_df_sorted = analysis_df.sort_values(by="Percentage", ascending=False)
        plt.barh(analysis_df_sorted["Field"], analysis_df_sorted["Percentage"])
        plt.xlabel("Percentage gevuld")
        plt.ylabel("Velden")
        plt.title("Percentage gevulde velden in XML-bestand")
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        # Veldlengte-analyse
        plt.figure(figsize=(12, 8))
        lengte_df = pd.DataFrame(list(lengte_analyse.items()), columns=["Field", "Average Length"])
        lengte_df = lengte_df.sort_values(by="Average Length", ascending=False)
        plt.barh(lengte_df["Field"], lengte_df["Average Length"])
        plt.xlabel("Gemiddelde lengte")
        plt.ylabel("Velden")
        plt.title("Gemiddelde lengte van velden")
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        # Trendanalyse per jaar
        for field, trends in datum_trend.items():
            plt.figure(figsize=(12, 8))
            plt.bar(trends.keys(), trends.values())
            plt.xlabel("Jaar")
            plt.ylabel("Aantal records")
            plt.title(f"Trendanalyse voor {field}")
            plt.tight_layout()
            pdf.savefig()
            plt.close()

    print(f"Grafieken opgeslagen in {pdf_output_file}")

# Voorbeeldgebruik
analyze_xml_fields()

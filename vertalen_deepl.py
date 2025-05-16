import requests
import pandas as pd

# API-sleutel (vervang 'your_deepl_auth_key' door jouw eigen sleutel)
DEEPL_API_KEY = 'b8f7f79f-47e3-f974-9476-f1ab39f7f278:fx'

# Functie om tekst te vertalen met DeepL API
def translate_text(text, target_lang='EN'):
    url = 'https://api-free.deepl.com/v2/translate'
    headers = {
        'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'text': [text],  # Zet de tekst in een lijst
        'target_lang': target_lang
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['translations'][0]['text']
    else:
        print(f'Error: {response.status_code}, {response.text}')
        return None

# Laad de Excel
df = pd.read_excel('concepten_zonder engels.xlsx')

# Vertaal de waarden in de kolom 'scopeNoteNL'
df['scopeNoteEN'] = df['scopeNoteNL'].apply(lambda x: translate_text(x) if pd.notnull(x) else None)

# Opslaan in een nieuwe Excel-bestand
df.to_excel('vertaald_excelbestand.xlsx', index=False)

print("Vertaling voltooid en opgeslagen in 'vertaald_excelbestand.xlsx'")

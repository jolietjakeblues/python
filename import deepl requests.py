import deepl

def translate_document_with_original():
    # Vraag om input- en uitvoerbestanden
    input_file = input("Voer de volledige pad en naam in van het te vertalen bestand (inclusief extensie): ").strip()
    output_file = input("Voer de volledige pad en naam in van het uitvoerbestand (inclusief extensie, bijv. .txt of .csv): ").strip()

    # DeepL API-sleutel
    auth_key = "fb84278e-55d3-4681-9aee-5bc7d7ee388e:fx"  # Uw opgegeven API-sleutel
    translator = deepl.Translator(auth_key)

    try:
        # Lees het originele bestand
        with open(input_file, 'r', encoding='utf-8') as file:
            original_lines = file.readlines()

        translated_lines = []
        print("Het document wordt vertaald, dit kan even duren...")

        # Vertaal regel voor regel
        for line in original_lines:
            translated_text = translator.translate_text(line.strip(), target_lang="NL")
            translated_lines.append((line.strip(), translated_text.text))

        # Schrijf naar het uitvoerbestand (origineel + vertaling)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Origineel\tVertaling\n")  # Header voor een tab-gescheiden bestand
            for original, translated in translated_lines:
                file.write(f"{original}\t{translated}\n")

        print(f"Vertaling voltooid en opgeslagen in: {output_file}")
    except deepl.DeepLException as e:
        print(f"DeepL API-fout: {e}")
    except FileNotFoundError:
        print("Het opgegeven inputbestand bestaat niet. Controleer de bestandsnaam en het pad.")
    except Exception as e:
        print(f"Onverwachte fout: {e}")

if __name__ == "__main__":
    translate_document_with_original()

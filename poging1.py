def main():
    # Vraag om input- en outputbestandsnamen
    input_filename = input("Geef de naam van het input bestand: ")
    output_filename = input("Geef de naam van het output bestand: ")

    try:
        # Lees de inhoud van het input bestand
        with open(input_filename, "r") as input_file:
            content = input_file.read()

        # Voer de zoek- en vervangacties uit
        modified_content = content.replace("</edm:WebResource>", "</edm:WebResource><ceox:ff>")
        modified_content = modified_content.replace("</rdf:RDF>", "</ceox:ff></rdf:RDF>")

        # Schrijf het gewijzigde bestand naar het output bestand
        with open(output_filename, "w") as output_file:
            output_file.write(modified_content)

        print("Het script is voltooid en het output bestand is aangemaakt.")
    except FileNotFoundError:
        print("Fout: Het opgegeven input bestand bestaat niet.")
    except Exception as e:
        print("Er is een fout opgetreden:", e)


if __name__ == "__main__":
    main()

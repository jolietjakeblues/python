from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium import webdriver

# Opties voor het uitvoeren van Chrome in de headless modus (zonder GUI)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Voer Chrome uit zonder GUI

# Pad naar de ChromeDriver-binary (zorg ervoor dat je de juiste versie voor je Chrome-browser hebt)
chrome_driver_path = 'E:/pythoncursus/chromedriver.exe'

# URL van de webpagina
url = "https://www.persistent-identifier.nl/urn:nbn:nl:ui:13-13c-g5x"

# Start de Chrome-webdriver
service = Service(chrome_driver_path)
service.start()

# Initialiseer de Chrome-driver met de service en de gewenste opties
driver = webdriver.Chrome(service=service, options=chrome_options)

# Laad de webpagina
driver.get(url)

# Wacht tot de pagina volledig is geladen (je kunt hier een specifieke wachttijd instellen als dat nodig is)
driver.implicitly_wait(10)  # Wacht maximaal 10 seconden totdat de elementen worden geladen

# Zoek naar de DOI-elementen op de pagina
dois = driver.find_elements(By.XPATH, "//a[contains(@href, 'doi.org')]")

# Print de gevonden DOI's
if dois:
    print("DOI(s) gevonden:")
    for doi in dois:
        print(doi.get_attribute("href"))
else:
    print("Geen DOI gevonden.")

# Sluit de browser en de service
driver.quit()
service.stop()

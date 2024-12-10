from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import os
import time

def scrape_appartager():
    # Configuration du WebDriver
    driver_path = "./scraping/chromedriver-win64/chromedriver.exe"
    service = Service(driver_path)
    options = Options()
    options.add_argument("--headless")  # Exécuter sans interface graphique
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.appartager.com/"
    driver.get(url)

    # Attends que la page charge
    time.sleep(5)

    # Résultats
    annonces = []
    try:
        elements = driver.find_elements(By.CLASS_NAME, "listing-card")  # Sélecteur à ajuster
        for el in elements:
            try:
                title = el.find_element(By.CLASS_NAME, "title").text  # Titre
                location = el.find_element(By.CLASS_NAME, "location").text  # Localisation
                price = el.find_element(By.CLASS_NAME, "price").text  # Prix
                annonces.append({"title": title, "location": location, "price": price})
            except Exception as e:
                print(f"Erreur lors de l'extraction d'une annonce : {e}")

    except Exception as e:
        print(f"Erreur principale : {e}")

    # Sauvegarde des résultats
    output_file = "./output/annonces_appartager.json"
    os.makedirs("./output", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(annonces, f, ensure_ascii=False, indent=4)

    print(f"{len(annonces)} annonces sauvegardées dans {output_file}")
    driver.quit()

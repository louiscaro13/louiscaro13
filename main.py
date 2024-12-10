import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuration du chemin vers ChromeDriver
driver_path = "./scraping/chrome-win64/chromedriver.exe"

# Vérifie si le dossier 'output' existe, sinon le crée
if not os.path.exists("scraping/output"):
    os.makedirs("scraping/output")

# Options du navigateur Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Pour exécuter Chrome sans interface
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialisation du navigateur
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


# Fonction pour scraper "La Carte des Colocs"
def scrape_carte_colocs():
    print("Scraping La Carte des Colocs...")
    url = "https://www.lacartedescolocs.fr/"
    driver.get(url)
    time.sleep(5)  # Attends le chargement complet de la page

    # Sauvegarder la page source pour débogage
    with open("scraping/output/page_source_carte_colocs.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Trouver les annonces
    results = []
    annonces = driver.find_elements(By.CSS_SELECTOR, "div.card")  # Adapter ce sélecteur si nécessaire
    for annonce in annonces:
        try:
            title = annonce.find_element(By.CSS_SELECTOR, "h3.card-title").text.strip()
            price = annonce.find_element(By.CSS_SELECTOR, "span.card-price").text.strip()
            location = annonce.find_element(By.CSS_SELECTOR, "span.card-location").text.strip()
            results.append({"title": title, "price": price, "location": location})
        except Exception as e:
            print(f"Erreur lors du traitement d'une annonce : {e}")

    # Sauvegarder les résultats dans un fichier JSON
    with open("scraping/output/annonces_carte_colocs.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"{len(results)} annonces sauvegardées dans ./scraping/output/annonces_carte_colocs.json")


# Fonction pour scraper "Appartager"
def scrape_appartager():
    print("Scraping Appartager...")
    url = "https://www.appartager.com/"
    driver.get(url)
    time.sleep(5)

    # Sauvegarder la page source pour débogage
    with open("scraping/output/page_source_appartager.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Trouver les annonces
    results = []
    annonces = driver.find_elements(By.CSS_SELECTOR, "div.listing-card")  # Adapter ce sélecteur si nécessaire
    for annonce in annonces:
        try:
            title = annonce.find_element(By.CSS_SELECTOR, "h2.title").text.strip()
            price = annonce.find_element(By.CSS_SELECTOR, "span.price").text.strip()
            location = annonce.find_element(By.CSS_SELECTOR, "span.location").text.strip()
            results.append({"title": title, "price": price, "location": location})
        except Exception as e:
            print(f"Erreur lors du traitement d'une annonce : {e}")

    # Sauvegarder les résultats dans un fichier JSON
    with open("scraping/output/annonces_appartager.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"{len(results)} annonces sauvegardées dans ./scraping/output/annonces_appartager.json")


# Appeler les fonctions de scraping
try:
    scrape_carte_colocs()
    scrape_appartager()
finally:
    driver.quit()
    print("Scraping terminé !")

import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from api_univ_lorraine.Utilisateur import Utilisateur
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_base import data_base_manager

MDW_URL = "https://mdw.univ-lorraine.fr/"
GECKODRIVER_PATH = "ressources/geckodriver"
DB_PATH = "ressources/data.db"
FIREFOX_PATH = "/usr/bin/firefox"

class Mdw:
    def __init__(self, user):
        self.username = user.username
        self.password = user.password
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.binary_location = FIREFOX_PATH
        if not os.path.isfile(GECKODRIVER_PATH):
            print("Geckodriver not found")
        self.driver = webdriver.Firefox(service=Service(GECKODRIVER_PATH), options=options)

        self.db_manager = data_base_manager.DatabaseManager(DB_PATH)



    def login(self):
        self.driver.get(MDW_URL)
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def get_html(self):
        note_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//span[.//span[text()='Notes & résultats']]]"))
        )
        note_button.click()
        sem_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//span[.//span[text()='L3-Informatique (NANCY) (APP)']]]"))
        )
        sem_button.click()
        close_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//span[.//span[text()='Fermer']]]"))
        )
        close_button.click()
        html = self.driver.page_source
        self.driver.quit()
        return html

    def get_notes(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', {'class': 'v-window-wrap'})
        table = div.find('table', attrs={'class': 'v-table-table'})

        # Extraire les données des deux premières colonnes
        data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                nom_matiere = cols[1].get_text(strip=True)
                note = cols[2].get_text(strip=True)
                note = float(note) if note else None
                data.append((nom_matiere, note))
        return data

    def update_db(self):
        return self.db_manager.nouvelle_note(self.get_notes())

def main():
    with open("ressources/config.json") as f:
        config = json.load(f)
    user = Utilisateur(config.get('LOGIN'), config.get('PASSWORD'))
    mdw = Mdw(user)
    mdw.login()
    nouvelle_notes = mdw.update_db()

if __name__ == '__main__':
    main()
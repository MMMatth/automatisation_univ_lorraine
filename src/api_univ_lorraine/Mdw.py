import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from api_univ_lorraine.Utilisateur import Utilisateur

MDW_URL = "https://mdw.univ-lorraine.fr/"
GECKODRIVER_PATH = "ressources/geckodriver"
DB_PATH = "ressources/notes.db"
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
        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()


    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_matiere TEXT,
                note FLOAT
            )
        """)
        self.conn.commit()


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
        """
        Met à jour la base de données
        :return: list of tuples (nom_matiere, note)
        """
        new_data = self.get_notes()
        cursor = self.conn.cursor()

        cursor.execute("SELECT nom_matiere, note FROM notes")
        old_data = {row[0]: row[1] for row in cursor.fetchall()}
        result = []

        for matiere, note in new_data:
            if matiere not in old_data: # dans le cas où la matière n'est pas dans la base de données
                cursor.execute("INSERT INTO notes (nom_matiere, note) VALUES (?, ?)", (matiere, note))
                result.append((matiere, note))
            elif note is not None and note != old_data[matiere]:
                cursor.execute("UPDATE notes SET note = ? WHERE nom_matiere = ?", (note, matiere))
                result.append((matiere, note))

        self.conn.commit()
        return result

def main():
    user = Utilisateur("username", "password")
    mdw = Mdw(user)
    mdw.login()
    nouvelle_notes = mdw.update_db()
    print(nouvelle_notes)

if __name__ == '__main__':
    main()
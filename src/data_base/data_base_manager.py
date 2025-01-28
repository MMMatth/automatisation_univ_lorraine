import sqlite3
import logging
import os
import json

# Path to the configuration file
DATA_BASE = 'ressources/data.db'

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS channel (id INTEGER PRIMARY KEY, name TEXT, serv_name TEXT, serv_id INTEGER)")
            cursor.execute("CREATE TABLE IF NOT EXISTS notes (nom_matiere TEXT PRIMARY KEY, note TEXT)")
            con.commit()

    def save_channel(self, channel_id, channel_name, server_name, server_id):
        try:
            with sqlite3.connect(self.db_path) as con:
                cursor = con.cursor()
                is_present = cursor.execute("SELECT * FROM channel WHERE id = ?", (channel_id,)).fetchone()
                if is_present is not None:
                    logging.warning("Channel already exists")
                    return False
                cursor.execute("INSERT INTO channel (id, name, serv_name, serv_id) VALUES (?, ?, ?, ?)", (channel_id, channel_name, server_name, server_id))
                con.commit()
                return True
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return False

    def remove_channel(self, channel_id):
        try:
            with sqlite3.connect(self.db_path) as con:
                cursor = con.cursor()
                is_present = cursor.execute("SELECT * FROM channel WHERE id = ?", (channel_id,)).fetchone()
                if is_present is not None:
                    cursor.execute("DELETE FROM channel WHERE id = ?", (channel_id,))
                    con.commit()
                    return True
                logging.warning("Channel not found")
                return False
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return False

    def get_all_channels(self, only_id = False):
            try:
                with sqlite3.connect(self.db_path) as con:
                    cursor = con.cursor()
                    if only_id:
                        cursor.execute("SELECT id FROM channel")
                        return [row[0] for row in cursor.fetchall()]
                    cursor.execute("SELECT id, name, serv_name, serv_id FROM channel")
                    return cursor.fetchall()
            except sqlite3.Error as e:
                logging.error(f"Database error: {e}")
                return []

    def nouvelle_note(self, notes):
        try:
            with sqlite3.connect(self.db_path) as con:
                cursor = con.cursor()
                cursor.execute("SELECT nom_matiere, note FROM notes")
                old_data = {row[0]: row[1] for row in cursor.fetchall()}
                result = []
                for matiere, note in notes:
                    if matiere not in old_data and note is not None: # nouvelle note
                        cursor.execute("INSERT INTO notes (nom_matiere, note) VALUES (?, ?)", (matiere, note))
                        result.append((matiere, note))
                    if matiere in old_data :
                        if note is not None and str(note) != old_data[matiere]:
                            cursor.execute("UPDATE notes SET note = ? WHERE nom_matiere = ?", (note, matiere))
                            result.append((matiere, note))
                con.commit()
                return result
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return []

if __name__ == '__main__':
    db_manager = DatabaseManager(DATA_BASE)
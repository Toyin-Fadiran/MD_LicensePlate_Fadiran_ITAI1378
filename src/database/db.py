import sqlite3


class Database:

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()


    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS authorized_vehicles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT UNIQUE NOT NULL,
            owner TEXT,
            vehicle TEXT,
            active BOOLEAN DEFAULT TRUE

        )
        """)


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT,
            ocr_confidence REAL,
            authorized BOOLEAN,
            detected_at TIMESTAMP

        )
        """)


        self.connection.commit()


    def close(self):
        self.connection.close()
import sqlite3
from pathlib import Path
from src.config import DATABASE_PATH # <-- Import it here

class Database:
    # Set the config path as the default argument
    def __init__(self, db_path=DATABASE_PATH):
        # 1. Ensure it's a Path object
        path_obj = Path(db_path)
        
        # 2. Defensive failsafe: Ensure the db_data directory actually exists
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # 3. Connect
        self.connection = sqlite3.connect(path_obj)
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
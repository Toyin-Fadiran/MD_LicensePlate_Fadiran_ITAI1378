import datetime
import pandas as pd
from src.config import PROJECT_ROOT, CSV_FILE_PATH


def seed_database(db, csv_path=CSV_FILE_PATH):
    print(f"Loading authorized vehicles from {csv_path}...")
    
    df = pd.read_csv(csv_path)
    
    count = 0
    for index, row in df.iterrows():
        plate = str(row['license_plate']).strip().upper()
        
        add_authorized_vehicle(
            db, 
            plate=plate, 
            owner=row['owner'], 
            vehicle=row['vehicle']
        )
        count += 1
        
    print(f"Successfully seeded {count} vehicles!")


def log_detection(db, plate, confidence, authorized):
    db.cursor.execute(
        """
        INSERT INTO detections 
        (license_plate, ocr_confidence, authorized, detected_at)
        VALUES (?, ?, ?, ?)
        """,
        (plate, confidence, authorized, datetime.datetime.now())
    )
    db.connection.commit()

def add_authorized_vehicle(db, plate, owner, vehicle):

    db.cursor.execute(
        """
        INSERT OR IGNORE INTO authorized_vehicles
        (license_plate, owner, vehicle)

        VALUES (?, ?, ?)
        """,
        (plate, owner, vehicle)
    )

    db.connection.commit()



def check_vehicle(db, plate):

    result = db.cursor.execute(
        """
        SELECT *
        FROM authorized_vehicles
        WHERE license_plate = ?
        """,
        (plate,)
    ).fetchone()


    return result
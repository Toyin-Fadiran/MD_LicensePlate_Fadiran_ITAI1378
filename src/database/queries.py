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
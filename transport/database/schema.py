from transport.database.connection import Database


# 1. Create every table and index the application needs
def createTables(database: Database) -> None:
    database.run("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT NOT NULL,
            vehicle_number TEXT NOT NULL UNIQUE,
            capacity INTEGER NOT NULL CHECK (capacity > 0)
        );
    """)
    database.run("""
        CREATE TABLE IF NOT EXISTS drivers (
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            driver_phone TEXT NOT NULL,
            license_number TEXT NOT NULL UNIQUE
        );
    """)
    database.run("""
        CREATE TABLE IF NOT EXISTS trips (
            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            trip_date TEXT NOT NULL,
            duration TEXT NOT NULL,
            duration_seconds INTEGER NOT NULL CHECK (duration_seconds > 0),
            pickup_location TEXT NOT NULL,
            drop_location TEXT NOT NULL,
            total_sum REAL NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
            FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
        );
    """)
    database.run("CREATE INDEX IF NOT EXISTS idx_trips_date ON trips(trip_date);")
    database.run("CREATE INDEX IF NOT EXISTS idx_trips_driver ON trips(driver_id);")
    database.run("CREATE INDEX IF NOT EXISTS idx_trips_vehicle ON trips(vehicle_id);")

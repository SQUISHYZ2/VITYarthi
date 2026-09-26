import sqlite3

from transport.logger import getLogger

logger = getLogger("transport.database")


# 1. Thin wrapper around the SQLite connection with logging and safe transactions
class Database:
    def __init__(self, path: str):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON;")
        logger.info(f"Connected to database at {path}.")

    def run(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        try:
            with self.connection:
                return self.connection.execute(query, params)
        except sqlite3.IntegrityError as error:
            logger.warning(f"Integrity error: {error}")
            raise ValueError(f"The data conflicts with existing records: {error}.")
        except sqlite3.Error as error:
            logger.error(f"Database error: {error}")
            raise

    def fetchAll(self, query: str, params: tuple = ()) -> list:
        return self.run(query, params).fetchall()

    def fetchOne(self, query: str, params: tuple = ()) -> sqlite3.Row | None:
        return self.run(query, params).fetchone()

    def close(self) -> None:
        self.connection.close()
        logger.info("Database connection closed.")

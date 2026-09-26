import sqlite3

from transport.config import databasePath
from transport.database import Database, createTables
from transport.logger import getLogger
from transport.services.fleet_service import FleetService
from transport.services.report_service import ReportService
from transport.services.trip_service import TripService
from transport.ui.fleet_menu import fleetMenu
from transport.ui.inputs import readInt
from transport.ui.report_menu import reportMenu
from transport.ui.trip_menu import tripMenu

logger = getLogger("transport.ui")


# 1. Main menu that ties the three modules together
def mainMenu() -> str:
    try:
        database = Database(databasePath)
        createTables(database)
    except sqlite3.Error as e:
        logger.error(f"Failed to start: {e}")
        return f"Failed to connect to database: {e}\nTerminating Program."
    fleetService = FleetService(database)
    tripService = TripService(database)
    reportService = ReportService(database)
    message = "Welcome Admin!"
    while True:
        print(message)
        try:
            ch = readInt("1. Fleet Management\n2. Trips And Billing\n3. Reports\n4. Exit\nEnter your choice: ")
            match ch:
                case 1: message = fleetMenu(fleetService)
                case 2: message = tripMenu(tripService)
                case 3: message = reportMenu(reportService)
                case 4:
                    database.close()
                    return "Thank you for visiting!\nTerminating Program."
                case _: message = "Invalid choice!"
        except (ValueError, sqlite3.Error) as e:
            message = f"An error occurred: {e}"
        except (KeyboardInterrupt, EOFError):
            database.close()
            return "\nTerminating Program."

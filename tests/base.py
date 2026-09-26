import unittest

from transport.database import Database, createTables
from transport.services.fleet_service import FleetService
from transport.services.report_service import ReportService
from transport.services.trip_service import TripService


# 1. Shared in-memory database fixture for the service tests
class DatabaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.database = Database(":memory:")
        createTables(self.database)
        self.fleetService = FleetService(self.database)
        self.tripService = TripService(self.database)
        self.reportService = ReportService(self.database)
        self.vehicle = self.fleetService.addVehicle("Bus", "KA01AB1234", 40)
        self.driver = self.fleetService.addDriver("Ravi Kumar", "9876543210", "DL-1234567")

    def tearDown(self) -> None:
        self.database.close()

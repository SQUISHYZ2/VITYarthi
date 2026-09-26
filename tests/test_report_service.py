import csv
import os
import tempfile

from tests.base import DatabaseTestCase


class TestReportService(DatabaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.secondDriver = self.fleetService.addDriver("Sita Rao", "9123456780", "MH-7654321")
        self.tripService.addTrip(self.vehicle.vehicleId, self.driver.driverId, "2026-03-01", "01:00:00", "Airport", "Station")
        self.tripService.addTrip(self.vehicle.vehicleId, self.driver.driverId, "2026-03-02", "02:00:00", "airport", "station")
        self.tripService.addTrip(self.vehicle.vehicleId, self.secondDriver.driverId, "2026-04-01", "00:30:00", "Mall", "Park")

    def testRevenueSummary(self):
        summary = self.reportService.revenueSummary("2026-03-01", "2026-03-31")
        self.assertEqual(summary["trips"], 2)
        self.assertEqual(summary["revenue"], 1500.0)
        self.assertEqual(summary["totalDuration"], "03:00:00")
        self.assertEqual(summary["averageRevenue"], 750.0)

    def testRevenueSummaryOfEmptyPeriod(self):
        summary = self.reportService.revenueSummary("2025-01-01", "2025-01-31")
        self.assertEqual(summary, {"trips": 0, "revenue": 0.0, "totalDuration": "00:00:00", "averageRevenue": 0.0})

    def testEarningsByDriverAreRanked(self):
        rows = self.reportService.earningsByDriver()
        self.assertEqual(rows[0], (self.driver.driverId, "Ravi Kumar", 2, 1500.0))
        self.assertEqual(rows[1], (self.secondDriver.driverId, "Sita Rao", 1, 250.0))

    def testEarningsByVehicle(self):
        rows = self.reportService.earningsByVehicle()
        self.assertEqual(rows, [(self.vehicle.vehicleId, "KA01AB1234", 3, "03:30:00", 1750.0)])

    def testTopRoutesIgnoreCase(self):
        rows = self.reportService.topRoutes(1)
        self.assertEqual(rows[0][2:], (2, 1500.0))
        with self.assertRaises(ValueError):
            self.reportService.topRoutes(0)

    def testExportToCsv(self):
        with tempfile.TemporaryDirectory() as folder:
            filePath = os.path.join(folder, "trips.csv")
            self.assertEqual(self.reportService.exportTripsToCsv(filePath), 3)
            with open(filePath, "r", newline="", encoding="utf-8") as newFile:
                rows = list(csv.reader(newFile))
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0][0], "trip_id")

from tests.base import DatabaseTestCase


class TestFleetService(DatabaseTestCase):
    def testAddedVehicleCanBeFetched(self):
        vehicle = self.fleetService.getVehicle(self.vehicle.vehicleId)
        self.assertEqual(vehicle.vehicleNumber, "KA01AB1234")
        self.assertEqual(vehicle.capacity, 40)
        self.assertEqual(len(self.fleetService.getVehicles()), 1)

    def testDuplicateVehicleNumberRejected(self):
        with self.assertRaises(ValueError):
            self.fleetService.addVehicle("Van", "ka01ab1234", 8)

    def testDuplicateLicenseRejected(self):
        with self.assertRaises(ValueError):
            self.fleetService.addDriver("Sita Rao", "9123456780", "DL-1234567")

    def testInvalidVehicleRejectedAndNothingSaved(self):
        with self.assertRaises(ValueError):
            self.fleetService.addVehicle("Van", "MH12XY9999", 0)
        self.assertEqual(len(self.fleetService.getVehicles()), 1)

    def testSqlInjectionIsStoredAsPlainText(self):
        vehicle = self.fleetService.addVehicle("Bus'); DROP TABLE vehicles;--", "TN09CD5678", 20)
        self.assertEqual(self.fleetService.getVehicle(vehicle.vehicleId).vehicleType, "Bus'); DROP TABLE vehicles;--")
        self.assertEqual(len(self.fleetService.getVehicles()), 2)

    def testUpdates(self):
        self.assertEqual(self.fleetService.updateVehicleCapacity(self.vehicle.vehicleId, 55).capacity, 55)
        self.assertEqual(self.fleetService.updateDriverPhone(self.driver.driverId, "9000000000").driverPhone, "9000000000")

    def testMissingRecordsRaise(self):
        with self.assertRaises(ValueError):
            self.fleetService.getVehicle(999)
        with self.assertRaises(ValueError):
            self.fleetService.getDriver(999)

    def testDeleteUnusedRecords(self):
        self.fleetService.deleteVehicle(self.vehicle.vehicleId)
        self.fleetService.deleteDriver(self.driver.driverId)
        self.assertEqual(self.fleetService.getVehicles(), [])
        self.assertEqual(self.fleetService.getDrivers(), [])

    def testCannotDeleteRecordsWithTrips(self):
        self.tripService.addTrip(self.vehicle.vehicleId, self.driver.driverId, "2026-03-01", "01:00:00", "A", "B")
        with self.assertRaises(ValueError):
            self.fleetService.deleteVehicle(self.vehicle.vehicleId)
        with self.assertRaises(ValueError):
            self.fleetService.deleteDriver(self.driver.driverId)

from tests.base import DatabaseTestCase


class TestTripService(DatabaseTestCase):
    def addTrip(self, tripDate: str = "2026-03-01", tripTime: str = "01:30:00", pickup: str = "Airport", drop: str = "Station"):
        return self.tripService.addTrip(self.vehicle.vehicleId, self.driver.driverId, tripDate, tripTime, pickup, drop)

    def testTripIsBilledAtHourlyRate(self):
        trip = self.addTrip(tripTime="01:30:00")
        self.assertEqual(trip.totalSum, 750.0)
        self.assertEqual(self.tripService.getTrips()[0].totalSum, 750.0)

    def testUnknownVehicleOrDriverRejected(self):
        with self.assertRaises(ValueError):
            self.tripService.addTrip(99, self.driver.driverId, "2026-03-01", "01:00:00", "A", "B")
        with self.assertRaises(ValueError):
            self.tripService.addTrip(self.vehicle.vehicleId, 99, "2026-03-01", "01:00:00", "A", "B")

    def testInvalidInputsRejected(self):
        with self.assertRaises(ValueError):
            self.addTrip(tripDate="2026-13-01")
        with self.assertRaises(ValueError):
            self.addTrip(tripTime="90 minutes")
        with self.assertRaises(ValueError):
            self.addTrip(pickup="Airport", drop="airport")
        self.assertEqual(self.tripService.getTrips(), [])

    def testTripsBetweenDatesIsInclusive(self):
        self.addTrip(tripDate="2026-03-01")
        self.addTrip(tripDate="2026-03-15")
        self.addTrip(tripDate="2026-04-01")
        trips = self.tripService.getTripsBetween("2026-03-01", "2026-03-31")
        self.assertEqual([trip.tripDate for trip in trips], ["2026-03-01", "2026-03-15"])

    def testDeleteTrip(self):
        trip = self.addTrip()
        self.tripService.deleteTrip(trip.tripId)
        self.assertEqual(self.tripService.getTrips(), [])
        with self.assertRaises(ValueError):
            self.tripService.deleteTrip(trip.tripId)

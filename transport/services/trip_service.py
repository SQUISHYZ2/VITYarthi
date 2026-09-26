from transport.database import Database
from transport.logger import getLogger
from transport.models import Trip
from transport.services.billing import calculateTotalSum, durationToSeconds, secondsToDuration
from transport.services.fleet_service import FleetService
from transport.services.validators import validateDate, validateDateRange, validateText

logger = getLogger("transport.trips")


# 1. Trip booking and billing
class TripService:
    def __init__(self, database: Database):
        self.database = database
        self.fleetService = FleetService(database)

    def addTrip(self, vehicleId: int, driverId: int, tripDate: str, tripTime: str,
                pickupLocation: str, dropLocation: str) -> Trip:
        self.fleetService.getVehicle(vehicleId)
        self.fleetService.getDriver(driverId)
        tripDate = validateDate(tripDate)
        pickupLocation = validateText(pickupLocation, "Pickup location")
        dropLocation = validateText(dropLocation, "Drop location")
        if pickupLocation.lower() == dropLocation.lower():
            raise ValueError("Pickup and drop locations cannot be the same.")
        totalSeconds = durationToSeconds(tripTime)
        duration = secondsToDuration(totalSeconds)
        totalSum = calculateTotalSum(duration)
        cursor = self.database.run("""
            INSERT INTO trips (vehicle_id, driver_id, trip_date, duration, duration_seconds,
                               pickup_location, drop_location, total_sum)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (vehicleId, driverId, tripDate, duration, totalSeconds, pickupLocation, dropLocation, totalSum))
        logger.info(f"Trip {cursor.lastrowid} added with total sum {totalSum}.")
        return Trip(cursor.lastrowid, vehicleId, driverId, tripDate, duration, pickupLocation, dropLocation, totalSum)

    def getTrips(self) -> list:
        rows = self.database.fetchAll("SELECT * FROM trips ORDER BY trip_date, trip_id;")
        return [Trip.fromRow(row) for row in rows]

    def getTripsBetween(self, startDate: str, endDate: str) -> list:
        startDate, endDate = validateDateRange(startDate, endDate)
        rows = self.database.fetchAll(
            "SELECT * FROM trips WHERE trip_date BETWEEN ? AND ? ORDER BY trip_date, trip_id;",
            (startDate, endDate))
        return [Trip.fromRow(row) for row in rows]

    def deleteTrip(self, tripId: int) -> None:
        if self.database.fetchOne("SELECT 1 FROM trips WHERE trip_id = ?;", (tripId,)) is None:
            raise ValueError(f"No trip found with ID {tripId}.")
        self.database.run("DELETE FROM trips WHERE trip_id = ?;", (tripId,))
        logger.info(f"Trip {tripId} deleted.")

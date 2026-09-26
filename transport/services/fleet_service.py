from transport.database import Database
from transport.logger import getLogger
from transport.models import Driver, Vehicle
from transport.services.validators import (validateCapacity, validateLicenseNumber, validateName,
                                           validatePhone, validateText, validateVehicleNumber)

logger = getLogger("transport.fleet")


# 1. Vehicle and driver management
class FleetService:
    def __init__(self, database: Database):
        self.database = database

    def addVehicle(self, vehicleType: str, vehicleNumber: str, capacity: int) -> Vehicle:
        vehicleType = validateText(vehicleType, "Vehicle type", 40)
        vehicleNumber = validateVehicleNumber(vehicleNumber)
        capacity = validateCapacity(capacity)
        cursor = self.database.run(
            "INSERT INTO vehicles (vehicle_type, vehicle_number, capacity) VALUES (?, ?, ?);",
            (vehicleType, vehicleNumber, capacity))
        logger.info(f"Vehicle {vehicleNumber} added.")
        return Vehicle(cursor.lastrowid, vehicleType, vehicleNumber, capacity)

    def getVehicles(self) -> list:
        rows = self.database.fetchAll("SELECT * FROM vehicles ORDER BY vehicle_id;")
        return [Vehicle.fromRow(row) for row in rows]

    def getVehicle(self, vehicleId: int) -> Vehicle:
        row = self.database.fetchOne("SELECT * FROM vehicles WHERE vehicle_id = ?;", (vehicleId,))
        if row is None:
            raise ValueError(f"No vehicle found with ID {vehicleId}.")
        return Vehicle.fromRow(row)

    def updateVehicleCapacity(self, vehicleId: int, capacity: int) -> Vehicle:
        self.getVehicle(vehicleId)
        capacity = validateCapacity(capacity)
        self.database.run("UPDATE vehicles SET capacity = ? WHERE vehicle_id = ?;", (capacity, vehicleId))
        logger.info(f"Vehicle {vehicleId} capacity changed to {capacity}.")
        return self.getVehicle(vehicleId)

    def deleteVehicle(self, vehicleId: int) -> None:
        self.getVehicle(vehicleId)
        if self.database.fetchOne("SELECT 1 FROM trips WHERE vehicle_id = ?;", (vehicleId,)):
            raise ValueError("This vehicle has recorded trips and cannot be deleted.")
        self.database.run("DELETE FROM vehicles WHERE vehicle_id = ?;", (vehicleId,))
        logger.info(f"Vehicle {vehicleId} deleted.")

    def addDriver(self, driverName: str, driverPhone: str, licenseNumber: str) -> Driver:
        driverName = validateName(driverName, "Driver name")
        driverPhone = validatePhone(driverPhone)
        licenseNumber = validateLicenseNumber(licenseNumber)
        cursor = self.database.run(
            "INSERT INTO drivers (driver_name, driver_phone, license_number) VALUES (?, ?, ?);",
            (driverName, driverPhone, licenseNumber))
        logger.info(f"Driver {driverName} added.")
        return Driver(cursor.lastrowid, driverName, driverPhone, licenseNumber)

    def getDrivers(self) -> list:
        rows = self.database.fetchAll("SELECT * FROM drivers ORDER BY driver_id;")
        return [Driver.fromRow(row) for row in rows]

    def getDriver(self, driverId: int) -> Driver:
        row = self.database.fetchOne("SELECT * FROM drivers WHERE driver_id = ?;", (driverId,))
        if row is None:
            raise ValueError(f"No driver found with ID {driverId}.")
        return Driver.fromRow(row)

    def updateDriverPhone(self, driverId: int, driverPhone: str) -> Driver:
        self.getDriver(driverId)
        driverPhone = validatePhone(driverPhone)
        self.database.run("UPDATE drivers SET driver_phone = ? WHERE driver_id = ?;", (driverPhone, driverId))
        logger.info(f"Driver {driverId} phone updated.")
        return self.getDriver(driverId)

    def deleteDriver(self, driverId: int) -> None:
        self.getDriver(driverId)
        if self.database.fetchOne("SELECT 1 FROM trips WHERE driver_id = ?;", (driverId,)):
            raise ValueError("This driver has recorded trips and cannot be deleted.")
        self.database.run("DELETE FROM drivers WHERE driver_id = ?;", (driverId,))
        logger.info(f"Driver {driverId} deleted.")

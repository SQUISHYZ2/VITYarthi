class Driver:
    def __init__(self, driverId: int, driverName: str, driverPhone: str, licenseNumber: str):
        self.driverId = driverId
        self.driverName = driverName
        self.driverPhone = driverPhone
        self.licenseNumber = licenseNumber

    @staticmethod
    def fromRow(row) -> "Driver":
        return Driver(row["driver_id"], row["driver_name"], row["driver_phone"], row["license_number"])

    def __str__(self) -> str:
        return (f"Driver ID: {self.driverId}\nDriver Name: {self.driverName}\n"
                f"Driver Phone: {self.driverPhone}\nLicense Number: {self.licenseNumber}")

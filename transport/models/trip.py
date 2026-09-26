class Trip:
    def __init__(self, tripId: int, vehicleId: int, driverId: int, tripDate: str, duration: str,
                 pickupLocation: str, dropLocation: str, totalSum: float):
        self.tripId = tripId
        self.vehicleId = vehicleId
        self.driverId = driverId
        self.tripDate = tripDate
        self.duration = duration
        self.pickupLocation = pickupLocation
        self.dropLocation = dropLocation
        self.totalSum = totalSum

    @staticmethod
    def fromRow(row) -> "Trip":
        return Trip(row["trip_id"], row["vehicle_id"], row["driver_id"], row["trip_date"], row["duration"],
                    row["pickup_location"], row["drop_location"], row["total_sum"])

    def __str__(self) -> str:
        return (f"Trip ID: {self.tripId}\nVehicle ID: {self.vehicleId}\nDriver ID: {self.driverId}\n"
                f"Trip Date: {self.tripDate}\nTrip Duration: {self.duration}\n"
                f"Pickup Location: {self.pickupLocation}\nDrop Location: {self.dropLocation}\n"
                f"Total Sum earned: {self.totalSum:.2f}")

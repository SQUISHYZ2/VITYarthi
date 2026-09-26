class Vehicle:
    def __init__(self, vehicleId: int, vehicleType: str, vehicleNumber: str, capacity: int):
        self.vehicleId = vehicleId
        self.vehicleType = vehicleType
        self.vehicleNumber = vehicleNumber
        self.capacity = capacity

    @staticmethod
    def fromRow(row) -> "Vehicle":
        return Vehicle(row["vehicle_id"], row["vehicle_type"], row["vehicle_number"], row["capacity"])

    def __str__(self) -> str:
        return (f"Vehicle ID: {self.vehicleId}\nVehicle Type: {self.vehicleType}\n"
                f"Vehicle Number: {self.vehicleNumber}\nCapacity: {self.capacity}")

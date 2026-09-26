from transport.services.fleet_service import FleetService
from transport.ui.inputs import formatRecords, readInt


# 1. Menu for vehicle and driver management
def fleetMenu(fleetService: FleetService) -> str:
    ch = readInt("1. Add Vehicle\n2. Add Driver\n3. Display Vehicles\n4. Display Drivers\n"
                 "5. Update Vehicle Capacity\n6. Update Driver Phone\n7. Delete Vehicle\n8. Delete Driver\n9. Back\n"
                 "Enter your choice: ")
    match ch:
        case 1:
            vehicleType = input("Enter vehicle type: ")
            vehicleNumber = input("Enter vehicle number: ")
            capacity = readInt("Enter capacity: ")
            vehicle = fleetService.addVehicle(vehicleType, vehicleNumber, capacity)
            return f"Vehicle added successfully with ID {vehicle.vehicleId}."
        case 2:
            driverName = input("Enter driver name: ")
            driverPhone = input("Enter driver phone: ")
            licenseNumber = input("Enter license number: ")
            driver = fleetService.addDriver(driverName, driverPhone, licenseNumber)
            return f"Driver added successfully with ID {driver.driverId}."
        case 3: return formatRecords(fleetService.getVehicles(), "No vehicles found.")
        case 4: return formatRecords(fleetService.getDrivers(), "No drivers found.")
        case 5:
            vehicleId = readInt("Enter vehicle ID: ")
            capacity = readInt("Enter new capacity: ")
            return str(fleetService.updateVehicleCapacity(vehicleId, capacity))
        case 6:
            driverId = readInt("Enter driver ID: ")
            driverPhone = input("Enter new phone number: ")
            return str(fleetService.updateDriverPhone(driverId, driverPhone))
        case 7:
            fleetService.deleteVehicle(readInt("Enter vehicle ID: "))
            return "Vehicle deleted successfully."
        case 8:
            fleetService.deleteDriver(readInt("Enter driver ID: "))
            return "Driver deleted successfully."
        case 9: return "Returning to main menu."
        case _: return "Invalid choice!"

from transport.services.trip_service import TripService
from transport.ui.inputs import formatRecords, readInt


# 1. Menu for trip booking and billing
def tripMenu(tripService: TripService) -> str:
    ch = readInt("1. Add Trip\n2. Display All Trips\n3. Display Trips Between Dates\n4. Delete Trip\n5. Back\n"
                 "Enter your choice: ")
    match ch:
        case 1:
            vehicleId = readInt("Enter vehicle ID: ")
            driverId = readInt("Enter driver ID: ")
            tripDate = input("Enter trip date (YYYY-MM-DD): ")
            tripTime = input("Enter trip time (HH:MM:SS): ")
            pickupLocation = input("Enter pickup location: ")
            dropLocation = input("Enter drop location: ")
            trip = tripService.addTrip(vehicleId, driverId, tripDate, tripTime, pickupLocation, dropLocation)
            return f"Trip added successfully.\nTotal sum earned: {trip.totalSum:.2f}"
        case 2: return formatRecords(tripService.getTrips(), "No trips found.")
        case 3:
            startDate = input("Enter start date (YYYY-MM-DD): ")
            endDate = input("Enter end date (YYYY-MM-DD): ")
            return formatRecords(tripService.getTripsBetween(startDate, endDate), "No trips found in that period.")
        case 4:
            tripService.deleteTrip(readInt("Enter trip ID: "))
            return "Trip deleted successfully."
        case 5: return "Returning to main menu."
        case _: return "Invalid choice!"

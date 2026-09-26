from transport.services.report_service import ReportService
from transport.ui.inputs import readInt


# 1. Menu for reports and analytics
def reportMenu(reportService: ReportService) -> str:
    ch = readInt("1. Revenue Summary\n2. Earnings By Driver\n3. Earnings By Vehicle\n4. Top Routes\n"
                 "5. Export Trips To CSV\n6. Back\nEnter your choice: ")
    match ch:
        case 1:
            startDate = input("Enter start date (YYYY-MM-DD): ")
            endDate = input("Enter end date (YYYY-MM-DD): ")
            summary = reportService.revenueSummary(startDate, endDate)
            return (f"Trips: {summary['trips']}\nTotal revenue: {summary['revenue']:.2f}\n"
                    f"Total duration: {summary['totalDuration']}\nAverage per trip: {summary['averageRevenue']:.2f}")
        case 2:
            rows = reportService.earningsByDriver()
            return "\n".join(f"Driver {driverId} ({driverName}): {trips} trips, {revenue:.2f} earned."
                             for driverId, driverName, trips, revenue in rows) or "No drivers found."
        case 3:
            rows = reportService.earningsByVehicle()
            return "\n".join(f"Vehicle {vehicleId} ({vehicleNumber}): {trips} trips, {duration} driven, {revenue:.2f} earned."
                             for vehicleId, vehicleNumber, trips, duration, revenue in rows) or "No vehicles found."
        case 4:
            rows = reportService.topRoutes()
            return "\n".join(f"{pickup} to {drop}: {trips} trips, {revenue:.2f} earned."
                             for pickup, drop, trips, revenue in rows) or "No trips found."
        case 5:
            fileName = input("Enter file name: ").strip() or "trips"
            count = reportService.exportTripsToCsv(f"{fileName}.csv")
            return f"Exported {count} trips to {fileName}.csv."
        case 6: return "Returning to main menu."
        case _: return "Invalid choice!"

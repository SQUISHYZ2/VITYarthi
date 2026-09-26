import csv

from transport.database import Database
from transport.logger import getLogger
from transport.services.billing import secondsToDuration
from transport.services.validators import validateDateRange

logger = getLogger("transport.reports")


# 1. Reporting and analytics
class ReportService:
    def __init__(self, database: Database):
        self.database = database

    def revenueSummary(self, startDate: str, endDate: str) -> dict:
        startDate, endDate = validateDateRange(startDate, endDate)
        row = self.database.fetchOne("""
            SELECT COUNT(*) AS trips, COALESCE(SUM(total_sum), 0) AS revenue,
                   COALESCE(SUM(duration_seconds), 0) AS seconds
            FROM trips WHERE trip_date BETWEEN ? AND ?;
        """, (startDate, endDate))
        averageRevenue = round(row["revenue"] / row["trips"], 2) if row["trips"] else 0.0
        return {
            "trips": row["trips"],
            "revenue": round(row["revenue"], 2),
            "totalDuration": secondsToDuration(row["seconds"]),
            "averageRevenue": averageRevenue,
        }

    def earningsByDriver(self) -> list:
        rows = self.database.fetchAll("""
            SELECT d.driver_id, d.driver_name, COUNT(t.trip_id) AS trips, COALESCE(SUM(t.total_sum), 0) AS revenue
            FROM drivers d LEFT JOIN trips t ON t.driver_id = d.driver_id
            GROUP BY d.driver_id ORDER BY revenue DESC, d.driver_id;
        """)
        return [(row["driver_id"], row["driver_name"], row["trips"], round(row["revenue"], 2)) for row in rows]

    def earningsByVehicle(self) -> list:
        rows = self.database.fetchAll("""
            SELECT v.vehicle_id, v.vehicle_number, COUNT(t.trip_id) AS trips,
                   COALESCE(SUM(t.duration_seconds), 0) AS seconds, COALESCE(SUM(t.total_sum), 0) AS revenue
            FROM vehicles v LEFT JOIN trips t ON t.vehicle_id = v.vehicle_id
            GROUP BY v.vehicle_id ORDER BY revenue DESC, v.vehicle_id;
        """)
        return [(row["vehicle_id"], row["vehicle_number"], row["trips"],
                 secondsToDuration(row["seconds"]), round(row["revenue"], 2)) for row in rows]

    def topRoutes(self, limit: int = 3) -> list:
        if limit <= 0:
            raise ValueError("Limit must be a positive number.")
        rows = self.database.fetchAll("""
            SELECT pickup_location, drop_location, COUNT(*) AS trips, SUM(total_sum) AS revenue
            FROM trips GROUP BY LOWER(pickup_location), LOWER(drop_location)
            ORDER BY trips DESC, revenue DESC LIMIT ?;
        """, (limit,))
        return [(row["pickup_location"], row["drop_location"], row["trips"], round(row["revenue"], 2)) for row in rows]

    def exportTripsToCsv(self, filePath: str) -> int:
        rows = self.database.fetchAll("SELECT * FROM trips ORDER BY trip_date, trip_id;")
        with open(filePath, "w", newline="", encoding="utf-8") as newFile:
            writer = csv.writer(newFile)
            writer.writerow(["trip_id", "vehicle_id", "driver_id", "trip_date", "duration",
                             "pickup_location", "drop_location", "total_sum"])
            for row in rows:
                writer.writerow([row["trip_id"], row["vehicle_id"], row["driver_id"], row["trip_date"],
                                 row["duration"], row["pickup_location"], row["drop_location"], row["total_sum"]])
        logger.info(f"Exported {len(rows)} trips to {filePath}.")
        return len(rows)

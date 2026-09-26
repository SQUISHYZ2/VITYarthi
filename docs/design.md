# Design Document

## Objectives
- Replace manual record keeping with a validated database.
- Calculate trip fares automatically and consistently.
- Give the owner a clear view of earnings.

## Functional requirements
| ID | Module | Requirement |
|----|--------|-------------|
| F1 | Fleet | Add, list, update and delete vehicles and drivers; vehicle and licence numbers are unique. |
| F2 | Trips | Record a trip for an existing vehicle and driver; total sum = duration in hours x rate per hour. |
| F3 | Trips | List all trips, list trips between two dates, delete a trip. |
| F4 | Reports | Revenue summary for a date range, earnings per driver and per vehicle, top routes. |
| F5 | Reports | Export all trips to a CSV file. |

## Non-functional requirements
| Type | How it is met |
|------|---------------|
| Security | Every query is parameterised (no SQL injection, covered by a test); no credentials are stored or needed. |
| Reliability | Every write runs in a transaction; foreign keys and CHECK constraints protect data integrity; records with trips cannot be deleted. |
| Usability | Numbered menus, friendly messages, clear error text, and a bad entry never ends the program. |
| Maintainability | Layered packages (database, models, services, ui), small typed functions, no logic in the UI layer. |
| Error handling | Validation raises `ValueError` with a full sentence; the menu catches errors and shows them. |
| Logging | Actions, warnings and database errors go to `logs/transport.log`. |
| Testability | Services take a `Database` object, so tests use an in-memory database. |

## System architecture
```mermaid
flowchart TB
    UI["ui: main_menu, fleet_menu, trip_menu, report_menu"] --> S
    subgraph S["services"]
        F[FleetService]
        T[TripService]
        R[ReportService]
        V[validators]
        B[billing]
    end
    F --> V
    T --> V
    T --> B
    T --> F
    R --> V
    S --> M[models]
    S --> D["database: Database, schema"]
    D --> DB[(SQLite file)]
    S --> L[logger]
```

## Workflow
```mermaid
flowchart TD
    A[Start] --> B[Open database and create tables]
    B --> C{Main menu}
    C -->|1| D[Fleet management]
    C -->|2| E[Trips and billing]
    C -->|3| F[Reports]
    C -->|4| G[Close database and exit]
    D --> C
    E --> C
    F --> C
    C -->|error| H[Show message] --> C
```

## Use case diagram
```mermaid
flowchart LR
    Admin((Admin))
    Admin --> U1[Manage vehicles]
    Admin --> U2[Manage drivers]
    Admin --> U3[Record trip]
    Admin --> U4[View trips by date]
    Admin --> U5[View revenue reports]
    Admin --> U6[Export trips to CSV]
    U3 -.includes.-> U7[Calculate total sum]
```

## Class diagram
```mermaid
classDiagram
    class Database {
        +run(query, params)
        +fetchAll(query, params)
        +fetchOne(query, params)
        +close()
    }
    class FleetService {
        +addVehicle()
        +addDriver()
        +getVehicles()
        +getDrivers()
        +updateVehicleCapacity()
        +updateDriverPhone()
        +deleteVehicle()
        +deleteDriver()
    }
    class TripService {
        +addTrip()
        +getTrips()
        +getTripsBetween()
        +deleteTrip()
    }
    class ReportService {
        +revenueSummary()
        +earningsByDriver()
        +earningsByVehicle()
        +topRoutes()
        +exportTripsToCsv()
    }
    class Vehicle
    class Driver
    class Trip
    FleetService --> Database
    TripService --> Database
    TripService --> FleetService
    ReportService --> Database
    FleetService ..> Vehicle
    FleetService ..> Driver
    TripService ..> Trip
```

## Sequence diagram: adding a trip
```mermaid
sequenceDiagram
    actor Admin
    participant Menu as trip_menu
    participant TS as TripService
    participant FS as FleetService
    participant Bill as billing
    participant DB as Database
    Admin->>Menu: vehicle ID, driver ID, date, time, locations
    Menu->>TS: addTrip(...)
    TS->>FS: getVehicle(), getDriver()
    FS->>DB: SELECT
    TS->>Bill: calculateTotalSum(time)
    Bill-->>TS: total sum
    TS->>DB: INSERT trip
    TS-->>Menu: Trip
    Menu-->>Admin: Trip added, total sum earned
```

## ER diagram
```mermaid
erDiagram
    VEHICLES ||--o{ TRIPS : "used in"
    DRIVERS ||--o{ TRIPS : "drives"
    VEHICLES {
        int vehicle_id PK
        text vehicle_type
        text vehicle_number UK
        int capacity
    }
    DRIVERS {
        int driver_id PK
        text driver_name
        text driver_phone
        text license_number UK
    }
    TRIPS {
        int trip_id PK
        int vehicle_id FK
        int driver_id FK
        text trip_date
        text duration
        int duration_seconds
        text pickup_location
        text drop_location
        real total_sum
    }
```

## Design decisions
- **SQLite instead of MySQL**: the original idea was to use a MySQL server and a root password. SQLite ships with Python, so the project runs anywhere, and tests can use an in-memory database.
- **Service layer**: all rules live in services, so the menus only read input and print output.
- **`duration_seconds` column**: durations are stored as text for display and as seconds for fast, exact aggregation in reports.
- **Deletion guard**: vehicles and drivers with recorded trips cannot be deleted, so earnings history is never lost.

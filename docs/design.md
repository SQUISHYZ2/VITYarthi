# Design Document

Diagrams were designed in Figma. The PNG files are in [diagrams/](diagrams/).

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
![System architecture](diagrams/01_system_architecture.png)

## Workflow
![Workflow](diagrams/02_workflow.png)

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
![Class diagram](diagrams/04_class_diagram.png)

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
![ER diagram](diagrams/06_er_diagram.png)

## Design decisions
- **SQLite instead of MySQL**: the original idea was to use a MySQL server and a root password. SQLite ships with Python, so the project runs anywhere, and tests can use an in-memory database.
- **Service layer**: all rules live in services, so the menus only read input and print output.
- **`duration_seconds` column**: durations are stored as text for display and as seconds for fast, exact aggregation in reports.
- **Deletion guard**: vehicles and drivers with recorded trips cannot be deleted, so earnings history is never lost.

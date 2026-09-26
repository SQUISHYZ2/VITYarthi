# Problem Statement

## Problem
Small transport operators often track vehicles, drivers and trips in notebooks or spreadsheets. Fares are worked out by
hand, records go missing or get duplicated, and there is no quick way to see how much each driver or vehicle earns.

## Scope
The project provides a command-line system that:
- stores vehicles, drivers and trips in a database with consistent, validated data,
- bills every trip automatically from its duration at a fixed hourly rate,
- reports revenue by period, driver, vehicle and route.

Out of scope: live GPS tracking, online payments, passenger booking and a graphical or web interface.

## Target users
- The owner or administrator of a small transport or cab business.
- Dispatchers who record trips and check earnings.

## High-level features
1. Fleet management (vehicles and drivers, full CRUD).
2. Trips and billing (automatic total sum from `HH:MM:SS` duration).
3. Reports and analytics (revenue summary, earnings per driver and vehicle, top routes, CSV export).
4. Input validation, error handling and logging throughout.
